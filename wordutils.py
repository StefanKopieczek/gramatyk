from __future__ import unicode_literals

VOWELS = set('aąeęioóuy')
CONSONANTS = (set('bcćdfghjklłmnńprsśtwzźż') +
              set(['bi', 'ch', 'ci', 'cz', 'dz', 'dzi', 'dź', 'dż', 'gi',
                   'ki', 'mi', 'ni', 'pi', 'rz', 'si', 'sz', 'zi']))


def trim_suffix(word, suffix):
    if word.endswith(suffix):
        word = word[:-len(suffix)]
    return word


def trim_prefix(word, prefix):
    if word.startswith(prefix):
        word = word[len(prefix):]
    return word


def join(*args):
    stack = list(args)
    while len(stack) > 1:
        stack = stack[:-2] + [_join_two(stack[-2], stack[-1])]
    return stack[0]


def _join_two(w1, w2):
    # TODO: Implement this properly, respecting Polish joining rules.
    return w1 + w2
