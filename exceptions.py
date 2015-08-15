#!/usr/bin/python
# -*- coding: UTF-8 -*-


class GramatykException(Exception):
    pass


class InputError(GramatykException):
    def __init__(self, bad_input):
        self.bad_input = bad_input
        super(InputError, self).__init__(repr(bad_input))


class UnknownWordType(InputError):
    pass
