import re
from bs4 import BeautifulSoup

class Occurence:
    """"""

    def __init__(self, docID, termFrequency=0, position=[]):
        self.docID = docID
        self.termFreq = termFrequency
        self.position = position

    def __str__(self):
        str = "[{}, {} : ".format(self.docID, self.termFreq)
        for pos in self.position:
            str += " {},".format(pos)
        str += "]"
        return str

    def __eq__(self, other):
        """To compare 2 Occurence object by their docID attribute"""
        return isinstance(other, Occurence) and self.docID == other.docID

    def __hash__(self):
        """Needed for __eq__()"""
        return hash(self.docID)

    def add(self, position):
        """"""
        position.append(position)
        position.sort()
        self.termFreq += 1

    def methodeToConvertToSaveableFormat(self):
        pass


class Term:
    """"""

    def __init__(self, word, docFrequency=0, occurences=[]):
        self.word = word
        self.docFreq = docFrequency
        self.occurences = occurences

    def __str__(self):
        str = "[{}, {}] -> {".format(self.word, self.docFreq)
        for occ in self.occurences:
            str += occ.__str__() + ", "
        str += "}"
        return str

    def __eq__(self, other):
        """To compare 2 Occurence object by their docID attribute"""
        return isinstance(other, Term) and self.word == other.word

    def __hash__(self):
        """Needed for __eq__()"""
        return hash(self.word)


    def getOccurence(self, docID):
        """"""
        for occ in self.occurences:
            if(occ.docID == docID):
                return occ
        return None

    def add(self, docID, position):
        """"""
        occurence = self.getOccurence(docID)
        if(occurence):
            occurence.add(position)
        else:
            occurence = Occurence(docID)
            occurence.add(position)
            self.occurences.append(occurence)
            self.docFreq += 1

class PositionalInvertedIndex:
    """"""

    def __init__(self, path2docs):
        self.path2docs = path2docs
        self.stopWords = []
        self.terms = []

    def build(self):
        docs = self.__loadDocuments()

    def __loadDocuments(self):
        """Load documents from a XML file. each document as to be between <doc></doc>"""
        docs = []
        with open(self.path2docs, "rt") as f:
            soup = BeautifulSoup(f, features="lxml")

        for doc in soup.find_all('doc'):
            docs.append(doc.get_text().split())

        return docs


    def loadDictionary(self, path2dic):
        pass

    def saveDictionary(self, path2dic):
        pass

    def setStopWords(self, stopWords):
        self.stopWords = stopWords
