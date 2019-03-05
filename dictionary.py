import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

class PositionalInvertedIndex:
    """"""

    def __init__(self, path2docs):
        self.path2docs = path2docs
        self.stopWords = []
        self.terms = []
        self.nbDocs = 0

    def __str__(self):
        str = ""
        for term in self.terms:
            str += term.__str__() + "\n"
        return str

    def build(self):
        """"""
        docs = self.__loadDocuments()
        # docs = [["la","vie","est", "belles", "vraiment", "belle"], ["c'est","avant", "tout", "des", "rencontres"], ["les", "rencontres", "qui", "forme", "la", "vie"]]

        self.nbDocs = len(docs)

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

    def getPostingList(self, word):
        """"""
        term = self.getTerm(word)
        if(term == None):
            return None
        return [occ.docID for occ in term.occurences]

    def getPostingListDistance(self, word1, word2, distance):
        """"""
        term1 = self.getTerm(word1)
        term2 = self.getTerm(word2)

        t1_posting = [occ for occ in term1.occurences]
        t2_posting = [occ for occ in term2.occurences]

        if(term1 == None or term2 == None):
            return None

        result = []
        idx_t1, idx_t2 = 0, 0
        while(idx_t1 < len(t1_posting) and idx_t2 < len(t2_posting)):
            if(t1_posting[idx_t1].docID == t2_posting[idx_t2].docID):
                idx_pt1, idx_pt2 = 0, 0
                t1_pos = t1_posting[idx_t1].positions
                t2_pos = t2_posting[idx_t2].positions
                while(idx_pt1 < len(t1_pos) and idx_t2 < len(t2_pos)):
                    if(abs(t1_pos[idx_pt1] - t2_pos[idx_pt2])-1 <= distance):
                        if(t1_posting[idx_t1].docID not in result):
                            result.append(t1_posting[idx_t1].docID)
                        idx_pt1 += 1
                        idx_pt2 += 1
                    else:
                        if(t1_pos[idx_pt1] < t2_pos[idx_pt2]):
                            idx_pt1 += 1
                        else:
                            idx_pt2 += 1
                idx_t1 += 1
                idx_t2 += 1
            else:
                if(t1_posting[idx_t1].docID < t2_posting[idx_t2].docID):
                    idx_t1 += 1
                else:
                    idx_t2 += 1

        return result


    def getTerm(self, word):
        for term in self.terms:
            if(term.word == word):
                # print("{}/{}".format(term.word, word))
                return term
        # print("not in term")
        return None

    def loadDictionary(self, path2dic):
        pass

    def saveDictionary(self, path2dic):
        pass

    def getNbTerms(this):
        return len(this.terms)

    def setStopWords(self, stopWords):
        self.stopWords = stopWords



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
