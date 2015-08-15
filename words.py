#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Word(object):
    pass


class Verb(Word):
    def __init__(self):
        self.infinitive = None
        self.category = None
        self.root = None
        self.present = [None] * 6

    def pprint(self):
        return '\n'.join([
            'Infinitive: %s' % self.infinitive,
            '%s\t%s' % (self.present[0], self.present[3]),
            '%s\t%s' % (self.present[1], self.present[4]),
            '%s\t%s' % (self.present[2], self.present[5]),
        ])
