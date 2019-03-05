import re
import math
from nltk.stem import PorterStemmer

class QueryManager:

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def process(self, query):
        """"""
        splited_query = self.__split_query(query)
        splited_query = self.__normalize_query(splited_query)
        splited_query = self.__stem_query(splited_query)

        print(splited_query)
        posting_lists = []
        for part in splited_query:
            if(len(part) > 1): #if distance information
                posting_lists.append(self.dictionary.getPostingListDistance(part[1], part[2], int(part[0])))
                print("\t{}({} {}) - \t Posting list: {}".format(
                        part[0],
                        part[1],
                        part[2],
                        self.dictionary.getPostingListDistance(part[1], part[2], int(part[0]))))
            else: #if single word
                posting_lists.append(self.dictionary.getPostingList(part[0]))
                print("\t{} - \t\t Posting list: {}".format(part[0], self.dictionary.getPostingList(part[0])))

        selected_docID = self.__merge_posting(posting_lists, "AND")
        # selected_docID = self.__merge_posting(posting_lists, "OR")

        query_terms = self.__get_query_terms(splited_query)

        scores = {}
        for docID in selected_docID:
            scores[docID] = self.__compute_score(docID, query_terms)

        return scores

    def __compute_score(self, docID, terms):
        """"""
        score = 0
        for word in terms:
            term = self.dictionary.getTerm(word)
            occurence = term.getOccurence(docID)
            tf = occurence.termFreq
            df = term.docFreq
            N = self.dictionary.nbDocs
            score += (1 + math.log10(tf)) * math.log10(N/df)

        return score

    def __merge_posting(self, lists, oper="AND"):
        """"""
        final_list = []
        if(oper == "OR"):
            for posting in lists:
                final_list = list(set(posting + final_list))
        elif(oper == "AND"):
            for idx, posting in enumerate(lists):
                if(idx == 0):
                    final_list = posting
                else:
                    final_tmp = []
                    for docID in final_list:
                        if(docID in posting):
                            final_tmp.append(docID)
                    final_list = final_tmp
        else:
            print("Error operation to merge posting lists not recognized.")
            return None

        return final_list

    def __get_query_terms(self, spltied_query):
        """"""
        terms = []
        for part in spltied_query:
            if(len(part) > 1):
                for i in range(1, 3):
                    if(part[i] not in terms):
                        terms.append(part[i])
            else:
                if(part[0] not in terms):
                    terms.append(part[0])
        return terms

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
