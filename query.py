import re
from nltk.stem import PorterStemmer

class QueryManager:

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def process(self, query):
        """"""
        splited_query = self.__split_query(query)
        splited_query = self.__normalize_query(splited_query)
        splited_query = self.__stem_query(splited_query)

        posting_lists = []
        for part in splited_query:
            if(len(part) > 1):
                posting_lists.append(self.dictionary.getPostingListDistance(part[1], part[2], int(part[0])))
                print("\t{}({} {}) - \t Posting list: {}".format(
                        part[0],
                        part[1],
                        part[2],
                        self.dictionary.getPostingListDistance(part[1], part[2], int(part[0]))))
            else:
                posting_lists.append(self.dictionary.getPostingList(part[0]))
                print("\t{} - \t\t Posting list: {}".format(part[0], self.dictionary.getPostingList(part[0])))


        return splited_query

    def __stem_query(self, query_array):
        """Do a morphologic tranformation on a query array"""
        pstemmer = PorterStemmer()
        stemmed_query = []
        for part in query_array:
            tmp_part = []
            for word in part:
                tmp_part.append(pstemmer.stem(word))
            stemmed_query.append(tmp_part)
        return stemmed_query

    def __normalize_query(self, query_array):
        """Normalize words using lower case and only alpha-numeric character"""
        normalized_query = []
        for part in query_array:
            tmp_part = []
            for word in part:
                word = word.lower()
                word = re.sub('[^a-zA-Z0-9]', '', word)
                tmp_part.append(word)
            normalized_query.append(tmp_part)
        return normalized_query

    def __split_query(self, query, separator=" ",lparen="(",rparen=")"):
        """"""
        nb_brackets=0
        query = query.strip(separator)

        l=[0]
        for i,c in enumerate(query):
            if c==lparen:
                nb_brackets+=1
            elif c==rparen:
                nb_brackets-=1
            elif c==separator and nb_brackets==0:
                l.append(i)
            if nb_brackets<0:
                raise Exception("Syntax error")

        l.append(len(query))
        if nb_brackets>0:
            raise Exception("Syntax error")

        splited_query = [query[i:j].strip(separator) for i,j in zip(l,l[1:])]
        result = []
        for query_part in splited_query:
            if("(" in query_part):
                r1 = re.compile("(.*?)\s*\((.*?)\)")
                m1 = r1.match(query_part)
                m2 = query_part[query_part.find("(")+1:query_part.find(")")]
                m2 = m2.split(" ")
                m3 = m2[0]
                m4 = m2[1]
                result.append([m1.group(1), m3, m4])
            else:
                result.append([query_part])
        return result
