
import copy
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.corpus import wordnet
from nltk.corpus import brown
import tkinter as tk
import random
import sys

class Blackboard:

    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False,False)
        self.canvas = tk.Canvas(self.window,width=1000,height=1000)
        self.canvas.pack()

        self.lines = []
        self.lines.append([random.randint(10,700),random.randint(10,950),                            "One day they decided to sleep together","l0"])
        self.lines.append([random.randint(10,700),random.randint(10,950),                            "Next day they cooked a heavy breakfast","l1"])


        for ll in self.lines:
            self.canvas.create_text(ll[0],ll[1],text=ll[2],tags=ll[3], anchor=tk.W)
        self.agentList = [replaceWithHyponyms,replaceWithSpeechSynonym,makeTwoWordsRhyme,correctPositions,repairAAn]

        
    def run(self):
        print("*** in run")
        print(self.lines)
        print(len(self.lines))
        ag = random.choice(self.agentList)
        print("executing ",ag)
        self.lines = ag(self.lines)
        self.canvas.delete("all")
        for ll in self.lines:
            self.canvas.create_text(ll[0],ll[1],text=ll[2],tags=ll[3],anchor=tk.W)
        self.canvas.after(600,Blackboard.run,self)

    def main(self):
        self.run()
        self.window.mainloop()


def repairAAn(lines): #from lab7
    newLines = []
    for ll in lines:
        tokens = nltk.word_tokenize(ll[2])
        for idx,tok in enumerate(tokens[:-1]):
            if tok=="a":
                if (tokens[idx+1])[0] in "aeiou":
                    tokens[idx] = "an"
            if tok=="an":
                if (tokens[idx+1])[0] not in "aeiou":
                    tokens[idx] = "an"
        newLine = " ".join(tokens)
        newLines.append([ll[0],ll[1],newLine,ll[3]])
    return newLines

def replaceWithSynonym(lines): #from lab7
    ll = lines.pop(random.randrange(len(lines)))
    tokens = nltk.word_tokenize(ll[2])
    wordIdx = random.randrange(len(tokens))
    wordToBeReplaced = tokens[wordIdx]
    synonyms = []
    for syn in wordnet.synsets(wordToBeReplaced):
        for l in syn.lemmas():
            if not "_" in l.name():
                synonyms.append(l.name())
    if synonyms:
        tokens[wordIdx] = random.choice(synonyms)
    else:
        tokens[wordIdx] = wordToBeReplaced
    newLine = " ".join(tokens)
    lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

def replaceWithSpeechSynonym(lines):
    ll = lines.pop(random.randrange(len(lines))) #from lab7
    tokens = nltk.word_tokenize(ll[2])    #from lab7
    tagged = nltk.pos_tag(tokens)
    print(tagged)
    wordIdx = random.randrange(len(tokens)) #from lab7
    wordToBeReplaced = tokens[wordIdx]    #    from lab7
    #wordtoReplaceType = nltk.pos_tag(wordToBeReplaced)
    
    print('Word To Be Replaced:')            
    print(tagged[wordIdx])
    synonyms = []
    for syn in wordnet.synsets(wordToBeReplaced):
        for l in syn.lemmas():  #from lab7
            if not "_" in l.name():  
                r = syn.name()[0:syn.name().find(".")]
                synonyms.append(r)
                
    print('Synonyms:')            
    print(nltk.pos_tag(synonyms))
    
    r = [word for (word, pos) in nltk.pos_tag(synonyms) if str.startswith(pos, str(tagged[wordIdx][1]))] #stores synonyms with similar part of speech into a list
    print("Similar part-of-the-speach Synonyms:")
    print(r)

    if r:
        tokens[wordIdx] = random.choice(r)
        token_choice = tokens[wordIdx]
        print('succesfully replaced with:')
        print(token_choice)
    else:
        tokens[wordIdx] = wordToBeReplaced
        print('unsuccesfully replaced')
        
    newLine = " ".join(tokens)
    lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines


def replaceWithHyponyms(lines):   
    ll = lines.pop(random.randrange(len(lines)))
    tokens = nltk.word_tokenize(ll[2])
    print(tokens)
    wordIdx = random.randrange(len(tokens))
    wordToBeReplaced = tokens[wordIdx]
    stop_words = set(stopwords.words('english'))

    print('wordToBeReplaced:')
    print(wordToBeReplaced)

    if wordToBeReplaced not in stop_words: #checks if the word being replaced is a stopword 
        word = wordnet.synsets(wordToBeReplaced)[0]
        typeofword = wordnet.synsets(word.name())
        typesOfhyponyms = list(set([w for s in word.closure(lambda s: s.hyponyms()) for w in s.lemma_names()])) #appends hyponyms into a dictionary
        print('typesOfhyponyms:')            
        print(typesOfhyponyms)
        
        if typesOfhyponyms:
            tokens[wordIdx] = random.choice(typesOfhyponyms)
            token_choice = tokens[wordIdx]
            print('succesfully replaced with:')
            print(token_choice)
        else:
            tokens[wordIdx] = wordToBeReplaced
            print('Unsuccesfully replaced!:')

    newLine = " ".join(tokens)
    lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

def correctPositions(lines): #from lab7
    newLines = []
    for ll in lines:
        if ll[1]>900:
            newLines.append([ll[0],random.randrange(10,800),ll[2],ll[3]])
        else:
            newLines.append(ll)
    return newLines

def makeTwoWordsRhyme(lines):
    ll = lines.pop(random.randrange(len(lines)))
    tokens = nltk.word_tokenize(ll[2])
    wordIdx = random.randrange(len(tokens))
    wordToBeReplaced = tokens[wordIdx]
    beforeWord = tokens[wordIdx - 1] # the word before the word selected at random to be replaced
    print('word To Be Replaced:')
    print(wordToBeReplaced)
    
    print('the word before:')
    print(beforeWord)
    #getting the syllables of the word-before
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == beforeWord]
    print("SYLLABLES:")
    print(syllables)
    rhymes = []
    level = random.randrange(1,3)
    #according to the level specified different rhymes are appended
    for (word, syllable) in syllables:
        rhymes += [word for word, pronunciation in entries if pronunciation[-level:] == syllable[-level:]]
    print("rhymes of:",beforeWord)
    print(rhymes[0:10])

    synonyms = []
    for syn in wordnet.synsets(wordToBeReplaced):
        for l in syn.lemmas():
            synonyms.append(l.name())
    print("synonyms of: ",wordToBeReplaced)
    print(set(synonyms[0:10]))
    #Obtaining synonyms that rhyme with the word-before by getting the interection of synonyms and rhymes sets.
    synonymsThatRhyme = list(set(synonyms).intersection(set(rhymes)))
    if synonymsThatRhyme:
        tokens[wordIdx] = random.choice(synonymsThatRhyme)
        chsWord = tokens[wordIdx]
        print("Word replaced with:")
        print(chsWord)
    else:
        tokens[wordIdx] = wordToBeReplaced
        print("Word couldn't be replaced!")
    newLine = " ".join(tokens)
    lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

bb = Blackboard()
bb.main()

