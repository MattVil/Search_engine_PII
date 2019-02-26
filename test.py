from dictionary import PositionalInvertedIndex
from query import QueryManager

PATH_TO_DOCUMENTS = "./data/documents.txt"
STOP_WORDS = ['', 'the', 'is', 'at', 'of', 'on', 'and', 'a']

def main():

    dictionary = PositionalInvertedIndex(PATH_TO_DOCUMENTS)
    dictionary.setStopWords(STOP_WORDS)

    docs = dictionary.build()

    print(dictionary.__str__())
    print("Nb word in dictionary : {}".format(dictionary.getNbTerms()))

    queryManager = QueryManager(dictionary)
    print(queryManager.process("1(fat thing) show 7(berkeley SFSU)"))

if __name__ == '__main__':
    main()
