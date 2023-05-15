#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# configuration globals

wiki_lemma_folder="/opt/Kbases/Wikipedia/wikilemma"
matrix_words_file="/opt/Kbases/Wikipedia/matrixwords"
wiki_matrix_file="/opt/Kbases/Wikipedia/wikimatrixmod"

# globals changed during work

stopwords={}
wordlist=[]
wordnums={}
wordvecs={}

increments=[0,10,8,5,5,4,4,3,3,3,2,2,2,2,2,2,2]
incrementslen=len(increments)

# ====== main carries out the whole process ======

def main():
  global stopwords
  print(sys.argv)
  if len(sys.argv)!=3:
    print("please give two arguments: first and last folder name to be processed")
    return
  firstfolder=sys.argv[1]  
  lastfolder=sys.argv[2]
  print("firstfolder",firstfolder,"lastfolder",lastfolder)   
  
  for word in raw_stopwords:
    if word.isalpha() and not (word in stopwords):
      stopwords[word]=True
  #print(stopwords)
  #return

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
  #print("folders",folders1)
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
              process_line(line,title,artlinenr)        

  print("----------------")
  print("filecount",filecount)
  print("articlecount",articlecount)
  write_matrix_file()  
  #for word in wordlist:
  #  print(word,wordvecs[word])
 
def process_line(line,title,artlinenr):
  #print("line,title,artlinenr",line,title,artlinenr)
  if not line: return
  titlewords=process_title(title)
  titlelen=len(titlewords)
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
      if len(word)<3: continue     
      if word in stopwords: continue      
      if not word.isalnum(): continue
      goodwords.append(word)
    #print("goodwords:",goodwords)  
 
    # connect title words to first sentences
    if (artlinenr==2 and sentnum<4) or titlelen==1: # line 1 is title, line 2 is first paragraph
      for word in titlewords:
        if not word: continue 
        if len(word)<3: continue     
        if word in stopwords: continue      
        if not word.isalnum(): continue
        if not (word in wordnums): continue
        #print("sentnum, ok titleword:",sentnum,word)
        for word2 in goodwords:
          if word==word2: continue
          if word2 in wordnums:
            if sentnum>=4: added=1
            else: added=4-sentnum
            wordvecs[word][wordnums[word2]]+=added
            wordvecs[word2][wordnums[word]]+=added

    i=0
    for word in goodwords:
      if not (word in wordnums): 
        i+=1
        continue
      j=0
      for word2 in goodwords:
        if i==j: continue
        if word2 in wordnums:
          dist=abs(i-j)
          if dist>=incrementslen:
            added=1
          else:
            added=increments[dist]            
          wordvecs[word][wordnums[word2]]+=added
          wordvecs[word2][wordnums[word]]+=added
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

raw_stopwords=["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", 
"be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
"did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had",
 "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", 
 "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
  "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", 
  "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", 
  "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", 
  "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
   "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", 
   "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", 
   "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", 
   "you've", "your", "yours", "yourself", "yourselves"]

main()  
