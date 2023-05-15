#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np

# configuration globals

matrix_words_file="/opt/Kbases/Wikipedia/matrixwords"
matrix_counts_file="/opt/Kbases/Wikipedia/wikimatrixcount20000"
matrix_related_file="/opt/Kbases/Wikipedia/wikimatrixrelated20000"
matrix_relatedtop_file="/opt/Kbases/Wikipedia/wikimatrixrelatedtop20000"

# globals changed during work


wordlist=[]
wordnums={}
wordoccsums={}
wordrelated={}


# ====== main carries out the whole process ======

def main():

  read_wordnums() 
  read_wordoccsums()
  read_related()  

  tests=["plant","sea","england","spoon","tyre","particle","engine","potato","green","night","owl",""]

  """
  for el in tests:
    relatedness_example(el)

  return
  """

  wordn=0
  results=[]
  for word in wordlist:
    reslst=[word,str(wordoccsums[word])]
    #print("\n****",word,wordnums[word],wordoccsums[word])
    pos=0
    pairs=[]
    for el in wordrelated[word]:
      pair=[wordlist[pos],el]
      pairs.append(pair)      
      pos+=1
    pairs.sort(key=lambda x:x[1],reverse=True)
    pcount=0
    for pair in pairs:    
      if pair[1]==0: break
      reslst.append(pair[0])
      reslst.append(str(pair[1]))
      #print(pair[0]+" "+str(pair[1])+",",end="")      
      pcount+=1
      if pcount>=1000: break
    wordn+=1
    results.append(",".join(reslst))
    #if wordn>1000: break

  try:
    f=open(matrix_relatedtop_file,"w")
    for line in results:
     f.write(line+"\n")
    f.close()
  except:
    print("cannot write to",matrix_relatedtop_file)     

  return
  
def relatedness(w1,w2):
  #print("w1","|"+w1+"|",w1 in wordrelated,"w2",w2 in wordrelated)
  if not((w1 in wordrelated) and (w2 in wordrelated)): return None
  if w1==w2: return 1
  w1num=wordnums[w1]
  w2num=wordnums[w2]
  r1=wordrelated[w1][w2num]
  r2=wordrelated[w2][w1num]
  #if r1<r2: r=r1
  #else: r=r2
  r=(r1+r2)/2
  r=r/10000000
  return r

def relatedness_example(word):
  print("*** "+word+": ",end="")
  if not word: 
    print()
    return
  word=word.lower()
  word=word.strip()
  if not word: 
    print()
    return
  if not (word in wordrelated): 
    print()
    return
  word=word.lower()
  words=["root","estonia","germany","castle","sea","wave","mountain","food","plastic","owl","blue","carbon","light","wheel"]  
  for el in words:
    print(el,relatedness(word,el), " ",end="")
  print()
 

def read_wordnums():
  global wordlist,wordnums
  num=0
  try:
    f=open(matrix_words_file,"r")
    lines=f.readlines()
    f.close()
  except:
    print("cannot read wordnums from",matrix_words_file)
    sys.exit(0)
  for line in lines:
    line=line.strip()
    line=line.lower()
    if line in wordnums: continue
    wordlist.append(line)
    wordnums[line]=num
    num+=1
  #print("wordlist",wordlist)  
  #print("wordnums",wordnums)

def read_wordoccsums():
  global wordlist,wordnums,wordoccsums
  try:
    f=open(matrix_counts_file,"r")
    lines=f.readlines()
    f.close()
  except:
    print("cannot read wordoccsums from",matrix_counts_file)
    sys.exit(0)
  for line in lines:
    spl=line.split(",")
    word=spl[0]
    num=int(spl[1])
    wordoccsums[word]=num
     

def read_related():
  global wordrelated
  try:
    f=open(matrix_related_file,"r")
    lines=f.readlines()
    f.close()
  except:
    print("cannot read relatedness from",matrix_related_file)    
    sys.exit(0)
  linenr=0    
  for line in lines:
    #print("line:",line)
    if not line: continue
    arr=np.fromstring(line, dtype=int, sep=',')       
    title=wordlist[linenr]          
    wordrelated[title]=arr  
    linenr+=1      
    #print("ok lines in",matrix_related_file,linenr) 




main()  
