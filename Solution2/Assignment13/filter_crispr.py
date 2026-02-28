#!/usr/bin/env python3
import argparse
import mysql.connector
import os
import re
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--sam", required=True)
parser.add_argument("--no-off-targets", required=False)
parser.add_argument("--with-mismatch", required=False)

args = parser.parse_args()
samfile = args.sam
no_off_targets = args.no_off_targets
with_mismatch = args.with_mismatch

alignments = defaultdict(list)

