import torch
import random
import torch.nn.functional as F
from .task import Task

"""
Needle in the haystack problems
"""


def filter_sequence(vocab_size=10, max_len=10):
    """
    Given a sequence, filter out all but a queried set of numbers  in the prompt, producing the numbers from the original sequnce in order that they appear.

    Examples:


    [D, D, C, A, A, A, B, C, D, |, A, |, A, A, A ]

    [D, D, A, B, D, D, C, A, C, |, C, A, | A, C, A, C ]

    """
    pass



def lookup_item(vocab_size=1000, max_seq_len=5000, occurences=1):
    """
    With a large vocab size, determine wether and item is an a sequence

    [A, ......, Z, | Z | T]
    """

    ML = max_seq_len - 4

    # Has to be at least one thing to search for
    minL = 5
    length = random.randint(minL, ML)

    vocab_size -= 1

    randtoken = lambda:  random.randint(4, vocab_size)
    lookfor = randtoken()
    tosearch = torch.randint(4, vocab_size, (length,))

    for i in (tosearch == lookfor).nonzero():
        rand = randtoken()

        while rand == lookfor:
            rand = randtoken()

        tosearch[i] = rand

    contains = random.random() < .5
    if contains:
        idxs = random.sample(list(range(len(tosearch))), k=occurences)
        tosearch[idxs] = lookfor

    # 0 pad 1 EOS 2 Command 3 True 4 False
    contains = 3 if contains else 4
    tosearch = torch.cat((tosearch, torch.tensor([2, lookfor, 2, contains])))
    return tosearch


class LookupItem(Task):

    def generate(self):
        return lookup_item(*self.args, **self.kwargs)

    def train(self, logits, seq, lengths):
        """
        We only really need the last logits
        """
        logits = torch.stack([logits[i, lengths[i]-1] for i in range(len(lengths))])
        targets = torch.stack([seq[i, lengths[i]-1] for i in range(len(lengths))])
        return F.cross_entropy(logits, targets)


