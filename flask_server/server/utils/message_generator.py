from random import choices, uniform, random
from math import floor


def get_wordlist():
    wordlist = []
    with open("./words.txt", "r") as f:
        for word in f:
            word = word.rstrip()
            if not word:
                continue
            wordlist.append(word.rstrip())

    return wordlist


def generate_random_message(num_words, wordlist=None):
    if wordlist is None or len(wordlist) == 0:
        wordlist = get_wordlist()
    word_array = choices(wordlist, k=num_words)
    word_array[0] = word_array[0].capitalize()
    return " ".join(word_array) + "."


wordlist = get_wordlist()


def generate_message_element(min_len=5, max_len=50, sender=None, wordlist=None):
    if sender not in ["sent", "recieved"]:
        sender = ["sent", "recieved"][round(random())]

    wrapped = f"<div class='message'>\n\t<div class='{sender}'>\n\t\t<p class='{sender}-message'>\n\t\t{generate_random_message(floor(uniform(min_len,max_len)), wordlist=wordlist)}\n\t\t</p>\n\t</div>\n</div>"
    return wrapped


for _ in range(15):
    print(generate_message_element(wordlist=wordlist))
