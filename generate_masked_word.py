#!/usr/bin/env python3

import sys
import re
import json

import numpy as np

from argparse import ArgumentParser


# Text for replaced word
REPLACEMENT = '_____'

# Instructions for the task. A random one will be assigned to each
# input/output pair.
INSTRUCTIONS = [
    'Mikä sana puuttuu seuraavasta tekstistä?'
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


def mask_word(text, rng, args):
    tokens = TOKENIZATION_RE.findall(text)
    tokens = [t for t in tokens if t]
    assert ''.join(tokens) == text

    indices = masked_token_candidate_indices(tokens)
    index = rng.choice(indices)
    
    word = tokens[index]
    tokens[index] = REPLACEMENT

    masked = ''.join(tokens)
    return word, masked


def main(argv):
    args = argparser().parse_args(argv[1:])

    rng = np.random.default_rng(args.seed)

    with open(args.jsonl) as f:
        for line in f:
            indata = json.loads(line)
            instruction = rng.choice(INSTRUCTIONS)
            text = indata['text']
            word, masked = mask_word(text, rng, args)
            outdata = {
                'instruction': instruction,
                'input': masked,
                'output': word,
            }
            print(json.dumps(outdata, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
