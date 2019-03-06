import re
import pickle
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

class PositionalInvertedIndex:
    """Dictionary containing the collection of Terms and their positional posting lists"""

    def __init__(self, path2docs):
        self.path2docs = path2docs
        self.stopWords = []
        self.terms = []
        self.nbDocs = 0

    def __str__(self):
        str = "-"*80
        str += "\nPositional Inverted Index\nNumber of document : {}\n".format(self.nbDocs)
        str += "-"*80 + "\n"
        for term in self.terms:
            str += term.__str__() + "\n"
        return str

    def build(self):
        """Build the dictionary from the documents"""
        docs = self.__loadDocuments()

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
                    self.__addTerm(word, docID, pos)


        self.__updateDocumentFrequency()

        return stemmedDocs


    def __addTerm(self, word, docID, pos):
        """Write a word, it docID and it position in the dictionary"""
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
        """Count the number of document for each term"""
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
        """Return the positional posting list of a term, None if the term is not in the dictionary"""
        term = self.getTerm(word)
        if(term == None):
            return None
        return [occ.docID for occ in term.occurences]

    def getPostingListDistance(self, word1, word2, distance):
        """Return the positional posting list of the intersection of 2 words with a positional constrain"""
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
        """Return the Term object of a word"""
        for term in self.terms:
            if(term.word == word):
                # print("{}/{}".format(term.word, word))
                return term
        # print("not in term")
        return None

    def save(self, filePath):
        """Save the PositionalInvertedIndex in a pickle file and write a readable txt file"""
        with open(filePath, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        fileName = filePath.replace(".pickle", ".txt")
        with open(fileName, "w") as f2:
            f2.write(self.__str__())

    def getNbTerms(this):
        return len(this.terms)

    def setStopWords(self, stopWords):
        self.stopWords = stopWords



class Term:
    """Term in the dictionary, with its document frequency and the position in each document"""

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

    def add(self, docID, position):
        """add a occurence in a document given a position"""
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
        """return the occurences in a documents"""
        for occ in self.occurences:
            # print("---- {}/{}".format(occ.docID, docID))
            if(occ.docID == docID):
                return occ
        return None



class Occurence:
    """Positions of a term in a document and term frequency in this document"""

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

    def add(self, position):
        """add a occurence of the term in a document"""
        if(position not in self.positions):
            self.positions.append(position)
            self.positions.sort()
            self.termFreq += 1
