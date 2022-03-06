import os
import hashlib
from nltk import tokenize
import spacy

hash_to_match = "AAEEA96DD86D6ECBFE21755151B00266C79368584289D15B0BFE58D6B3498A36"

def hash_string(string):
    """
    Return a SHA-256 hash of the given string
    """
    return hashlib.sha256(string.encode('utf-8')).hexdigest().upper()

def read_book(book):
    current_book = open(book, 'r')
    contents = current_book.read()
    sentences = tokenize.sent_tokenize(contents)
    for sentence in sentences:
        hash = hash_string(sentence)
        if hash == hash_to_match:
            print("Sentence: {}".format(sentence))
            break

def main():
    for book in os.listdir("."):
        read_book(book)
    print("done")
if __name__ == "__main__":
    main()
