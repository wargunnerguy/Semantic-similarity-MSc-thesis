#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# configuration globals

wiki_lemma_folder="/opt/Kbases/Wikipedia/wikilemma"
matrix_words_file="/opt/Kbases/Wikipedia/matrixwords"
wiki_matrix_file="/opt/Kbases/Wikipedia/wikimatrix"

# globals changed during work

wordlist=[]
wordnums={}
wordvecs={}

# ====== main carries out the whole process ======

def main():
  global nlp_model
  print(sys.argv)
  if len(sys.argv)!=3:
    print("please give two arguments: first and last folder name to be processed")
    return
  firstfolder=sys.argv[1]  
  lastfolder=sys.argv[2]
  print("firstfolder",firstfolder,"lastfolder",lastfolder)   
  
  read_wordnums()
  read_wordvecs()  
  """
  line="a of of and . and the"
  process_line(line,"")
  for word in wordlist:
    print(word,wordvecs[word])
  return
  """
  filecount=0
  articlecount=0
  start_path=wiki_lemma_folder
  folders1 = [name for name in os.listdir(start_path) if os.path.isdir(os.path.join(start_path, name))]
  folders1.sort()
  print("folders",folders1)
  #print(folders1)
  for folder1 in folders1:
    if folder1 in ["software"]: continue
    #if folder1!="a": continue
    if folder1<firstfolder: continue
    if folder1>lastfolder: continue
    path1=start_path+"/"+folder1
    folders2 = [name for name in os.listdir(path1) if os.path.isdir(os.path.join(path1, name))]
    folders2.sort()
    #print(folder1,folders2)
    for folder2 in folders2:
      #if folder2!="l": continue
      path2=path1+"/"+folder2
      folders3 = [name for name in os.listdir(path2) if not os.path.isdir(os.path.join(path2, name))]
      folders3.sort()
      print(folder1,folder2)
      #print(folder1,folder2,folders3)
      for folder3 in folders3:        
        #if folder3!="p": continue
        path3=path2+"/"+folder3        
        filecount+=1
        #print(path3)
        try:
          f=open(path3,"r")
          lines=f.readlines()
          f.close()
        except:
          print("failed opening",path3)
          return None
        artlinenr=0
        for line in lines:          
          if line.startswith("$_article_separator_$"):
            articlecount+=1            
            artlinenr=0
            title=None
          else:
            artlinenr+=1
            if artlinenr==1:
              #print("*****",line)
              title=line
            else:
              process_line(line,title)        
      
  print("----------------")
  print("filecount",filecount)
  print("articlecount",articlecount)
  write_matrix_file()  
  #for word in wordlist:
  #  print(word,wordvecs[word])
 
def process_line(line,title):
  if not line: return
  titlewords=process_title(title)
  #print("titlewords",titlewords)
  #print(line)
  if "?" in line:
    line=line.replace("?",".")
  if "!" in line:
    line=line.replace("!",".")  
  sentences=line.split(".")
  sentnum=0
  for sentence in sentences:    
    words=sentence.split(" ")
    if (not words) or len(words)<2: continue
    sentnum+=1
    goodwords=[]
    for word in words:
      if not word: continue
      if not word.isalnum(): continue
      goodwords.append(word)
    #print(goodwords)  
 
    i=0
    for word in goodwords:
      j=0
      for word2 in goodwords:
        if i==j: continue
        if word in wordnums and word2 in wordnums:
          wordvecs[word][wordnums[word2]]+=1
          wordvecs[word2][wordnums[word]]+=1
        j+=1
      i+=1  

def process_title(title):
  if not title: return []
  words=title.split("_")
  #print("words",words)
  goodwords=[]
  for word in words:
    word=word.strip()
    if not word or len(word)<4: continue
    if not word.isalpha(): continue
    word=word.lower()
    goodwords.append(word)
  return goodwords

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
  num=0
  try:
    f=open(wiki_matrix_file,"r")
    lines=f.readlines()
    f.close()
  except:
    print("cannot read wordvecs from, making empty file",wiki_matrix_file)
    make_empty_matrix_file()
    try:
      f=open(wiki_matrix_file,"r")
      lines=f.readlines()
      f.close()
    except:
      print("cannot read wordvecs even from the empty file created",wiki_matrix_file)
      sys.exit(0)
  for line in lines:
    if not line: continue
    line=line.strip()
    if not line: continue
    els=line.split(",")
    title=els[0]
    if not (title in wordnums):
      print("vec title not in wordnums",title)
      sys.exit(0)
    if (title in wordvecs):
      print("vec title already in wordvecs",title)
      sys.exit(0)  
    nums=[]
    for num in els[1:]:
      try:
        intnum=int(num)
      except:
        print("error parsing num in line",num,line)
        sys.exit()  
      nums.append(intnum)  
    wordvecs[title]=nums
  #print("wordvecs",wordvecs)

def make_empty_matrix_file():
  try:
    f=open(wiki_matrix_file,"a")    
  except:
    print("cannot open matrix_file for creation",wiki_matrix_file)
    sys.exit(0) 
  for word in wordlist:
    s=word
    for word2 in wordlist:
      s+=",0"
    f.write(s+"\n")
  f.close()

def write_matrix_file():
  try:
    f=open(wiki_matrix_file,"w")    
  except:
    print("cannot open matrix_file for writing",wiki_matrix_file)
    sys.exit(0) 
  for word in wordlist:
    s=word
    vec=wordvecs[word]
    for num in vec:
      s+=","+str(num)
    f.write(s+"\n")
  f.close()


main()  
