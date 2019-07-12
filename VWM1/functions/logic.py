from collections import defaultdict
import math

def getIdf(corpus):
    docs_count = len(corpus)
    idf = defaultdict(lambda :0)
    for doc in corpus:
        for word in doc.keys():
            idf[word] += 1

    for key in idf.keys():
        cnt = idf[key]
        idf[key] = math.log(docs_count/cnt)
    return idf


def calculateWeights(idf,doc):

    for word in doc:
        tmp = 1 + ((float(doc[word]) / float(len(doc))) * 100)
        # print(tmp)
        doc[word] = idf[word] * (math.log(tmp) + 1)

def buildSeq(idf,docs):
    termDict = defaultdict()
    for word in idf:
        termDict[word] = []

    i = 0
    count = len(idf)
    n=0
    prev = -1
    for key in idf:
        n+=1
        if int((n / count) * 100) % 5 == 0 and int((n / count) * 100) != prev:
            print("buduji seq...",int((n / count) * 100), "%")
            prev = int((n / count) * 100)
        # print(n,"z",len(idf), "\nmatice bude: ",len(idf),"*",len(docs),"=",len(idf)*len(docs))
        i=0
        for doc in docs:
            # if(i % 100) == 0:
            #     print("...",i)
            i += 1
            if(doc[key]):
                termDict[key].append([i,doc[key]])
            else:
                termDict[key].append([i,0])
    print("dobudoval jsem seq")
    return termDict

def invertedIndex(idf,docs):

    termDict = defaultdict()
    for word in idf:
        termDict[word] = []

    i = 0
    for doc in docs:
        i += 1
        for word in doc:
            termDict[word].append([i,doc[word]])

    # for word in termDict:
    #     for doc in docs:
    #         termDict[word].append(doc)


    return termDict

# def build_inverted_index(idf, corpus):
#     inverted_index = {}
#     for word, value in idf.items():
#         inverted_index[word] = {}
#         inverted_index[word]['idf'] = value
#         inverted_index[word]['postings_list'] = []
#
#     for index, doc in enumerate(corpus):
#         for word, value in doc.items():
#             inverted_index[word]['postings_list'].append([index, value])
#
#     return inverted_index