import os
from flask import Flask, render_template, request
from functions import fileManagement
from functions import logic
from collections import Counter
from collections import defaultdict
import time

app = Flask(__name__)

resource_folder = os.path.join(os.getcwd(), 'resources')
stopwords_file = os.path.join(resource_folder, 'eng_stop_words')
inverted_file = os.path.join(resource_folder, 'inverted_index')
sequence_file = os.path.join(resource_folder, 'sequence_matrix')
ids_file = os.path.join(resource_folder, 'document_ids')
stopwords = fileManagement.getWordsFromFile(stopwords_file)

test_path = os.path.join(os.getcwd(), 'database')
docs = []
IDs = defaultdict()

# getting raw files from wiki
print("build database from raw files from wiki ? ( 1 = yes )")
raw = input()
if (raw == "1"):
    print("type maximum size of your database (files count)")
    howmany = int(input())
    print(howmany)
    almost_full_pathIN = os.path.join(os.getcwd(), 'rawENwiki')
    almost_full_pathOUT = os.path.join(os.getcwd(), 'database')
    print("remove existing database ?")
    remov = input()
    if remov == "1":
        for file in os.listdir(almost_full_pathOUT):
            os.unlink(os.path.join(almost_full_pathOUT, file))
    for file in os.listdir(almost_full_pathIN):
        print("zpracovavam...")
        fileManagement.handleRaw(almost_full_pathIN, file, almost_full_pathOUT, howmany)
print("do you want to build new inverted index ? ( 1 = yes )")
newindex = input()
if (newindex == "1"):
    i = 0
    count = 0
    for file in os.listdir(test_path):
        count += 1
    prev = 0
    hei = 0
    for file in os.listdir(test_path):
        if int((i / count) * 100) % 5 == 0 and int((i / count) * 100) != prev:
            print("buduji index...", int((i / count) * 100), "%")
            prev = int((i / count) * 100)
        i += 1
        full_path = test_path + "/" + file
        wordsBag = fileManagement.getWordsFromFile(full_path)
        preprocessedBag = fileManagement.getCleanWords(wordsBag, stopwords)
        wordsWithCount = Counter(preprocessedBag)
        docs.append(wordsWithCount)
        IDs[i] = file

    idFile = open(ids_file, "w+")
    for index in IDs:
        line = str(index) + ";" + IDs[index] + "\n"
        idFile.write(line)

    idf = logic.getIdf(docs)

    for doc in docs:
        logic.calculateWeights(idf, doc)

    print("do you want to build new sequence matrix as well ? (1 = yes)")
    seqToo = input()
    if seqToo == "1":
        sequence = logic.buildSeq(idf, docs)
    inv = logic.invertedIndex(idf, docs)
    # and the index is done
    print("--------------------------inverted index done--------------------------\n")
    print("saving inverted index and sequence...\n")
    nko = 0
    for x in inv:
        if (nko == 20):
            break
        nko += 1
        # print(x)
        # print(inv[x])
    # saving the inverted index for later use
    invertFile = open(inverted_file, "w+")
    for word in inv:
        line = word + " "
        for index, value in inv[word]:
            line += str(index) + ";" + str(value) + " "
        line += "\n"
        invertFile.write(line)
        # print("zapsal jsem:", line)
    invertFile.close()

    if seqToo == "1":
        seqFile = open(sequence_file, "w+")
        for word in sequence:
            line = word + " "
            for index, value in sequence[word]:
                line += str(index) + ";" + str(value) + " "
            line += "\n"
            seqFile.write(line)
        seqFile.close()
print("do you want to use inverted index (1) or seqence (2) as method ?")
method = input()
inv = defaultdict()
print("loading from database...")
if method == "1":
    inv = fileManagement.getInv(inverted_file)
elif method == "2":
    inv = fileManagement.getInv(sequence_file)
else:
    print("you didnt input 1 or 2")
    exit(2)

idsFile = open(ids_file, "r")
for line in idsFile:
    lineArr = line.split(";")
    IDs[int(lineArr[0])] = lineArr[1]


# print("nowinv:\n")
# nko = 0
# for x in inv:
#     if (nko == 20):
#         break
#     nko += 1
#     print(x)
#     print(inv[x])


def stringToQuery(query):
    finalarr = []
    weights = []
    arr = query.split()
    n = 0
    prevWord = ""
    for word in arr:
        # print(word,n)
        if (n % 2 == 0):
            finalarr.append(word)
            prevWord = word
        else:
            INTword = float(word)
            weights.append(INTword)
        n += 1
    finalarr = fileManagement.getCleanWords(finalarr, stopwords)
    return finalarr, weights


def prepareQuery(query, weights):
    both = []
    i = 0
    for w in query:
        both.append([w, weights[i]])
        i += 1
    finalarrCount = Counter()
    for a, b in both:
        finalarrCount[a] = b
    # print(finalarrCount)
    return finalarrCount


def handleQuery(query):
    results = Counter()
    # print(query)
    # print(inv)

    for word, weight in query.items():
        if word in inv.keys():
            # print("youhoo")
            # print(word,weight)
            for index, value in inv[word]:
                # print(index,value)
                tmp = value * weight
                # print("tmp=",value,weight)
                results[index] += tmp
    results.most_common(10)
    almostResults = Counter()
    almostResults = results.most_common(10)
    # print(almostResults)
    fileRes = []
    fileValues = []
    for index, value in almostResults:
        # print("appending...", index)
        fileRes.append([IDs[index],value])
        # fileValues.append(value)
    return fileRes, fileValues


def getArr(name):
    arr = fileManagement.fileToArr(test_path + '/' + name)
    return arr


@app.route('/test', methods=['GET', 'POST'])
def test():
    # return 'Hello There!'
    return render_template('main.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    res = []
    vals = []
    t = 0.0
    if (request.values.get('fname') != None):
        queryArr, weights = stringToQuery(request.values.get('fname'))
        query = prepareQuery(queryArr, weights)
        start = time.time()
        res, vals = handleQuery(query)
        end = time.time()
        t = (end - start) * 1000.0
        print("elapsed search time:", t)
    # print( res)
    return render_template('main.html', data=inv, test=request.values.get('fname'), res=res,vals=vals, time=t)
    # return 'Hello There!'


@app.route('/files/<name>')
def hello_name(name):
    arr = getArr(name)
    # startchange
    queryArr = fileManagement.buildQuery(test_path + '/' + name)
    weights = []
    for word in queryArr:
        weights.append(1)
    query = prepareQuery(queryArr, weights)
    # print(query)
    start = time.time()
    res, vals = handleQuery(query)
    end = time.time()
    t = (end - start) * 1000.0
    print("full document elapsed search time:", t)
    # print("result:",res)

    # endchange
    return render_template('file.html', name=name, arr=arr, res=res)
    # return 'Hello %s!' % name


if __name__ == '__main__':
    app.run()

    #
    # {% for item in data %}
    #     <p> {{ item }} </p>
    # {% endfor %}

    # git push master-origin
