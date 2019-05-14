import keras
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

def cleanText(text):
    text = text.lower()
    
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'https?://[A-Za-z0-9./]+', 'url', text)
    
    text = nltk.word_tokenize(text)
    text = " ".join(text)
    
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"''", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r'\d', '', text)
    text = re.sub(r":", "", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r'(\w)\1{2,}', r'', text)
    text = re.sub(r'\w(\w)\1{2}', '', text)
    
    
    stops = set(stopwords.words('english'))
    text = text.split()
    text = [w for w in text if not w in stops and len(w) >= 3]   
    text = " ".join(text)
    
    return text

def cleanText(text_list):
    clean_text = []
    for i in range(len(text_list)):
        clean_text.append( cleanText(text_list[i]) )
    return clean_text

def tokenize(text_list):
    tokenizer = Tokenizer(lower=True)
    tokenizer.fit_on_texts(text_list)
    token_list = tokenizer.texts_to_sequences(text_list)
    return token_list, tokenizer.word_index

def padding(token_list, MAX_SEQUENCE_LENGTH):
    data = pad_sequences(token_list, maxlen=MAX_SEQUENCE_LENGTH)
    return data

def embeddingMatrixGenerate(EMBEDDING_DIM):
    embeddings_Glove = dict()
    testo = open('glove.twitter.27B.' + str(EMBEDDING_DIM) + 'd.txt', encoding = 'utf8')
    for line in testo:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_Glove[word] = coefs
    testo.close()

    embedding_matrix = np.zeros((WORD_INDEX_NUM+1, EMBEDDING_DIM))
    for word, index in tokenizer.word_index.items():
        embedding_vector = embeddings_Glove.get(word)
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector
    return embedding_matrix

if __name__ == '__main__':
    main()