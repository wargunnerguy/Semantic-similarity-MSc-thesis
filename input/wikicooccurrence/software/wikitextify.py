#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
from html.parser import HTMLParser
from pathlib import Path

# configuration globals

wiki_input_folder="/media/tanel/wd_ntfs_1/Data/wikihtml"
wiki_output_folder="/opt/Kbases/Wikipedia/wikitext"

# ====== main carries out the whole process ======

def main():
  start_path=wiki_input_folder
  contents1=os.listdir(start_path) 
  #print(contents1)
  for path,dirs,files in os.walk(start_path):
    #for name in dirs:
    #  print("dir",name)
    for filename in files:      
      if badfile(filename): 
        #print("bad name",filename)
        continue
      fullname=os.path.join(path,filename)
      #plen=len(fullname)
      slen=len(start_path)
      outpath=wiki_output_folder+fullname[slen:-4]+"txt"
      lastslash=outpath.rfind("/")
      outfolder=outpath[:lastslash]
      if os.path.isfile(outpath):
        #print("exists",outpath)
        continue
      if smallfile(fullname):
        #print("small",fullname)
        continue
      print("conv",fullname,outpath)       
      try:
        f=open(fullname,"r")
        htmltext=f.read()
        f.close()
      except:
        print("failed opening",fullname)
        continue    
      try:
        f = HTMLFilter()
        start=find_start(htmltext)
        end=find_end(htmltext)
        f.feed(htmltext[start:end])
        txt=f.text
      except:
        print("failed parsing",fullname)
        continue     
      try:
        outfolderpath = Path(outfolder)
        outfolderpath.mkdir(parents= True, exist_ok= True)
      except:
        print("failed making path",outfolder)  
        continue
      try:        
        of=open(outpath,"w")
        of.write(txt)
        of.close()
      except:
        print("failed writing to path",outpath)    
        continue
      



def badfile(name):
  if "~" in name: return True 
  try:
    name.encode('ascii')
  except UnicodeEncodeError:
      return True  # string is not ascii 
  return False  

def smallfile(path):
  n=os.path.getsize(path)
  #print("n",n)
  if (n<1024):
    return True
  return False  

def find_start(txt):
  n=txt.find("<body ")
  if n<0: return 0
  return n

def find_end(txt):
  n=txt.find("<footer ")
  if n<0: return len(txt)
  return n


class HTMLFilter(HTMLParser):
  text = ""
  def handle_data(self, data):
    self.text += data



main()  
