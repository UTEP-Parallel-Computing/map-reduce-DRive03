import pymp
import time
import threading
import re

def countInstances(document,word_list,wordCount): #this is an auxiliary function that helps count all the instances of the words
    f = open(document, 'r')#open the file in read mode
    for w in word_list: #find all the words in the list and add it to the count on the dictionary in lowercaps
        wordCount[w] += len(re.findall(w,f.read().lower()))
        f.seek(0)#return to the beginning of the file for the next word search

def findAllWords(documents,word_list):#this will be the parallel section of the program
    wordCount = pymp.shared.dict()#shared dictionary
    with pymp.Parallel(8) as pimp:
        for word in word_list:
            wordCount[word] = 0
        safe = pimp.lock#declaring the lock for the threads
        for d in pimp.iterate(documents):
            safe.acquire()
            countInstances(d, word_list, wordCount)#use the auxiliary function
            safe.release()
    print(wordCount)#at the end print the whole dictionary with the values




documents = ["shakespeare1.txt", "shakespeare2.txt", "shakespeare3.txt", "shakespeare4.txt",
             "shakespeare5.txt", "shakespeare6.txt", "shakespeare7.txt", "shakespeare8.txt"] # all the files to be read

word_list = ["hate", "love", "death", "night", "sleep", "time", "henry", "hamlet", # the words to look for
             "you", "my", "blood", "poison", "macbeth", "king", "heart", "honest"]




startTime = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
findAllWords(documents,word_list)
endTime = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
totalTime = endTime-startTime
print("Time for execution: %s", totalTime )