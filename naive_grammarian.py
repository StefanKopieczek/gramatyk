# Polish special characters.
a_nasal  =  u'\u0105'
c_acute  =  u'\u0107'
e_nasal  =  u'\u0119'
l_stroke =  u'\u0142'
n_acute  =  u'\u0144'
o_acute  =  u'\u00f3'
s_acute  =  u'\u015b'
z_acute  =  u'\u017a'
z_dot    =  u'\u017c'

# Character classes used by the Naive Grammarian.
vowels = ['a', 'e', 'i', 'o', 'u', 'y', a_nasal, e_nasal, o_nasal] 
consonants = list('mbpwfndtzscrlgkhj') + 
             ['dz', 'd'+z_acute, c_acute, z_dot, 'rz', 'sz', 'd'+z_dot, 'cz', 
              n_acute, 'ch', l_stroke]

# Conversion tables for hard consonants to soft, and vice versa.
soft_to_hard = 
{
    'pi'        : 'p',
    'bi'        : 'b',
    'fi'        : 'f',
    'wi'        : 'w',
    'mi'        : 'm',
    c_acute     : 't',
    d + z_acute : 'd',
    s_acute     : 's',
    z_acute     : 'z',
    n_acute     : 'n',
    l           : l_stroke,
    'rz'        : 'r',
    'cz'        : 'c',      # cz softens to c, but c is still soft.
    'c'         : 'k',
    z_dot       : 'dz',     # z-dot softens to dz, but dz is still soft.
    'dz'        : 'g',
    'sz'        : 'ch',
    s_acute     : 'ch',
    'j'         : 'j'       # 'j' is soft, but has no matching hard consonant.   
}

hard_to_soft = {v:k for k, v in soft_to_hard.iteritems()}
del hard_to_soft['j'] # 'j' is not a hard consonant.

# -- Helper methods used by the Naive Grammarian -- #

def _cluster_is_soft(cluster):
    cluster = cluster.lower() # Ignore case for comparisons.
    return cluster in soft_to_hard

def _cluster_is_hard(cluster):
    # We are hard if and only if we are not soft.
    # It is not enough to check the hard_to_soft table, since some soft
    # consonants have softened forms, and so appear there without being hard.
    return not _cluster_is_soft(cluster)

def fix_letter_forms(word):
    """Corrects a word which wrongly uses a certain letter instead of its
       equivalent; for example, ci- should be used in place of c-acute before
       vowels."""
    pass # todo

class Noun(object):
    def __init__(self, nominative):
        self._nominative = nominative

    @classmethod
    def getRoot(self):
        
