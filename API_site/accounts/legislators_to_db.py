#! /usr/bin/env python3

# Created: 3/25/22
# Author : Brett Warren
# Project: s22-Gold
# File   : legislators_to_db.py

"""
Description:

"""
from models import Legislator
import pandas as pd
import csvImporter


def main():
    legislators_list = Legislator.import_data(data=open("../../legislators/current_legislators.csv"))
    print(legislators_list[0])


if __name__ == '__main__':
    main()
