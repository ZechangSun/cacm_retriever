import re
import h5py
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from os.path import join,exists
from os import listdir
from paper import paper

def html_reader(input_dir):
    """
    read the html file at input_dir, and parse the html file, return a paper object
    -------------------------------------------------------------------------------
    parameter:
    input_dir: str, dir of the html file
    ------------------------------------------------------------------------------
    return:
    paper: paper.paper object
    """
    #read data from the html file
    with open(input_dir,'r') as html_file:
        content = html_file.read()
    content = (content.split('\n'))[4:-4]
    num = re.compile("(.*\t\d.*)|(\d*\d\.\d*)")
    information = []
    for i in range(len(content)):
        if num.match(content[i])==None:
            information.append(content[i])
    information = information[:-1]
    #data parsing
    Date = re.compile('( ?CACM|June)')
    Meta = re.compile("(CA\d\d\d\d\d\d|June)")
    #get date and meta index
    for i in range(len(information)):
        if Date.match(information[i])!=None:
            index_date = i
        if Meta.match(information[i])!=None:
            index_meta =i
    content = information[:index_date]
    others = information[index_date+2:index_meta]
    for i in range(len(content)):
        if content[i]=="":
            title = content[:i]
            abstract = content[i+1:]
            break
    #get author and other
    author = []
    other = []
    for i in range(len(others)):
        if others[i]=="":
            if re.match("[A-Z].*, ?[A-Z].*\..*",others[0]) != None:
                author = others[:i]
                other = others[i+1:]
            else:
                other = others
            break
    for i in range(len(author)):
        if re.match("[A-Z].*, ?[A-Z].*\..*",author[i]) != None:
            name = author[i].split(",")
            author[i] = (name[1]+name[0])
            author[i] = author[i].replace(" ","")
            author[i] = author[i].replace("\t","")
            author[i] = author[i].lower()

    #parse date
    date = []
    date.append(re.search("19\d\d", information[index_date]).group())
    date.append(re.search("(January|February|March|April|May|June|JUly|July|August|September|October|November|December)",information[index_date]).group().lower())

    #parse meta data
    meta = []
    meta.append(re.search("CA\d\d\d\d\d\d\w?",information[index_meta]).group().lower())#0
    meta.append(re.search("[a-z0-9] [A-Z]{2}[A-Z]?",information[index_meta]).group()[2:].lower())#1
    meta.append(re.search("(January|February|March|April|May|June|JUly|July|August|September|October|November|December)",information[index_meta]).group().lower())#2
    meta.append(re.search("\w \d\d?",information[index_meta]).group()[2:])#3
    meta.append(re.search("\d?\d:\d\d",information[index_meta]).group())#4
    meta.append(re.search("(AM|PM)",information[index_meta]).group().lower())#5
    meta.append(re.search("19\d\d",information[index_meta]).group())#6

    #build corpus
    corpus = set()
    lemmatizer = WordNetLemmatizer()
    for i in range(len(title)):
        title[i] = re.sub("\(|\)|-|\d\d?\d?|:|/|\.|`|\?"," ",title[i])
        words = word_tokenize(title[i])
        for word in words:
            normal_word = word.lower()
            if normal_word not in stopwords.words("english"):
                corpus.add(lemmatizer.lemmatize(normal_word))

    for i in range(len(abstract)):
        abstract[i] = re.sub("\(|\)|-|\d\d?\d?|:|/|\.|`|\?|,"," ",abstract[i])
        words = word_tokenize(abstract[i])
        for word in words:
            normal_word = word.lower()
            if normal_word not in stopwords.words("english"):
                corpus.add(lemmatizer.lemmatize(normal_word))

    for i in range(len(other)):
        other[i] = re.sub("\(|\)|-|\d\d?\d?|:|/|\.|`|\?|,"," ",other[i])
        words = word_tokenize(other[i])
        for word in words:
            normal_word = word.lower()
            if normal_word not in stopwords.words("english"):
                corpus.add(lemmatizer.lemmatize(normal_word))

    corpus = list(corpus)

    return  paper(author= author, other= other, metadata= meta,date = date,title = title,abstract = abstract,id=int(input_dir[-9:-5]),corpus = corpus)

def convert(num):
    """
    format the number like "0001","0012","0123","1234"
    -------------------------------------------------------------------------
    parameter:
    num: int, the number to be formatted
    -------------------------------------------------------------------------
    return:
    num:str, the formatted number
    """
    if len(str(num))==1:
        return "000%i"%num
    elif len(str(num)) == 2:
        return "00%i"%num
    elif len(str(num)) == 3:
        return "0%i"%num
    elif len(str(num)) == 4:
        return "%i"%num
