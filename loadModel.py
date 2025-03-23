import time

from gensim.models import KeyedVectors

model = None
def load():
    global model
    model = KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
