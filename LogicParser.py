#Taken from https://github.com/pyparsing/pyparsing/blob/master/examples/searchparser.py
#Add license where needed

from pyparsing import *

class SearchQueryParser:

    def __init__(self):
        self._methods = {
            'and': self.evaluateAnd,
            'or': self.evaluateOr,
            'not': self.evaluateNot,
            'parenthesis': self.evaluateParenthesis,
            'quotes': self.evaluateQuotes,
            'word': self.evaluateWord
        }
        self._parser = self.parser()

    def parser(self):
        """
        This function returns a parser.
        The grammar should be like most full text search engines (Google, Tsearch, Lucene).
        Grammar:
        - a query consists of alphanumeric words, with an optional '*' wildcard
          at the end of a word
        - a sequence of words between quotes is a literal string
        - words can be used together by using operators ('and' or 'or')
        - words with operators can be grouped with parenthesis
        - a word or group of words can be preceded by a 'not' operator
        - the 'and' operator precedes an 'or' operator
        - if an operator is missing, use an 'and' operator
        """
        operatorOr = Forward()

        operatorWord = Group(Word(alphanums)).setResultsName('word')

        operatorQuotesContent = Forward()
        operatorQuotesContent << (
            (operatorWord + operatorQuotesContent) | operatorWord
        )

        operatorQuotes = Group(
            Suppress('"') + operatorQuotesContent + Suppress('"')
        ).setResultsName("quotes") | operatorWord

        operatorParenthesis = Group(
            (Suppress("(") + operatorOr + Suppress(")"))
        ).setResultsName("parenthesis") | operatorQuotes

        operatorNot = Forward()
        operatorNot << (Group(
            Suppress(Keyword("not", caseless=True)) + operatorNot
        ).setResultsName("not") | operatorParenthesis)

        operatorAnd = Forward()
        operatorAnd << (Group(
            operatorNot + Suppress(Keyword("and", caseless=True)) + operatorAnd
        ).setResultsName("and") | Group(
            operatorNot + OneOrMore(~oneOf("and or") + operatorAnd)
        ).setResultsName("and") | operatorNot)

        operatorOr << (Group(
            operatorAnd + Suppress(Keyword("or", caseless=True)) + operatorOr
        ).setResultsName("or") | operatorAnd)

        return operatorOr.parseString

    def evaluateAnd(self, argument):
        self.evaluate(argument[0])
        self.evaluate(argument[1])
        return

    def evaluateOr(self, argument):
        return self.evaluate(argument[0]).union(self.evaluate(argument[1]))

    def evaluateNot(self, argument):
        return self.GetNot(self.evaluate(argument[0]))

    def evaluateParenthesis(self, argument):
        return self.evaluate(argument[0])

    def evaluateQuotes(self, argument):
        """Evaluate quoted strings
        First is does an 'and' on the indidual search terms, then it asks the
        function GetQuoted to only return the subset of ID's that contain the
        literal string.
        """
        r = set()
        search_terms = []
        for item in argument:
            search_terms.append(item[0])
            if len(r) == 0:
                r = self.evaluate(item)
            else:
                r = r.intersection(self.evaluate(item))
        return self.GetQuotes(' '.join(search_terms), r)

    def evaluateDescriptor(self, argument):
        return self.GetDescriptor(argument[0])

    def evaluate(self, argument):
        methods = self._methods[argument.getName()]
        return methods(argument)

    def Parse(self, query):
        #print self._parser(query)[0]
        parsedQuery = self._parser(query)[0]
        return self.evaluate(parsedQuery)

    def GetDescriptor(self, word):
        return None

    def GetQuotes(self, search_string, tmp_result):
        return None

    def GetNot(self, not_set):
        return set().difference(not_set)


class ParserTest(SearchQueryParser):
    """Tests the parser with some search queries
    tests containts a dictionary with tests and expected results.
    Actual logic looks like s1 = 4. Where s1 corresponds to a question and 4 corresponds to code.
    """
    tests = {
        'men or women': 15,
        'gender is men or women and age is 21-25 and favouriteColour is red': 3
        'gender is men or women and age is 21-25 and favouriteColour is green': 3
        'gender is men or women and age is 21-25 and favouriteColour is blue': 1
    }

    banners = {
        'man': {
            'question': 'gender',
            'count': 7
        },
        'woman': {
            'question': 'gender',
            'count': 8
        },
        '21-25': {
            'question': 'age',
            'count': 7
        },
        '26-30': {
            'question': 'age',
            'count': 3
        },
        '31-35': {
            'question': 'age',
            'count': 5
        },
        'red': {
            'question': 'favouriteColour',
            'count': 8
        },
        'green': {
            'question': 'favouriteColour',
            'count': 4
        },
        'blue': {
            'question': 'favouriteColour',
            'count': 3
        }
    }

    questions = ['gender', 'age', 'favouriteColour']

    def GetDescriptor(self, descriptor):
        return self.demographics[descriptor]

    def GetQuotes(self, search_string, tmp_result):
        result = set()
        for item in tmp_result:
            if self.docs[item].count(search_string):
                result.add(item)
        return result

    def GetNot(self, not_set):
        all = set(list(self.docs.keys()))
        return all.difference(not_set)

    def Test(self):
        all_ok = True
        for item in list(self.tests.keys()):
            print(item)
            r = self.Parse(item)
            e = self.tests[item]
            print('Result: %s' % r)
            print('Expect: %s' % e)
            if e == r:
                print('Test OK')
            else:
                all_ok = False
                print('>>>>>>>>>>>>>>>>>>>>>>Test ERROR<<<<<<<<<<<<<<<<<<<<<')
            print('')
        return all_ok

if __name__=='__main__':
    if ParserTest().Test():
        print('All tests OK')
    else:
        print('One or more tests FAILED')