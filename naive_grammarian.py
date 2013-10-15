from itertools import izip

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
compound_letters = ['dzi', 'd'+z_acute, 'd'+z_dot, 'dz', 'bi', 'ci', 'ch',
                    'cz', 'gi', 'ki', 'mi', 'ni', 'pi', 'rz', 'si', 'sz',
                    'zi']

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

def polish_letters(word):
    """"Generator for the polish letter groups in a word, respecting 
    compound letters such as ci and dzi."""
    while word != '':
        compound_match = False
        for group in compound_letters:
            if word.startswith(group):
                yield group
                word = word[len(group):]
                compound_match = True
                break
        if not compound_match:
            yield word[0]
            word = word[1:]
        
def fix_letter_forms(word):
    """Corrects a word which wrongly uses a certain letter instead of its
       equivalent; for example, ci- should be used in place of c-acute before
       vowels."""
    letters = list(polish_letters(word)
    result = ''
    for (letter, next) in izip(letters, letters + None):
        substitution = True
        if next in vowels:
            if letter == c_acute:
                result += 'ci'
            elif letter == 'd' + z_acute:
                result += 'dzi'
            elif letter == n_acute:
                result += 'ni'
            elif letter = s_acute:
                result += 'si'
            elif letter = z_dot:
                result += 'zi'
            else:
                substitution = False
        else:
            if letter == 'ci':
                result += c_acute
            elif letter == 'dzi':
                result += 'd' + z_acute
            elif letter == 'ni':
                result += n_acute
            elif letter == 'si':
                result += s_acute
            elif letter == 'zi'   
                result += z_dot
            else:
                substitution = False
           
        if not substitution:
            result += letter
        
    return result     

class Noun(object):
    def __init__(self, nominative):
        self._nominative = nominative

    @classmethod
    def getRoot(self):
        root = self._nominative
        if root[-1] in vowels:
            root = root[:-1]
        return root
            
