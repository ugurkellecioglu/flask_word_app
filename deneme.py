
from random_words import RandomWords
# Configure application
from PyDictionary import PyDictionary
import random
import mysql.connector
def replace(s, position, character):
    return s[:position] + character + s[position+1:]
def random_word():
    rw = RandomWords()
    word = rw.random_word()
    return word

def definition(word):
    word = word
    dictionary=PyDictionary(word)
    definitions = dictionary.getMeanings()
    definitionx = definitions[word]['Noun']
    return definitionx
class Word:
    def __init__(self, word):
        self.word = word



word = random_word()
w1 = Word(word)
w2 = Word(len(w1.word)* "_")
answer = False


list = []
point = len(w1.word)
print("#############")
print("Hello this is a game that created by Uğur Kellecioğlu dedicated to cs50")
print("You have to find the words by looking their meanings. Good Luck")
print("#############")

length = len(w1.word)

tries = length
score = 0
count = 0
while answer != True:
    count =0
    ##print(w1.word)
    defi = definition(w1.word)
    for defin in defi:
        print(str(count + 1 ) + " ---> " + defin)
        count+=1
        if count == 3:
            break
    print("#############")
    print(w2.word)
    
    rnd = random.randint(0,length-1)
    

    x = input()
    if x == w1.word:
       
        print("TRUE")
        score += tries      
        w1 = Word(random_word())
        w2 = Word(len(w1.word)* "_") 
        print("Score" + str(score))
        tries = len(w1.word)
        list = []
    else:
        
        print("TRY AGAIN")
        tries -= 1
        
        
        if rnd not in list:
            w2.word = replace(w2.word,rnd, w1.word[rnd])
            list.append(rnd)
        else:
            while rnd in list:
                rnd = random.randint(0,len(w1.word)-1)
            w2.word = replace(w2.word,rnd, w1.word[rnd])
            list.append(rnd)
        print(w2.word)
        
      