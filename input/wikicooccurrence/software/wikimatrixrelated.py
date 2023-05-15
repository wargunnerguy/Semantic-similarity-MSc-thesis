#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np

# configuration globals

matrix_words_file="/opt/Kbases/Wikipedia/matrixwords"
wiki_matrix_file="/opt/Kbases/Wikipedia/wikimatrixmod20000"
matrix_counts_file="/opt/Kbases/Wikipedia/wikimatrixcount20000"
matrix_related_file="/opt/Kbases/Wikipedia/wikimatrixrelated20000"

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
  read_wordoccsums()
  read_wordvecs()  

  n=0
  lst=[]
  for word in wordlist:
    #if wordoccsums[word]==0: continue
    wordoccsum=wordoccsums[word]
    vec=wordvecs[word]
    occnr=0
    pos=0
    ratios1=[]
    ratios2=[]
    vecres=[]
    for el in vec:      
      if el==0: 
        vecres.append(str(0))
        pos+=1
        continue
      elword=wordlist[pos]
      #if elword==word: 
      #  pos+=1
      #  continue
      #ratio1=el/wordoccsum
      elwordoccsum=wordoccsums[elword]
      ratio2=(el/math.sqrt(elwordoccsum))/wordoccsum
      #ratios1.append([elword,ratio1])
      ratio2int=round(ratio2*1000*1000*1000*1000)
      #ratios2.append([elword,ratio2int])
      vecres.append(str(ratio2int))
      pos+=1
    #ratios1.sort(key=lambda x:x[1],reverse=True)  
    """
    ratios2.sort(key=lambda x:x[1],reverse=True)
    worddata=[word,wordoccsum,
              ratios2[0][0],ratios2[0][1],
              ratios2[1][0],ratios2[1][1],
              ratios2[2][0],ratios2[2][1],
              ratios2[-1][0],ratios2[-1][1]]
    worddata=[word,wordoccsum,
              ratios2[0][0],"{:.10f}".format(ratios2[0][1]),
              ratios2[1][0],"{:.10f}".format(ratios2[1][1]),
              ratios2[2][0],"{:.10f}".format(ratios2[2][1]),
              ratios2[-1][0],"{:.10f}".format(ratios2[-1][1])]
    """          
    #lst.append(worddata)
    lst.append(",".join(vecres))
    n+=1
    #if n>1000: break

  #lst.sort(key=lambda x:x[3],reverse=True)

  try:
    f=open(matrix_related_file,"w")
    for line in lst:
      f.write(line+"\n")
    f.close()
  except:
    print("cannot write matrix related file",matrix_related_file)
    sys.exit(0)

  """ 
  for el in lst:
    i=0
    while i<len(el):
      el[i]=str(el[i])
      i+=1 
    print(",".join(el))
  """     

  """
  print("**** ",word)
  print("ratios1: ")
  i=0
  for el in ratios1:
    print(el[0]+" "+"{:.10f}".format(el[1])+",",end="")
    i+=1
    if i>100: break
  print()
  print("ratios2: ")
  i=0
  for el in ratios2:
    print(el[0]+" "+"{:.10f}".format(el[1])+",",end="")
    i+=1
    if i>100: break
  print()
  """

  #n+=1
  #if n>1000: break

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

def make_empty_matrix_file():
  try:
    f=open(wiki_matrix_file,"a")    
  except:
    print("cannot open matrix_file for creation",wiki_matrix_file)
    sys.exit(0) 
  for word in wordlist:
    s=[word]
    for word2 in wordlist:
      s.append(",0")
    f.write("".join(s)+"\n")
  f.close()

def write_matrix_file():
  try:
    f=open(wiki_matrix_file,"w")    
  except:
    print("cannot open matrix_file for writing",wiki_matrix_file)
    sys.exit(0) 
  for word in wordlist:
    s=[word]
    vec=wordvecs[word]
    for num in vec:
      s.append(",")
      s.append(str(num))
    f.write("".join(s)+"\n")
  f.close()


main()  
