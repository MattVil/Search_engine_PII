import re

class QueryManager:

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def process(self, query):
        """"""
        splited_query = self.__split_query(query)


        return splited_query

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
                result.append(query_part)
        return result
