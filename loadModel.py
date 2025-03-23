import gensim.downloader
from gensim.scripts.glove2word2vec import glove2word2vec


model = None
def load():
    global model
    glove_vectors = gensim.downloader.load('glove-wiki-gigaword-50')
    glove_vectors.save_word2vec_format('./glove-wiki-gigaword-50.txt')
    glove2word2vec('./glove-wiki-gigaword-50.txt', './glove-wiki-gigaword-50.txt')

