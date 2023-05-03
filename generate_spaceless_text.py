#!/usr/bin/env python3

import sys
import re
import json

import numpy as np

from argparse import ArgumentParser


# Instructions for the task. A random one will be assigned to each
# input/output pair.
INSTRUCTIONS = [
    'Erottele sanat tekstistä.'
]


def argparser():
    ap = ArgumentParser()
    ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('jsonl', help='JSONL with text in "text" field')
    return ap


def remove_space(text, args):
    return re.sub(r'\s+', '', text)


def main(argv):
    args = argparser().parse_args(argv[1:])

    rng = np.random.default_rng(args.seed)

    with open(args.jsonl) as f:
        for line in f:
            indata = json.loads(line)
            instruction = rng.choice(INSTRUCTIONS)
            text = indata['text']
            spaceless = remove_space(text, args)
            outdata = {
                'instruction': instruction,
                'input': spaceless,
                'output': text,
            }
            print(json.dumps(outdata, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
