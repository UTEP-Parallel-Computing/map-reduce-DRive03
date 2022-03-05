# import pymp
import time
import re
from mpi4py import MPI


# import collections

def countInstances(document, word_list,
                   wordCount):  # this is an auxiliary function that helps count all the instances of the words
    f = open(document, 'r')  # open the file in read mode
    for w in word_list:  # find all the words in the list and add it to the count on the dictionary in lowercaps
        wordCount[w] += len(re.findall(w, f.read().lower()))
        f.seek(0)  # return to the beginning of the file for the next word search


def findAllWords(documents, word_list):  # this will be the parallel section of the program
    rank = comm.Get_rank()  # get our rank (process #)

    if rank == 0:
        wordCount = {}
        for word in word_list:
            wordCount[word] = 0  # Creating the dictionary for all the threads
        if threads >= 2:  # if we have more than one thread it'll send all the data to the other threads
            for i in range(1, threads):
                comm.send(wordCount, dest=i, )
    else:
        wordCount = {}
        wordCount = comm.recv(source=0, )  # tag=<tag#>

    docs = len(documents)  # number of docs 8
    perThread = int(docs / threads)  # docs per thread
    current = perThread * rank  # current index for the document list
    limit = int(perThread * (rank + 1))  # limit of the part assigned to this thread

    for d in range(current,
                   limit):  # each thread gets a certain number of docs depending of the number of threads
        countInstances(documents[d], word_list, wordCount)  # use the auxiliary function

    if rank != 0:  # all the other threads are sending their count to thread 0
        comm.send(wordCount, dest=0, )

    if rank == 0:  # we gather all the counts from all the dictionary parts into one
        result = wordCount
        if threads >= 2:
            for i in range(1, threads):
                data = comm.recv(source=i, )
                for k, v in data.items():
                    if k not in result:
                        result[k] = v
                    else:
                        result[k] += v

        return result

    # return wordCount#at the end return the whole dictionary with the values


documents = ["shakespeare1.txt", "shakespeare2.txt", "shakespeare3.txt", "shakespeare4.txt",
             "shakespeare5.txt", "shakespeare6.txt", "shakespeare7.txt", "shakespeare8.txt"]  # all the files to be read

word_list = ["hate", "love", "death", "night", "sleep", "time", "henry", "hamlet",  # the words to look for
             "you", "my", "blood", "poison", "macbeth", "king", "heart", "honest"]

# get the world communicator
comm = MPI.COMM_WORLD

# get the size of the communicator in # processes
threads = comm.Get_size()

rank = comm.Get_rank()  # get our rank (process #)

startTime = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
dictionary = findAllWords(documents, word_list)
endTime = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)

if rank == 0:
    print(dictionary)
    totalTime = endTime - startTime
    print("Time for execution: %s", totalTime)
