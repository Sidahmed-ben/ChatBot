import nltk
import numpy as np
nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
import spacy
nlp = spacy.load('fr_core_news_md')


# Fonction qui sépare une phrase en groupe de mots
def separe_phrase(phrase):
    return nltk.word_tokenize(phrase)

# Fonction qui retourne la racine d'un mot
def racine(mots):
    if(mots == "foot"):
        mots = "football"
    for mot in mots:
        return mot.lemma_

# Fonction qui retourne le bag d'un mot
def bag_de_mot(phrase_separe, tout_mots):
    phrase_separe= [racine(nlp(w.lower())) for w in phrase_separe]
    bag = np.zeros(len(tout_mots),dtype=np.float32)
    for idx,w in enumerate(tout_mots):
        if w in phrase_separe:
            bag[idx] = 1.0
    return bag
