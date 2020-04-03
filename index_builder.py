import h5py
import numpy as np
from html_reader import html_reader,convert
from paper import paper
from cacm_downloader import data_loader

num = np.arange(1,3205)
def index():
    papers = [html_reader('cacm/CACM-%s.html'%convert(i)) for i in num]
    years = set()
    for item in papers:
        years.update((item.metadata[6],item.date[0]))
    years = list(years)
    index_year = {year:set() for year in years}
    for item in papers:
        index_year[item.date[0]].add(item.id)
        index_year[item.metadata[6]].add(item.id)
    for key in index_year:
        index_year[key] = np.sort(np.array(list(index_year[key])))

    year_file = h5py.File("year_index.h5",'w')
    for key in index_year:
        year_file.create_dataset(name=key,data=index_year[key])
    year_file.close()

    months = set()
    for item in papers:
        months.update((item.date[1],item.metadata[2]))
    months = list(months)
    index_month = {month:set() for month in months}
    for item in papers:
        index_month[item.date[1]].add(item.id)
        index_month[item.metadata[2]].add(item.id)
    for key in index_month:
        index_month[key] = np.sort(np.array(list(index_month[key])))

    month_file = h5py.File("month_index.h5",'w')
    for key in index_month:
        month_file.create_dataset(name = key, data=index_month[key])
    month_file.close()

    ids = set()
    for item in papers:
        ids.add(item.metadata[0])
    ids = list(ids)
    index_id = {id:set() for id in ids}
    for item in papers:
        index_id[item.metadata[0]].add(item.id)
    for key in index_id:
        index_id[key] = np.sort(np.array(list(index_id[key])))
    id_file = h5py.File("id_index.h5",'w')
    for key in index_id:
        id_file.create_dataset(name=key,data=index_id[key])
    id_file.close()

    sigs = set()
    for item in papers:
        sigs.add(item.metadata[1])
    sigs = list(sigs)
    index_sig = {sig:set() for sig in sigs}
    for item in papers:
        index_sig[item.metadata[1]].add(item.id)
    for key in index_sig:
        index_sig[key] = np.sort(np.array(list(index_sig[key])))
    sig_file = h5py.File("sig_index.h5","w")
    for key in index_sig:
        sig_file.create_dataset(name=key,data=index_sig[key])
    sig_file.close()

    times = set()
    for item in papers:
        times.add(item.metadata[4]+" "+item.metadata[5])
    times = list(times)
    index_time = {time:set() for time in times}
    for item in papers:
        index_time[item.metadata[4]+" "+item.metadata[5]].add(item.id)
    for key in index_time:
        index_time[key] = np.sort(np.array(list(index_time[key])))
    time_file = h5py.File("time_index.h5","w")
    for key in index_time:
        time_file.create_dataset(name=key,data=index_time[key])
    time_file.close()

    authors = set()
    for item in papers:
        authors.update(item.author)
    authors = list(authors)
    index_author = {author:set() for author in authors}
    for item in papers:
        for a in item.author:
            index_author[a].add(item.id)
    for key in index_author:
        index_author[key] = np.sort(np.array(list(index_author[key])))
    author_file = h5py.File("author_index.h5","w")
    for key in index_author:
        author_file.create_dataset(name=key,data=index_author[key])
    author_file.close()

    dates = set()
    for item in papers:
        dates.add(item.metadata[2]+" "+item.metadata[3])
    dates = list(dates)
    index_date = {date:set() for date in dates}
    for item in papers:
        index_date[item.metadata[2]+" "+item.metadata[3]].add(item.id)
    for key in index_date:
        index_date[key] = np.sort(np.array(list(index_date[key])))
    date_file = h5py.File("date_index.h5","w")
    for key in index_date:
        date_file.create_dataset(name=key,data=index_date[key])
    author_file.close()

    words = set()
    for item in papers:
        words.update(item.corpus)
    words = list(words)
    index_word = {word:set() for word in words}
    for item in papers:
        for word in item.corpus:
            index_word[word].add(item.id)
    for key in index_word:
        index_word[key] = np.sort(np.array(list(index_word[key])))
    word_file = h5py.File("word_index.h5","w")
    for key in index_word:
        word_file.create_dataset(name=key,data=index_word[key])
    word_file.close()

def buildindex():
    data_loader()
    index()
