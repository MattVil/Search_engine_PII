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
    print("\nnexus like love happy")
    print(queryManager.process("nexus like love happy"))
    print("\nasus repair")
    print(queryManager.process("asus repair"))
    print("\n0(touch screen) fix repair")
    print(queryManager.process("0(touch screen) fix repair"))
    print("\n1(great tablet) 2(tablet fast)")
    print(queryManager.process("1(great tablet) 2(tablet fast)"))
    print("\ntablet")
    print(queryManager.process("tablet"))

if __name__ == '__main__':
    main()
