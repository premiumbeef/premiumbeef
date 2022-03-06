# Good'n Burger

- Type  : Forensics
- Points: 200

## Description
The K9's are trading passwords in plain sight. By using excerpts of publicly available books as their passwords, they can pass around credentials completely incognito! Catmen Sanfrancisco has provided you a SHA256 hash of their password and books she suspects they are using. Discover the sentence that pertains to the hash `AAEEA96DD86D6ECBFE21755151B00266C79368584289D15B0BFE58D6B3498A36` to help thwart their nefurious plans!

## Solution
Reading the description provides us with a pretty clear idea of what to do for this challenge. We need to find a string in the given books that matches the hash above. 
I used the python library `ntlk` to help me tokenise the sentences in the text files. 

1. Create a python script to read through every single text files and obtain each sentences.
2. Hash the sentence using `SHA256` and compare it to the given hash.
3. After a few seconds, the script should print the output of the sentence matching the hash, which is the flag to use.

**FLAG: ATR[The Cat only grinned when it saw Alice.]**

## After Thoughts
Initially, i realised that `readlines` does not print any output. This is because `readlines` considers a "sentence" ending in `\r\n` and not an actual sentence. A sentence should end in punctuation (other than `,`). Hence i used `ntlk` to read in the text files as sentence. If given more time, i would have tried to use `regex` to sort out the sentences instead.

## Script
```python
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
```
