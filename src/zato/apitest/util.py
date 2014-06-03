# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import csv, operator, os, random, uuid
from datetime import timedelta

# Arrow
from arrow import api as arrow_api

# Bunch
from bunch import Bunch

# Dateutil
from dateutil.parser import parse as parse_dt

# six
from six.moves import cStringIO as StringIO

# Zato
from zato.apitest import version

random.seed()

# Singleton used for storing Zato's own context across features and steps.
# Not thread-safe so this will have to be added if need be.
context = Bunch()

def new_context(old_ctx, environment_dir):
    context.zato = Bunch()
    context.zato.user_data = {}
    context.zato.date_formats = {'default':'YYYY-MM-DDTHH:mm:ss'}
    context.zato.environment_dir = old_ctx.zato.environment_dir if old_ctx else environment_dir
    context.zato.request = Bunch()
    context.zato.request.headers = {'User-Agent':'zato.apitest/{} (+https://zato.io)'.format(version)}
    context.zato.request.ns_map = {}

    return context

# ################################################################################################################################

def get_full_path(base_dir, *path_items):
    return os.path.normpath(os.path.join(base_dir, *path_items))

def get_file(path):
    return open(path).read()

# ################################################################################################################################

def parse_list(value):
    return tuple(csv.reader(StringIO(value)))[0]

def any_from_list(value):
    return random.choice(tuple(elem.strip() for elem in parse_list(value) if elem)).decode('utf-8')

# ################################################################################################################################

def rand_string(count=1):
    # First character is 'a' so it nevers starts with a digit.
    # Some parsers will insist a string is an integer if they notice a digit at idx 0.
    if count == 1:
        return 'a' + uuid.uuid4().hex
    else:
        return ['a' + uuid.uuid4().hex for x in range(count)]

def rand_int(min=0, max=100):
    return random.choice(range(min, max))

def rand_float(min, max):
    return float(rand_int(min, max)) + random.random()

def rand_date(format, start=None, stop=None):
    if not(start and stop):
        # Now is as random as any other date
        return now(format)

# ################################################################################################################################

def now(format):
    return arrow_api.now().format(format)

def utcnow(format):
    return arrow_api.utcnow().format(format)

# ################################################################################################################################

def date_after_before(base_date, format, direction, limit, needs_parse=True):
    if needs_parse:
        base_date = parse_dt(base_date)

    days=rand_int(0, abs(limit))
    return arrow_api.get(direction(base_date, timedelta(days=days))).format(format)

def date_after(base_date, format, limit=100000, needs_parse=True):
    return date_after_before(base_date, format, operator.add, limit, needs_parse)

def date_before(base_date, format, limit=100000, needs_parse=True):
    return date_after_before(base_date, format, operator.sub, limit, needs_parse)

def date_between(start_date, end_date, format):
    start_date = parse_dt(start_date)
    end_date = parse_dt(end_date)

    diff = int((start_date - end_date).days)
    func = date_after if end_date > start_date else date_before
    return func(start_date, format, diff, False)

# ################################################################################################################################