import os
import time
from contextlib import nullcontext
from functools import partial

import torch
import torch.multiprocessing as mp
from torch.distributed import destroy_process_group, init_process_group
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.nn.utils import clip_grad_norm_
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader

import wandb
from toyds import utils, download
from toyds.config import Config, load_config
from toyds.model import GPT as Model
from toyds.data import ToyDataset
from toyds.tasks.needle import LookupItem
from toyds import optim, download
from toyds.utils import count_parameters, to_device

def train(rank: int, world_size: int, config: Config, dev: bool = False):
    if world_size > 1:
        init_process_group(
            backend="nccl",
            world_size=world_size,
            rank=rank,
        )

    torch.cuda.set_device(rank)
    device = torch.cuda.current_device()

    start_time = time.time()
    train = config.train
    datacfg = config.data

    assert config.run_dir is not None

    is_main_process = rank == 0
    B = train.batch_size

    if is_main_process:
        wandb.init(
            project="toyds",
            config=config.model_dump(),
            name="dev" if dev else None,
        )

    dtype = (
        torch.bfloat16
        if torch.cuda.is_available() and torch.cuda.is_bf16_supported()
        else torch.float16
    )

    model = Model(config).cuda(rank)
    embs = config.model.num_embs
    ds = ToyDataset([LookupItem(vocab_size=embs, max_seq_len=config.model.max_seq_len)])

    def collate_fn(batch):
        sequences = [b[0] for b in batch]
        lengths = torch.tensor([s.shape[-1] for s in sequences])
        loss_funcs = {}
        for i, s in enumerate(batch):
            task = s[1]
            if task.name not in loss_funcs:
                loss_funcs[task.name] = {
                    "loss": task.train,
                    "items": []
                }
            loss_funcs[task.name]["items"].append(i)

        tokens = pad_sequence(sequences, batch_first=True)
        return {"tokens": tokens, "loss_funcs": loss_funcs, "lengths": lengths}

    train_dl = DataLoader(
        ds,
        batch_size=B,
        collate_fn=collate_fn,
        num_workers=datacfg.num_workers,
        pin_memory=True,
        persistent_workers=datacfg.num_workers > 0,
    )

    betas = tuple(train.betas)
    optimizer = model.configure_optimizers(
        weight_decay=train.weight_decay, lr=train.min_lr, betas=betas
    )

    step = 0

    if train.checkpoint is not None:
        checkpoint_path = train.checkpoint

        if "http" in checkpoint_path:
            checkpoint_path = download.dl_http_file(checkpoint_path)

        if ":" in checkpoint_path:
            checkpoint_path = download.dl_scp_file(checkpoint_path)

        checkpoint = torch.load(checkpoint_path, map_location=f"cuda:{rank}")
        utils.load_what_you_can(checkpoint["model"], model)

        if train.continue_from_checkpoint:
            optimizer.load_state_dict(checkpoint["optimizer"])
            step = checkpoint["step"]

        del checkpoint
        torch.cuda.empty_cache()

    # if not dev:
    #     model = torch.compile(model)

    if world_size > 1:
        model = DDP(model, device_ids=[rank])

    if is_main_process:
        print(f"{count_parameters(model) / 1_000_000:.2f}M parameters")

    max_lr = train.max_lr or 10.0 * train.min_lr
    gradient_accumulation_steps = train.grad_acc_steps

    train_dl_iter = iter(train_dl)

    batch = to_device(next(train_dl_iter), device)

    def wandb_log(*args, **kwargs):
        if is_main_process:
            wandb.log(*args, **kwargs)
        if dev:
            print(*args)

    get_lr = getattr(optim, train.lr_schedule)

    wait, warmup, active = 5, 5, 5
    steps = wait + warmup + active if train.torch_profile else train.total_steps

    prof = (
        torch.profiler.profile(
            activities=[
                torch.profiler.ProfilerActivity.CPU,
                torch.profiler.ProfilerActivity.CUDA,
            ],
            schedule=torch.profiler.schedule(
                wait=wait, warmup=warmup, active=active, repeat=1
            ),
            on_trace_ready=torch.profiler.tensorboard_trace_handler("./profiles"),
            record_shapes=False,
            profile_memory=False,
            with_stack=False,  # incurs an additional overhead, disable if not needed
            with_flops=True,
            with_modules=False,  # only for torchscript models atm
        )
        if train.torch_profile
        else nullcontext()
    )

    loss = 0.0
    losses = []
    running = True

    if is_main_process:
        print(f"Took {time.time() - start_time:.2f}s to hit training")

    with prof:
        while step < steps and running:
            t1 = time.perf_counter()
            lr = get_lr(
                step, train.lr_warmup_steps, train.total_steps, train.min_lr, max_lr
            )

            for param_group in optimizer.param_groups:
                param_group["lr"] = lr

            for micro_step in range(gradient_accumulation_steps):
                model.require_backward_grad_sync = (
                    micro_step == gradient_accumulation_steps - 1
                )

                with torch.amp.autocast(
                    enabled=True, device_type="cuda", dtype=dtype
                ), torch.backends.cuda.sdp_kernel(**train.flash.model_dump()):
                    loss = model(**batch)
                    loss = loss / gradient_accumulation_steps

                if torch.isnan(loss):
                    wandb.alert("Nan Detection", "Stopping!")
                    running = False
                    continue

                loss.backward()
                batch = to_device(next(train_dl_iter), device)

            if is_main_process and step == 0:
                print(
                    f"Took {time.time() - start_time:.2f}s to finish first step training loop"
                )

            grad_norm = clip_grad_norm_(model.parameters(), train.max_grad_norm)

            optimizer.step()
            optimizer.zero_grad()
            step += 1

            t2 = time.perf_counter()

            if train.torch_profile:
                prof.step()

            if step % train.log_every == 0:
                loss = loss.item() * gradient_accumulation_steps
                # Determining loss slope for explosion detection / divergence
                # losses.append(loss)
                # loss_slope = optim.calculate_smoothed_slope(
                #     losses,
                #     regression_win=train.regression_win,
                #     smoothing_constant=train.regression_smoothing,
                # )

                # if loss_slope > 1e-3 and steps > 400:
                #     wandb.alert("Explosion Warning", "Check loss graph")

                metrics = {
                    "train/loss": loss,
                    "train/grad_norm": grad_norm.item(),
                    "train/lr": lr,
                    "train/batch_duration": t2 - t1,
                    # "train/loss_slope": loss_slope,
                }

                wandb_log(
                    metrics,
                    step=step,
                )

            if step % train.checkpoint_every == 0 and is_main_process:
                checkpoint = {
                    "config": config.model_dump(),
                    "step": step,
                    "model": {
                        k: v
                        for k, v in model.state_dict().items()
                        if not k.startswith("dac.")
                    },
                    "optimizer": optimizer.state_dict(),
                }
                file_url = os.path.join(config.run_dir, f"{step:07}.pt")
                print(f"Saved checkpoint to {file_url}")
                torch.save(checkpoint, file_url)

    if world_size > 1:
        destroy_process_group()


