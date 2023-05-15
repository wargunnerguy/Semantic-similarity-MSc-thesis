#!/usr/bin/env python3

# before running:
#  * install spacy
#  * load spacy nlp data like this:
#    python -m spacy download en_core_web_md

import sys
import math
import csv
import re
import spacy

# configuration globals

raw_words_filename="important_words.txt"

max_produced=20000

# globals used and changed during work


# ====== main carries out the whole process ======

def main():
  found=0
  try:
    f=open(raw_words_filename,"r")
    words=f.readlines()
    f.close()
  except:
    print("failed reading",raw_words_filename) 
    return
  i=0
  res=[]
  dict={}
  for word in words:        
    if "_" in word: 
      i+=1
      continue
    #print(word,word.isalnum())    
    #print(i,word)
    sp=word.split(" ")
    w1=sp[0]
    w1=w1.strip()
    #print("w1",w1)
    if not w1.isalnum():
      i+=1
      continue
    w1=w1.lower()
    if w1 in dict:
      i+=1
      continue
    i+=1
    dict[w1]=True
    res.append(w1)
    found+=1
    #print(i,found,w1)
    print(w1)
    if found>=max_produced:
      break    

main()
