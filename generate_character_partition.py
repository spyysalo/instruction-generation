#!/usr/bin/env python3

import sys
import re
import json

import numpy as np

from argparse import ArgumentParser


# Instructions for the task. A random one will be assigned to each
# input/output pair.
INSTRUCTIONS = [
    'Koosta kirjaimet sanoiksi.'
]

# Regular expression for tokenization
TOKENIZATION_RE = re.compile(r'([^\W_]+|\S|.)')


def argparser():
    ap = ArgumentParser()
    ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('jsonl', help='JSONL with text in "text" field')
    return ap


def masked_token_candidate_indices(tokens):
    # Prefer alphabetic token
    candidates = [
        i for i, t in enumerate(tokens)
        if all(c.isalpha() for c in t)
    ]
    if candidates:
        return candidates

    # As a second option, alphanumeric
    candidates = [
        i for i, t in enumerate(tokens)
        if all(c.isanum() for c in t)
    ]
    if candidates:
        return candidates

    # Third option, non-whitespace
    candidates = [
        i for i, t in enumerate(tokens)
        if all(not c.isspace() for c in t)
    ]
    if candidates:
        return candidates
    
    # Final fallback: anything
    return list(range(len(tokens)))


def partition_chars(text, args):
    text = re.sub(r'\s+', '', text)
    return ' '.join(text)


def main(argv):
    args = argparser().parse_args(argv[1:])

    rng = np.random.default_rng(args.seed)

    with open(args.jsonl) as f:
        for line in f:
            indata = json.loads(line)
            instruction = rng.choice(INSTRUCTIONS)
            text = indata['text']
            partitioned = partition_chars(text, args)
            outdata = {
                'instruction': instruction,
                'input': partitioned,
                'output': text,
            }
            print(json.dumps(outdata, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
