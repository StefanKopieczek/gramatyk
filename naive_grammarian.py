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
compound_letters = ['dzi', 'd'+z_acute, 'd'+z_dot, 'dz', 'bi', 'ci', 'ch',
                    'cz', 'gi', 'ki', 'mi', 'ni', 'pi', 'rz', 'si', 'sz',
                    'zi']
consonants = list('mbpwfndtzscrlgkhj') + [c_acute, z_dot, n_acute,
             z_acute, l_stroke] + compound_letters

# Conversion tables for hard consonants to soft, and vice versa.
soft_to_hard = 
{
    'pi'        : 'p',
    'bi'        : 'b',
    'fi'        : 'f',
    'wi'        : 'w',
    'mi'        : 'm',
    c_acute     : 't',
    'ci'        : 't',
    d + z_acute : 'd',
    s_acute     : 's',
    z_acute     : 'z',
    n_acute     : 'n',
    'ni'        : 'n',
    l           : l_stroke,
    'rz'        : 'r',
    'cz'        : 'c',      # cz softens to c, but c is still soft.
    'c'         : 'k',
    z_dot       : 'dz',     # z-dot softens to dz, but dz is still soft.
    'dz'        : 'g',
    'sz'        : 'ch',
    s_acute     : 'ch',
    'si'        : 'ch',
    'j'         : 'j'       # 'j' is soft, but has no matching hard consonant.   
}

hard_to_soft = {v:k for k, v in soft_to_hard.iteritems()}
del hard_to_soft['j'] # 'j' is not a hard consonant.

# -- Helper methods used by the Naive Grammarian -- #

def is_soft(letter):
    letter = letter.lower() # Ignore case for comparisons.
    return letter in soft_to_hard

def is_hard(letter):
    # We are hard if and only if we are not soft.
    # It is not enough to check the hard_to_soft table, since some soft
    # consonants have softened forms, and so appear there without being hard.
    return letter in consonants and not is_soft(letter)

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
    for (letter, next) in izip(letters, letters[1:] + None):
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
    def __init__(self,
                 nominative=None,
                 gender=None,
                 root=None):
        self._nominative = nominative
        self._gender = gender
        self._root = root
        self._animate = False  # Assume not animate
        self._personal = False # Assume not personal.

    @classmethod
    def setRoot(self, root):
        self._root = root
        
    @classmethod
    def setGender(self, gender):
        if gender in ['m', 'f', 'n']:
            self._gender = gender
        else:
            raise ValueError('Invalid gender \''+gender+'\'') 
     
    @classmethod
    def setAnimate(self, is_animate):
       """Set whether this Noun is to be regarded as an inanimate
          object for the purposes of declension. If not animate,
          also mark as 'not a person' since all personal nouns are
          necessarily animate."""
       self._animate = is_animate
       self._personal = self._personal and is_animate
    
    @classmethod
    def setPersonal(self, is_personal):
        """Set whether this Noun is to be regarded as a person for the
           purposes of declension. If it is, also mark it as animate,
           since all people are animate."""
        self._personal = is_personal
        self._animate = self._animate or is_personal
    
    @classmethod
    def guessRoot(self):
        if self._root is None:
            self._root = self._nominative
            if self._root[-1] in vowels:
                self._root = self._root[:-1]
                
        return self._root
        
    @classmethod
    def guessGender(self):
        if self._gender is None:
            if self._nominative[-1] in consonants and
               not self._nominative[-2] == 'um':
                self._gender = 'm'
            elif self._nominative[-1] in ['a', 'i']:
                self._gender = 'f'
            else:
                self._gender = 'n'
                    
        return self._gender
            
    @classmethod
    def guessPlural(self):
        gender = guessGender()
        root = getRoot()
        root_end = list(get_polish_letters(root))[-1]
        
        plural = ''
        if gender == 'm' and self._personal:
            plural = list(get_polish_letters(root))[:-1]
            plural += hard_to_soft(root_end)
            if plural[-1] in ['k', 'g']:
                plural += 'y'
            else:
                plural += 'i
        elif gender in ['m', 'f']:
            if root_end in ['g', 'k']:
                plural = root + 'y'
            elif is_hard(root_end):
                plural = root + 'i'
            else:
                plural = root + 'e'
       else:
            plural = root + 'a'
            
       return fix_letter_forms(plural)
            
    @classmethod
    def guessAccusative(self):
        gender = guessGender()
        root = guessRoot()
        root_end = list(get_polish_letters(root))[-1]
        
        accus = ''
        if gender == 'm':
            accus = root
            if self._animate:
                accus += 'a'
        elif gender == 'f';
            if is_soft(root_end):
                accus = root
            else:
                accus = root + e_nasal
        else:
            accus = self._nominative
        
        return fix_letter_forms(accus)
        
    @classmethod
    def guessAccusativePl(self):
        accuspl = ''
        if self.guessGender() == 'm' and self._personal:
            accuspl = self.guessGenitivePl()    
        else:
            accuspl = self.guessPlural()
            
    @classmethod
    def guessGenitive(self):
        gender = self.guessGender()
        root = self.guessRoot()
        root_end = list(polish_letters(root))[-1]
        
        gen = ''
        if (gender == 'm' and self._animate) or
           (gender == 'n'):
           gen = root + 'a'
        elif gender == 'm' and not self._animate:
            gen = root + 'u'
        else: # == 'f'
            if root_end in ['g', 'k']:
                gen = root + 'y'
            else:
                gen = root + 'i'
       
        return fix_letter_forms(gen)
        
    @classmethod
    def guessGenitivePl(self):
        return None # Todo
        
    @classmethod
    def guessDative(self):
        return None # Todo
        
    @classmethod
    def guessDativePl(self):
        return None # Todo
        
    @classmethod
    def guessInstrumental(self):
        return None # Todo
        
    @classmethod
    def guessInstrumentalPl(self):
        return None # Todo
        
    @classmethod
    def guessLocative(self):
        return None # Todo
        
    @classmethod
    def guessLocativePl(self):
        return None # Todo
        
    @classmethod
    def guessVocative(self):
        return None # Todo
        
    @classmethod
    def guessVocativePl(self):
        return None # Todo