#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
from pathlib import Path
import spacy

# configuration globals

wiki_compact_folder="/opt/Kbases/Wikipedia/wikicompact"
wiki_lemma_folder="/opt/Kbases/Wikipedia/wikilemma"

# globals changed during work

nlp_model=None

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
  nlp_model = spacy.load("en_core_web_sm",disable = ['parser','ner'])  
  filecount=0
  articlecount=0
  start_path=wiki_compact_folder
  folders1 = [name for name in os.listdir(start_path) if os.path.isdir(os.path.join(start_path, name))]
  folders1.sort()
  print("folders",folders1)
  #print(folders1)
  for folder1 in folders1:
    if folder1 in ["software"]: continue
    #if folder1!="t": continue
    if folder1<firstfolder: continue
    if folder1>lastfolder: continue
    path1=start_path+"/"+folder1
    folders2 = [name for name in os.listdir(path1) if os.path.isdir(os.path.join(path1, name))]
    folders2.sort()
    #print(folder1,folders2)
    for folder2 in folders2:
      #if folder2!="a": continue
      path2=path1+"/"+folder2
      folders3 = [name for name in os.listdir(path2) if not os.path.isdir(os.path.join(path2, name))]
      folders3.sort()
      print(folder1,folder2)
      #print(folder1,folder2,folders3)
      for folder3 in folders3:        
        #if folder3!="l": continue
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
        res=[]  
        artlinenr=0        
        for line in lines:          
          if line.startswith("$_article_separator_$"):
            articlecount+=1
            res.append(line)
            artlinenr=0
          else:
            artlinenr+=1
            if artlinenr==1:
              res.append(line)
            else:
              lineres=process_text(line)
              res.append(lineres)
        fullart="".join(res)
        #print(fullart)        
        outfolder=wiki_lemma_folder+"/"+folder1+"/"+folder2
        try:
          outfolderpath = Path(outfolder)
          outfolderpath.mkdir(parents= True, exist_ok= True)
        except:
          print("failed making path",outfolder)  
          continue
        outfilename=outfolder+"/"+folder3
        try:
          of=open(outfilename,"w")
          of.write(fullart)
          of.close()
        except:
          print("failed writing",outfilename,"at path",outfolder)        

  print("----------------")
  print("filecount",filecount)
  print("articlecount",articlecount)
 
def process_text(s):
  tokens = nlp_model(s)
  #print("tokens",tokens)
  #s=s.lower()
  lemmas=[]
  for token in tokens:
    #print("word",token.text, token.has_vector, token.vector_norm, token.is_oov, token.lemma_)
    lemmas.append(token.lemma_)
  #print(s)
  tmp=" ".join(lemmas)
  return tmp.lower()


main()  
