import torch
from torch.nn import Module
from torch import Tensor, nn
import torch.nn.functional as F

from .config import Config
from .modules import ScaledSinusoidalEmbedding, Decoder

class GPT(Module):

    def __init__(self, config: Config = Config()):
        super().__init__()

        self.config = config
        modelcfg = config.model
        dmodel = modelcfg.dmodel
        self.num_embs = modelcfg.num_embs

        self.pad_idx = 0
        self.eos_idx = 1
        self.token_emb = nn.Embedding(self.num_embs, dmodel)

        self.token_head = nn.Linear(dmodel, self.num_embs, bias=modelcfg.bias)
        self.init_mod_weights = []
        self.token_pos = ScaledSinusoidalEmbedding(dmodel, max_seqlen=modelcfg.max_seq_len)

        self.decoder = Decoder(
            d_model=dmodel,
            n_heads=modelcfg.nheads,
            n_layers=modelcfg.layers,
            bias=modelcfg.bias,
            dropout=modelcfg.dropout,
        )

        self.init_mod_weights += [
            self.decoder,
            self.token_head,
            self.token_pos,
        ]

        for w in self.init_mod_weights:
            w.apply(self._init_weights)

    def configure_optimizers(
        self, *, weight_decay: float, lr: float, betas: tuple[float, float]
    ):
        # start with all of the candidate parameters
        param_dict = {pn: p for pn, p in self.named_parameters()}
        # filter out those that do not require grad
        param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}
        # create optim groups. Any parameters that is 2D will be weight decayed, otherwise no.
        # i.e. all weight tensors in matmuls + embeddings decay, all biases and layernorms don't.
        decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
        nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
        optim_groups = [
            {"params": decay_params, "weight_decay": weight_decay},
            {"params": nodecay_params, "weight_decay": 0.0},
        ]

        optimizer = torch.optim.AdamW(optim_groups, lr=lr, betas=betas, fused=True)

        return optimizer

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
        elif isinstance(module, nn.Conv1d):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)

    def forward(
        self,
        tokens: Tensor,
        loss_funcs: dict[callable],
        lengths: Tensor,
    ):
        max_seq_len = self.config.model.max_seq_len
        pad_tokens  = F.pad(tokens, (0, max(0, max_seq_len - tokens.size(-1))))
        embs = pad_tokens[:, :-1]
        embs = self.token_emb(embs) + self.token_pos(torch.arange(embs.shape[-1]))
        embs = self.decoder(embs)
        embs = self.token_head(embs).permute(0, 2, 1)
        loss = torch.tensor(0, device=tokens.device, dtype=embs.dtype)


        # This is the slightly complicated bit!
        for v in loss_funcs.values():
            loss += v["loss"](embs[v["items"]], tokens, lengths)

        return loss

    @torch.inference_mode()
    def generate(
        self,
        prompt: Tensor,
        temperature=0.8,
        max_steps=10,
        top_k: int = 100,
        top_p: float = 0.0,
    ):
        # TODO
        cfg = self.config.model
        pass

    def from_pretrained(ckpt: str | dict):
        """
        {
            "config": config.model_dump(),
            "step": step,
            "model": {
                k: v
                for k, v in model.state_dict().items()
                if not k.startswith("dac.")
            },
            "optimizer": optimizer.state_dict(),
        }
        """
        if type(ckpt) is str:
            ckpt = torch.load(ckpt)

        config = Config(**ckpt["config"])
        model = GPT(config)
        model.load_state_dict(ckpt["model"], strict=False)
        return model
