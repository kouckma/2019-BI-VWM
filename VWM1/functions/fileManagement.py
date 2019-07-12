from functions import porter
from collections import defaultdict
from collections import Counter

def getWordsFromFile(file):
    words = []
    with open(file, mode='r') as f:
        words = (f.read().split())
    return words


def fileToArr(file):
    # arr = []
    with open(file, mode='r') as f:
        # arr.append(f.read())
        words = [(f.read())]
    return words


def handleRaw(inFolder, file, outFolder,max):
    # print(file)
    f = open(inFolder + '/' + file, mode='r')
    title = ""
    n = 0
    filesC = 0
    # currFile = open("txt", "w+")
    for x in f:
        # print("zpracovavam", n)
        if x.startswith("<d"):
            arr = x.split()
            title = arr[2].lstrip("title=")
            i = 3
            while (not title.endswith("\"")):
                title += " " + arr[i]
                i += 1
            # print(title)
            title = title.replace("/", "-")
            title = title.replace("?", "-")
            # print(title)
            currFile = open(outFolder + "/" + title, "w+")
        elif x.startswith("</"):
            currFile.close()
            filesC +=1
            # print("zapsano do", currFile)
        else:
            currFile.write(x)
        n += 1
        if(filesC>=max):
            break
    # this may cause problems
    f.close()
        # arr.append(f.read())
        # words = [(f.read())]
    # return words

def getInv(inverted_file):
    inv = defaultdict()
    invertFile = open(inverted_file, "r")
    for line in invertFile:
        lineArr = line.split()
        inv[lineArr[0]] = []
        first = 1
        for d in lineArr:
            if first == 1:
                first = 0
            else:
                dArr = d.split(";")
                inv[lineArr[0]].append([int(dArr[0]), float(dArr[1])])
    invertFile.close()
    return inv

def removeStopWords(inDoc, inStop):
    usefullWords = []

    for word in inDoc:
        if word not in inStop:
            usefullWords.append(word)

    return usefullWords


def usePorterStemmer(dataset):
    p = porter.PorterStemmer()

    clean_dataset = []
    for word in dataset:
        word.lower()
        clean_dataset.append(p.stem(word, 0, len(word) - 1))

    return clean_dataset

def buildQuery(file):
    f = open(file, mode='r')
    # print("\n\nBUILDQUERY\n\n")
    arr = []
    for line in f:
        arr += line.split()
        # for word in line:
        #     print(word," 42 ")
    f.close()
    return arr

    #
    # word = ""
    # output = set()
    # for c in f:
    #     if c.isalpha():
    #         word += c.lower()
    #     else:
    #         if word:
    #             output += p.stem(word, 0, len(word) - 1)
    #             word = ''
    #         output += c.lower()
    # print(output)


def getCleanWords(inDoc, inStop):
    # print("preprocessing document...")
    # potentially remove NonWords function needed ?
    dataset = removeStopWords(inDoc, inStop)
    dataset = usePorterStemmer(dataset)

    return dataset
