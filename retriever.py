import re
import h5py
from nltk.stem import WordNetLemmatizer

def get_index(word):
    """
    get the index of the given word
    -----------------------------------
    parameter:
    word:str, the word to be retrieved
    ----------------------------------
    return:
    index:np.array, the index of the given word
    """
    dir = ""
    if re.match("19\d\d",word)!=None:
        dir = "year_index.h5"
    elif re.match("(January|February|March|April|May|June|JUly|July|August|September|October|November|December)",word,re.I)!=None:
        dir = "month_index.h5"
    elif re.match(".*\..*\w",word,re.I)!=None:
        dir = "author_index.h5"
    elif re.match("[A-Z]{2}[A-Z]?$",word,re.I)!=None:
        dir = "sig_index.h5"
    elif re.match("CA\d\d\d\d\d\d\w?",word,re.I)!=None:
        dir = "id_index.h5"
    elif re.match("\d\d?:\d\d (PM|AM)",word,re.I)!=None:
        dir = "time_index.h5"
    elif re.match("(January|February|March|April|May|June|JUly|July|August|September|October|November|December) \d\d?",word,re.I)!=None:
        dir = "date_index.h5"
    else:
        dir = "word_index.h5"

    assert dir!="", "No such word!"

    file = h5py.File(dir,'r')
    if dir!="word_index.h5":
        index = file[word.lower()][:]
    else:
        stem = WordNetLemmatizer()
        index = file[stem.lemmatize(word.lower())][:]
    file.close()

    return index

def compare_without_skip_pointer(index1,index2):
    iter1=iter2=0
    ans = []
    while iter1!=len(index1) and iter2 != len(index2):
        if index1[iter1]>index2[iter2]:
            iter2 += 1
        elif index1[iter1]<index2[iter2]:
            iter1 += 1
        elif index1[iter1] == index2[iter2]:
            ans.append(index1[iter1])
            iter1 += 1
            iter2 += 1
    return ans

def compare_with_skip_pointer(index1,index2,step = 8):
    def hasSkip(i,index):
        if i+step<len(index):
            return True
        else:
            return False
    ans = []
    iter1 = iter2 = 0
    while iter1!=len(index1) and iter2 != len(index2):
        if index1[iter1]==index2[iter2]:
            ans.append(index1[iter1])
            iter1 += 1
            iter2 += 1
        elif index1[iter1]>index2[iter2]:
            if hasSkip(iter2,index2):
                iter2 += step if index2[iter2+step]<=index1[iter1] else 1
            else:
                iter2 += 1
        elif index1[iter1]<index2[iter2]:
            if hasSkip(iter1,index1):
                iter1 += step if index1[iter1+step]<=index2[iter2] else 1
            else:
                iter1 += 1
    return ans

def retrieve(*words, step = None):
    indexs = []
    for item in words:
        indexs.append(get_index(item))
    indexs.sort(key=len)
    assert indexs!=[], "No such word!"
    ans = indexs[0]
    if step==None:
        for index in indexs[1:]:
            ans = compare_without_skip_pointer(ans,index)
    else:
        for index in indexs[1:]:
            ans = compare_with_skip_pointer(ans,index,step)
    return ans

