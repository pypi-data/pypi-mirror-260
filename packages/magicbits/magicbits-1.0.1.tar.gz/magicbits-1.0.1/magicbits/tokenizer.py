import nltk
from nltk.tokenize import word_tokenize


def tokenize(text):
    nltk.download('punkt')
    tokens = word_tokenize(text)
    return tokens

if __name__ == '__main__':
    tokenized = tokenize(
        'THIS IS A COMPUTER SCIENCE CLASS, WE ARE STUDYING NLP TOKENIZATION')
    print(tokenized)

