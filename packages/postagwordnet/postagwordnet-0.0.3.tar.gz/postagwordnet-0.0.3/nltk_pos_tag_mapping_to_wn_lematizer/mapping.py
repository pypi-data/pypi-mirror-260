import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
def word_net_map(str=""):
    #str="Picture to text converter allows you to extract text from image or convert PDF to Word, Excel or Text formats using Optical Character Recognition software online"  
    words=word_tokenize(str)
    word_tags=pos_tag(words)
    tag_map = { 
    'CC':None, # coordin. conjunction (and, but, or) .
    'CD':wn.NOUN, # cardinaL number (one, two) 
    'DT':None, # determiner (a, the) 
    'EX':wn.ADV, # existentiaL 'there' (there)
    'FW':None, # foreign word (mea cuLpa) 
    'IN':wn.ADV, # preposition/sub-conj (of, in, by) 
    'JJ':[wn.ADJ, wn.ADJ_SAT], # adjective (yellow) 
    'JJR':[wn.ADJ, wn.ADJ_SAT], # adj., comparative (bigger) 
    'JJS':[wn.ADJ, wn.ADJ_SAT], # adj., superLative (wildest) 
    'LS':None, # List item marker (1, 2, One) 
    'MD':None, # modaL (can, shouLd) 
    'NN':wn.NOUN, # noun, sing. or mass (LLama) 
    'NNS':wn.NOUN, # noun, pLuraL (Llamas) 
    'NNP':wn.NOUN, # proper noun, sing. (IBM) 
    'NNPS':wn.NOUN, # proper noun, pLuraL (CaroLinas) 
    'PDT':[wn.ADJ, wn.ADJ_SAT], # predeterminer (aLL, both) 
    'POS':None, # possessive ending ('s ) 
    'PRP':None, # personaL pronoun (I, you, he) 
    'PRPV':None, # possessive pronoun (your, one's) 
    'RB':wn.ADV, # adverb (quickLy, never) 
    'RBR':wn.ADV, # adverb, comparative (faster) 
    'RBS':wn.ADV, # adverb, superLative (fastest) 
    'RP':[wn.ADJ, wn.ADJ_SAT], # particle (up, off) 
    'SYM':None, # symbol (+Ac, &) 
    'TO':None, # "to" (to) # interjection (ah, oops) 
    'VB':wn.VERB, # verb base form (eat) 
    'VBD':wn.VERB, # verb past tense (ate) 
    'VBG':wn.VERB, # verb gerund (eating) 
    'VBN':wn.VERB, # verb past participle (eaten) 
    'VBP':wn.VERB, # verb non-3sg pres (eat) 
    'VBZ':wn.VERB, # verb 3sg pres (eats))
    ',':None, 
    }
    #print(word_tags)
    wordnet_tags=[(w,tag_map[word_tags[x][1]])for x, w in enumerate(words)]
    #print(wordnet_tags)
    return wordnet_tags