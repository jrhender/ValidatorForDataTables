class ParserTest():
    """
    Actual logic looks like s1 = 4. Where s1 corresponds to a question and 4 corresponds to code.
    """
    tests = [
        {
            'banners': ['male', 'female'],
            'result': 15
        },
        {
            'banners': ['male', 'female', '21-25', 'red'],
            'result': 3
        },
        {
            'banners': ['male', 'female', '21-25', 'green'],
            'result': 3
        },
        {
            'banners': ['male', 'female', '21-25', 'blue'],
            'result': 1
        }
    ]

    banners = {
        'male': {
            'question': 'gender',
            'count': 7
        },
        'female': {
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