#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import exceptions
import words
import wordutils

from collections import Counter
from itertools import product

_PRESENT_TENSE_ENDINGS = [
    [['ę'], ['esz'], ['e'], ['emy'], ['ecie'], ['ą']],
    [['ę'], ['isz', 'ysz'],  ['i', 'y'], ['imy', 'ymy'], ['icie', 'ycie'], ['ą']],
    [['am'], ['asz'], ['a'], ['amy'], ['acie'], ['ają', 'adzą']],
    [['em'], ['esz'], ['e'], ['emy'], ['ecie'], ['eją', 'edzą']]
]


def complete(word):
    if isinstance(word, words.Verb):
        _complete_verb(word)
    else:
        raise exceptions.UnknownWordType(word.__class__)


def _complete_verb(verb):
    if verb.category is None:
        verb.category = _deduce_category(verb)

    if verb.root is None:
        verb.root = _deduce_verb_root(verb)

    if verb.infinitive is None:
        verb.infinitive = _deduce_infinitive(verb)

    # Build up the present tense.
    for person, plurality in product(range(3), range(2)):
        idx = 3 * plurality + person
        if verb.present[idx] is None:
            verb.present[idx] = _deduce_present_tense(verb, person, plurality)


def _deduce_category(verb):
    possibilities = [category for category in range(1, 5)
                     if _verb_matches_category(verb, category)]
    if len(possibilities) == 1:
        return possibilities[0]
    else:
        return None


def _verb_matches_category(verb, category):
    for idx, endings in enumerate(_PRESENT_TENSE_ENDINGS[category - 1]):
        form = verb.present[idx]
        if form is not None and all(not form.endswith(x) for x in endings):
            return False
    return True


def _deduce_verb_root(verb):
    candidates = []
    for idx, form in enumerate(verb.present):
        if form is not None:
            trimmings = [wordutils.trim_suffix(form, ending)
                         for category in _PRESENT_TENSE_ENDINGS
                         for ending in category[idx]]
            candidates.append(min(trimmings, key=len))

    return Counter(candidates).most_common(1)[0][0]


def _deduce_infinitive(verb):
    return verb.root + 'ać'


def _deduce_present_tense(verb, person, plurality):
    if verb.category:
        ending = _PRESENT_TENSE_ENDINGS[verb.category - 1][plurality * 3 + person][0]
        return wordutils.join(verb.root, ending)
    return None
