#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np

# configuration globals

matrix_words_file="/opt/Kbases/Wikipedia/matrixwords"
wiki_matrix_file="/opt/Kbases/Wikipedia/wikimatrixmod20000"
matrix_counts_file="/opt/Kbases/Wikipedia/wikimatrixcount20000"

# globals changed during work


wordlist=[]
wordnums={}
wordvecs={}
wordoccsums={}

# ====== main carries out the whole process ======

def main():

  """
  print(sys.argv)
  if len(sys.argv)!=3:
    print("please give two arguments: first and last folder name to be processed")
    return
  """  
  read_wordnums() 
  read_wordvecs()  

  totalcount=0
  maxnum=0
  zerocount=0
  occnr=0
  for word in wordlist:
    vec=wordvecs[word]
    occnr=0
    for el in vec:
      #if el>maxnum: maxnum=el
      #if el==0: zerocount+=1
      #totalcount+=1
      occnr+=el
    wordoccsums[word]=occnr
 
  try:
    f=open(matrix_counts_file,"w")
    for word in wordlist:
      s=word+","+str(wordoccsums[word])+"\n"
      f.write(s)
    f.close()
  except:
    print("cannot write to",matrix_counts_file)
    sys.exit(0) 

  #print("totalcount",totalcount)
  #print("maxnum",maxnum)
  #print("zerocount",zerocount)  

  return
  

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

def read_wordvecs():
  global wordvecs
  try:
    f=open(wiki_matrix_file,"r")
    lines=f.readlines()
    f.close()
  except:
    print("cannot read wordvecs from",wiki_matrix_file)
    sys.exit(0)
  linenr=0    
  for line in lines:
    #print("line:",line)
    if not line: continue    
    i=0
    while line[i]!=",": i+=1
    title=line[0:i]
    title=title.strip()
    #print("title:",title)
    numbers=line[i+1:]    
    arr=np.fromstring(numbers, dtype=int, sep=',')
    #for el in arr:
    #  print(","+str(el),end = '')
    #print("\narray length was:",len(arr))
    #print("\n")  
    linenr+=1    
    if not (title in wordnums):
      print("vec title not in wordnums",title)
      sys.exit(0)
    if (title in wordvecs):
      print("vec title already in wordvecs",title)
      sys.exit(0)      
    wordvecs[title]=arr        
  #print("wordvecs",wordvecs)


main()  
