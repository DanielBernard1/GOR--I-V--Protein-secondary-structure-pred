#!/usr/bin/env python3
import argparse
import MySQLdb

db = MySQLdb
parser = argparse.ArgumentParser(description="Add Swissprot to Database")
parser.add_argument("--input", type=str, required=True, help="Path to swissprot data")

args = parser.parse_args()
file_path = args.input

with open(file_path, "r") as f:
    for line in f:
        print('')