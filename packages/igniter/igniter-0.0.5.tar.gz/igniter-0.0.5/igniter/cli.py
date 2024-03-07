#!/usr/bin/env python

import argparse
import os

from igniter.logger import logger
from igniter.main import initiate


def main():
    parser = argparse.ArgumentParser(description='Igniter Command Line Interface (CLI)')
    parser.add_argument('--config', type=str, help='Configuration filename')
    parser.add_argument('--pkg', type=str, required=False, default=None)
    args = parser.parse_args()
    logger.error(args)

    if args.pkg:
        directory = os.path.dirname(args.pkg)

    # print("<<< ", directory)
    # config = os.path.abspath(args.config)
    logger.warning(f'Using config {args.config}')
    
    initiate(args.config)

    # p = os.path.dirname(os.path.abspath(__file__)) + '/../example/configs/mnist.yaml'
    # initiate(p)


if __name__ == '__main__':
    main()
