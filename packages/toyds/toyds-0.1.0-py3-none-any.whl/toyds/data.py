from torch.utils.data import IterableDataset
import random

class ToyDataset(IterableDataset):
    """
    Produces an infinite stream of toy tasks for training debugging
    """

    def __init__(self, challenges:list[callable], probs:list[float]=None):
        self.challenges = challenges
        self.probs = probs

        if self.probs is None:
           self.probs = [1/len(challenges)]*len(challenges)

        assert sum(self.probs) == 1

    def gen(self):
        while True:
            func = random.choices(self.challenges, self.probs)[0]
            yield func.generate(), func

    def __iter__(self):
        return self.gen()


