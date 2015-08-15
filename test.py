#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import words
import predict_engine
import sys

if __name__ == "__main__":
    conj = sys.argv[1:]
    conj = [(None if form == '?' else form) for form in conj]
    v = words.Verb()
    v.present = conj
    predict_engine.complete(v)
    print(v.pprint())
