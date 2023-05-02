#!/usr/bin/env python3

import sys
import json

import numpy as np

from string import ascii_letters, digits, punctuation
from argparse import ArgumentParser


# Instructions for the task. A random one will be assigned to each
# input/output pair.
INSTRUCTIONS = [
    'Korjaa virjeet seuraavasta tekstistä.',
    'Korjaa virheet.',
    'Korjaa teksti:',
]

# Default set of characters that can be substituted for
DEFAULT_CHARSET = ascii_letters + 'åäöÅÄÖ' + digits + punctuation + ' '


def argparser():
    ap = ArgumentParser()
    ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('--mean', type=float, default=0.1)
    ap.add_argument('--stdev', type=float, default=0.05)
    ap.add_argument('--min-error-prob', type=float, default=0.0)
    ap.add_argument('--max-error-prob', type=float, default=0.25)
    ap.add_argument('--delete-prob', type=float, default=0.1)
    ap.add_argument('--insert-prob', type=float, default=0.1)
    ap.add_argument('--charset', default=DEFAULT_CHARSET)
    ap.add_argument('jsonl', help='JSONL with text in "text" field')
    return ap


def add_noise(text, rng, args):
    # draw probability of error
    prob = rng.normal(args.mean, args.stdev)
    prob = min(max(prob, args.min_error_prob), args.max_error_prob)

    chars = []
    for c in text:
        if rng.random() > prob:
            chars.append(c)    # no error
        elif rng.random() < args.delete_prob:
            pass    # delete
        elif rng.random() < args.insert_prob:
            chars.append(rng.choice(args.charset))    # insert
            chars.append(c)
        else:
            chars.append(rng.choice(args.charset))    # substitute

    return ''.join(chars)


def main(argv):
    args = argparser().parse_args(argv[1:])
    args.charset = [c for c in args.charset]    # for np.random.choice

    # Adjust insert_prob: as the possibility of insertion is only
    # considered if the deletion probability threshold is not
    # exceeded, it needs to be adjusted to match the CLI probability
    args.insert_prob = args.insert_prob / (1-args.delete_prob)

    rng = np.random.default_rng(args.seed)

    with open(args.jsonl) as f:
        for line in f:
            indata = json.loads(line)
            instruction = rng.choice(INSTRUCTIONS)
            text = indata['text']
            noised = add_noise(text, rng, args)
            outdata = {
                'instruction': instruction,
                'input': noised,
                'output': text,
            }
            print(json.dumps(outdata, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
