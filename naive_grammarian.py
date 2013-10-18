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
vowels = ['a', 'e', 'i', 'o', 'u', 'y', a_nasal, e_nasal, o_acute] 
compound_letters = ['dzi', 'd'+z_acute, 'd'+z_dot, 'dz', 'bi', 'ci', 'ch',
                    'cz', 'gi', 'ki', 'mi', 'ni', 'pi', 'rz', 'si', 'sz',
                    'zi']
consonants = list('mbpwfndtzscrlgkhj') + [c_acute, z_dot, n_acute,
             z_acute, l_stroke] + compound_letters

# Conversion tables for hard consonants to soft, and vice versa.
soft_to_hard = { 
    'pi'          : 'p',
    'bi'          : 'b',
    'fi'          : 'f',
    'wi'          : 'w',
    'mi'          : 'm',
    'ci'          : 't',
    c_acute       : 't',
    'd' + z_acute : 'd',
    'si'          : 's',
    s_acute       : 's',
    z_acute       : 'z',
    'ni'          : 'n',
    n_acute       : 'n',
    'l'           : l_stroke,
    'rz'          : 'r',
    'cz'          : 'c',      # cz softens to c, but c is still soft.
    'c'           : 'k',
    z_dot         : 'dz',     # z-dot softens to dz, but dz is still soft.
    'dz'          : 'g',
    'sz'          : 'ch',
    'j'           : 'j'       # 'j' is soft, but has no matching hard consonant.   
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
    letters = list(polish_letters(word))
    result = ''
    for (letter, next) in izip(letters, letters[1:] + [None]):
        substitution = True
        if next in vowels:
            if letter == c_acute:
                result += 'ci'
            elif letter == 'd' + z_acute:
                result += 'dzi'
            elif letter == n_acute:
                result += 'ni'
            elif letter == s_acute:
                result += 'si'
            elif letter == z_dot:
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
            elif letter == 'zi':   
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

    def setRoot(self, root):
        self._root = root
        
    def setGender(self, gender):
        if gender in ['m', 'f', 'n']:
            self._gender = gender
        else:
            raise ValueError('Invalid gender \''+gender+'\'') 

    def setAnimate(self, is_animate):
       """Set whether this Noun is to be regarded as an inanimate
          object for the purposes of declension. If not animate,
          also mark as 'not a person' since all personal nouns are
          necessarily animate."""
       self._animate = is_animate
       self._personal = self._personal and is_animate
    
    def setPersonal(self, is_personal):
        """Set whether this Noun is to be regarded as a person for the
           purposes of declension. If it is, also mark it as animate,
           since all people are animate."""
        self._personal = is_personal
        self._animate = self._animate or is_personal
    
    def guessRoot(self):
        if self._root is None:
            self._root = self._nominative
            if self._root[-1] in vowels:
                self._root = self._root[:-1]
                
        return self._root
        
    def guessGender(self):
        if self._gender is None:
            if (self._nominative[-1] in consonants and
                not self._nominative[-2] == 'um'):
                self._gender = 'm'
            elif self._nominative[-1] in ['a', 'i']:
                self._gender = 'f'
            else:
                self._gender = 'n'
                    
        return self._gender
            
    def guessPlural(self):
        gender = self.guessGender()
        root = self.guessRoot()
        root_end = list(polish_letters(root))[-1]
        
        plural = ''
        if gender == 'm' and self._personal:
            plural = list(get_polish_letters(root))[:-1]
            plural += hard_to_soft(root_end)
            if plural[-1] in ['k', 'g']:
                plural += 'i'
            else:
                plural += 'y'
        elif gender in ['m', 'f']:
            if root_end in ['g', 'k']:
                plural = root + 'i'
            elif is_hard(root_end):
                plural = root + 'y'
            else:
                plural = root + 'e'
        else:
            plural = root + 'a'
            
        return fix_letter_forms(plural)
            
    def guessAccusative(self):
        gender = self.guessGender()
        root = self.guessRoot()
        root_end = list(polish_letters(root))[-1]
        nom_end = list(polish_letters(self._nominative))[-1]
        
        accus = ''
        if gender == 'm':
            accus = root
            if self._animate:
                accus += 'a'
        elif gender == 'f':
            if is_soft(root_end) and not nom_end in ['a', 'i']:
                accus = root
            else:
                accus = root + e_nasal
        else:
            accus = self._nominative
        
        return fix_letter_forms(accus)
        
    def guessAccusativePl(self):
        accuspl = ''
        if self.guessGender() == 'm' and self._personal:
            accuspl = self.guessGenitivePl()    
        else:
            accuspl = self.guessPlural()

        return fix_letter_forms(accuspl)
            
    def guessGenitive(self):
        gender = self.guessGender()
        root = self.guessRoot()
        root_end = list(polish_letters(root))[-1]
        
        gen = ''
        if ((gender == 'm' and self._animate) or
            (gender == 'n')):
           gen = root + 'a'
        elif gender == 'm' and not self._animate:
            gen = root + 'u'
        else: # == 'f'
            if root_end in ['g', 'k']:
                gen = root + 'i'
            else:
                gen = root + 'y'
       
        return fix_letter_forms(gen)
        
    def guessGenitivePl(self):
        gender = self.guessGender()
        root = self.guessRoot()
        root_end = list(polish_letters(root))[-1]
        nom_end = list(polish_letters(self._nominative))[-1]
        
        genpl = ''
        if is_soft(root_end) and (gender == 'm' or 
           (gender == 'f' and nom_end in ['a', 'i'])):
            if root_end in ['g', 'k']:
                genpl = root + 'i'
            else:
                gen = root + 'y'
        elif gender == 'm':
            # Masculine noun, hard stem.
            genpl = root + o_acute + 'w'
        else:
            # Feminine noun with hard stem, or neuter noun.
            genpl = root

        return fix_letter_forms(genpl)        

    def guessDative(self):
        gender = self.guessGender()
        root = self.guessRoot()
        root_end = list(polish_letters(root))[-1]
        
        dative = ''
        if gender == 'm':
            dative = root + 'owi'
        elif gender == 'f' and is_hard(root_end):
            dative = (''.join(polish_letters(root))[:-1] + 
                      hard_to_soft[root_end] + 'e')
        elif gender == 'f':
            # Feminine, soft stem.
            if root_end in ['g', 'k']:
                dative = root + 'i'
            else:
                dative = root + 'y'
        else:
            # Neuter
            dative = root + 'u' 
        
        return fix_letter_forms(dative)
        
    def guessDativePl(self):
        return fix_letter_forms(self.guessRoot() + 'om')    
        
    def guessInstrumental(self):
        instrumental = ''
        root = self.guessRoot()
        if self.guessGender() == 'f':
            instrumental = root + a_nasal
        else:
            instrumental = root + 'em'
        
        return fix_letter_forms(instrumental)

    def guessInstrumentalPl(self):
        return self.guessRoot() + 'ami'
        
    def guessLocative(self):
        gender = self.guessGender()
        root = self.guessRoot()
        root_end = list(polish_letters(root))[-1] 

        locative = ''
        if gender == 'f':
            locative = self.guessDative()
        elif is_soft(root_end) or root_end in ['k', 'g', 'w']:
            locative = root + 'u'
        else:
            locative = (''.join(polish_letters(root))[:-1] + 
                        hard_to_soft[root_end] + 'e')
            
        return fix_letter_forms(locative) 
        
    def guessLocativePl(self):
        return fix_letter_forms(self.guessRoot() + 'ach') 
        
    def guessVocative(self):
        gender = self.guessGender()
        root = self.guessRoot()
        root_end = list(polish_letters(root))[-1]
        nom_end = list(polish_letters(self._nominative))[-1]

        vocative = ''
        if gender == 'f' and (is_hard(root_end) or nom_end in ['a', 'i']):
            vocative = root + 'o' 
        elif gender == 'f' and root_end in ['k', 'g']:
            vocative = root + 'i'
        elif gender == 'f':
            vocative = root + 'y'
        elif gender == 'm':
            vocative = self.guessLocative()
        else:
            # Neuter
            vocative = self._nominative

        return fix_letter_forms(vocative)
        
    def guessVocativePl(self):
        return fix_letter_forms(self.guessPlural()) 
