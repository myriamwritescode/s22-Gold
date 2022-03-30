#! /usr/bin/env python3

# Created: 3/25/22
# Author : Brett Warren
# Project: s22-Gold
# File   : resources.py

"""
Description:
Classes here describe how a resource can be imported or exported.
"""
from import_export import resources
from .models import *


class ElectedOfficialResource(resources.ModelResource):

    class Meta:
        model = TestElectedOfficial
        import_id_fields = ('bioguide_id',)


class VotesResource(resources.ModelResource):

    class Meta:
        model = TestVote
        import_id_fields = ('voter_id', 'number', 'roll',)


class BillsResource(resources.ModelResource):

    class Meta:
        model = TestBill
        import_id_fields = ('bill_id',)
