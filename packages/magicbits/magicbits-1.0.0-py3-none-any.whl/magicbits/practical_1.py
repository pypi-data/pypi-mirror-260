import nltk
from nltk.tokenize import word_tokenize


def tokenize(text):
    nltk.download('punkt')
    tokens = word_tokenize(text)
    return tokens


tokenized = tokenize(
    'THIS IS A COMPUTER SCIENCE CLASS, WE ARE STUDYING NLP TOKENIZATION')
print(tokenized)

print('Coded by Durani Mohammed Zaeem, Roll No: 557')
