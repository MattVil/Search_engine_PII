from dictionary import PositionalInvertedIndex

PATH_TO_DOCUMENTS = "./data/documents.txt"
STOP_WORDS = ['', 'the', 'is', 'at', 'of', 'on', 'and', 'a']

def main():

    dictionary = PositionalInvertedIndex(PATH_TO_DOCUMENTS)
    dictionary.setStopWords(STOP_WORDS)

    docs = dictionary.build()

    for doc in docs:
        print(doc)

if __name__ == '__main__':
    main()