#!/usr/bin/env python3
import argparse
import mysql.connector
import os

parser = argparse.ArgumentParser()
parser.add_argument("--sam", required=True)
parser.add_argument("--no-off-targets", required=False)
parser.add_argument("--with-mismatch", required=False)

args = parser.parse_args()
samfile = args.sam

off_target_or_mismatch = 