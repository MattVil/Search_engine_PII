import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

class Occurence:
    """"""

    def __init__(self, docID):
        self.docID = docID
        self.termFreq = 0
        self.positions = []

    def __str__(self):
        str = "[{}, {} : ".format(self.docID, self.termFreq)
        for pos in self.positions:
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
        if(position not in self.positions):
            self.positions.append(position)
            self.positions.sort()
            self.termFreq += 1

    def methodeToConvertToSaveableFormat(self):
        pass


class Term:
    """"""

    def __init__(self, word):
        self.word = word
        self.docFreq = 1
        self.occurences = []

    def __str__(self):
        str = "[{}, {}] -> (".format(self.word, self.docFreq)
        for occ in self.occurences:
            str += occ.__str__() + ", "
        str += ")"
        return str

    def __eq__(self, other):
        """To compare 2 Occurence object by their docID attribute"""
        return isinstance(other, Term) and self.word == other.word

    def __hash__(self):
        """Needed for __eq__()"""
        return hash(self.word)

    def add(self, docID, position):
        """"""
        occurence = self.getOccurence(docID)
        if(occurence):
            # print("\treuse past occ")
            occurence.add(position)
        else:
            # print("\tcreate new occ")
            newOccurence = Occurence(docID)
            newOccurence.add(position)
            self.occurences.append(newOccurence)

    def getOccurence(self, docID):
        """"""
        for occ in self.occurences:
            # print("---- {}/{}".format(occ.docID, docID))
            if(occ.docID == docID):
                return occ
        return None

class PositionalInvertedIndex:
    """"""

    def __init__(self, path2docs):
        self.path2docs = path2docs
        self.stopWords = []
        self.terms = []

    def __str__(self):
        str = ""
        for term in self.terms:
            str += term.__str__() + "\n"
        return str

    def build(self):
        """"""
        docs = self.__loadDocuments()
        # docs = [["la","vie","est", "belles", "vraiment", "belle"], ["c'est","avant", "tout", "des", "rencontres"], ["les", "rencontres", "qui", "forme", "la", "vie"]]

        normalizedDocs = []
        for doc in docs:
            normalizedDocs.append(self.__normalization(doc))

        stemmedDocs = []
        for doc in normalizedDocs:
            stemmedDocs.append(self.__stemming(doc))

        for docID, doc in enumerate(stemmedDocs):
            for pos, word in enumerate(doc):
                if(word not in self.stopWords):
                    self.addTerm(word, docID, pos)


        self.__updateDocumentFrequency()

        return stemmedDocs


    def addTerm(self, word, docID, pos):
        """"""
        term = self.getTerm(word)
        if(term):
            term.add(docID, pos)
            # print("modif term : " + term.__str__())
        else:
            newTerm = Term(word)
            newTerm.add(docID, pos)
            self.terms.append(newTerm)
            # print("new term : " + newTerm.__str__())



    def __stemming(self, doc):
        """Do a morphologic tranformation on a document"""
        stemmedDoc = []
        pstemmer = PorterStemmer()
        for word in doc:
            stemmedDoc.append(pstemmer.stem(word))
        return stemmedDoc

    def __normalization(self, doc):
        """Normalize words using lower case and only alpha-numeric character"""
        normalizedDoc = []
        for word in doc:
            word = word.lower()
            word = re.sub('[^a-zA-Z0-9]', '', word)
            normalizedDoc.append(word)

        return normalizedDoc

    def __updateDocumentFrequency(self):
        """"""
        for term in self.terms:
            term.docFreq = len(term.occurences)

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

    def getTerm(self, word):
        for term in self.terms:
            if(term.word == word):
                # print("{}/{}".format(term.word, word))
                return term
        # print("not in term")
        return None

    def getNbTerms(this):
        return len(this.terms)

    def setStopWords(self, stopWords):
        self.stopWords = stopWords