def main(
    config: str | Config,
    dev: bool = False,
    profile: bool = False,
):
    config: Config = load_config(config)

    config.train.torch_profile = config.train.torch_profile or profile

    if dev:
        print("Running in dev mode (smaller dataset, batch size, fewer epochs, etc.)")
        config.data.num_workers = 0

    if config.train.is_resuming:
        print(f"Resuming from {config.train.checkpoint}. Incrementing seed.")
        # TODO save the seed state in the checkpoint
        config.seed += 1

    if "MASTER_ADDR" not in os.environ:
        os.environ["MASTER_ADDR"] = "127.0.0.1"

    if "MASTER_PORT" not in os.environ:
        os.environ["MASTER_PORT"] = "17778"

    world_size = config.train.gpus
    if world_size is None:
        world_size = torch.cuda.device_count()

    if world_size > 1:
        mp.spawn(
            train,
            args=(world_size, config, dev),
            nprocs=world_size,
            join=True,
        )
    else:
        train(0, world_size, config, dev)

def cli_main():
    import argparse

    parser = argparse.ArgumentParser(description="GPT Training")

    # Add a positional argument 'config' which expects a string input
    parser.add_argument("config", help="Path to configuration file")

    # Add optional boolean flags with short and long versions
    parser.add_argument("-d", "--dev", action='store_true', help="Run in dev mode")
    parser.add_argument("-p", "--profile", action='store_true', help="Profile memory usage")

    args = parser.parse_args()

    # Access values from parsed arguments
    config = args.config
    dev = args.dev
    profile = args.profile
    main(config, dev, profile)


if __name__ =="__main__":
    cli_main()
