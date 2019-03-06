import pickle
import timeit
import argparse
from dictionary import PositionalInvertedIndex
from query import QueryManager

PATH_TO_DOCUMENTS = "./data/documents.txt"
PATH_TO_DICTIONARY = "./dictionary/dictionary.pickle"
STOP_WORDS = ['', 'the', 'is', 'at', 'of', 'on', 'and', 'a']

def loadDictionary(path2dic):
    with open(path2dic, "rb") as f:
        return pickle.load(f)
    return None

def printResult(result):
    print("\n" + "#"*31)
    print("#" + " "*7 + "RESULTING DOCID"+ " "*7 + "#")
    print("#"*31 + "\n")
    count = 1
    while(result):
        maxKey = max(result, key=result.get)
        print("#{}\tdocID: {}\ttf-idf score: {}".format(count, maxKey, result[maxKey]))
        del result[maxKey]
        count += 1

def main():

    parser = argparse.ArgumentParser(description='Inverted index to search in documents.txt file.')
    parser.add_argument('query', type=str, help='Query to be process.')
    parser.add_argument('-b', '--build', action="store_true", help='Build the dictionary.')
    parser.add_argument('-s', '--save', action="store_true", help='Save the dictionary in the given file SAVE.')
    parser.add_argument('-t', '--time', action="store_true", help='Print execution time.')
    args = parser.parse_args()


    startB = timeit.default_timer()
    if(args.build):
        print("\nBuilding dictionary ...", end=' ')
        dictionary = PositionalInvertedIndex(PATH_TO_DOCUMENTS)
        dictionary.setStopWords(STOP_WORDS)
        docs = dictionary.build()
        print("Done.")
    else:
        print("\nLoading dictionary ...", end=' ')
        dictionary = loadDictionary(PATH_TO_DICTIONARY)
        print("Done.")
    stopB = timeit.default_timer()

    if(args.save):
        startS = timeit.default_timer()
        print("Saving ...", end=' ')
        dictionary.save(PATH_TO_DICTIONARY)
        print("Done.")
        stopS = timeit.default_timer()

    print()

    queryManager = QueryManager(dictionary)

    start = timeit.default_timer()
    result = queryManager.process(args.query)
    stop = timeit.default_timer()

    printResult(result)

    if(args.time):
        print("\nExecution time to load (or build) the dictionary: {:.3f}ms".format((stopB-startB)*1000))
        if(args.save):
            print("Execution time to save the dictionary: {:.3f}ms".format((stopS-startS)*1000))
        print("Execution time for the request: {:.3f}ms".format((stop-start)*1000))


if __name__ == '__main__':
    main()
