class DataTable():
    banners = {
        'gender': [
            {
                'column': 'male',
                'expression': 's1 = 1',
                'count': 50,
                'basis': 100
            },
            {
                'column': 'female',
                'expression': 's1 = 2',
                'count': 50,
                'basis': 100
            }
        ],
        'age': [
            {
                'column': '20-24',
                'expression': '',
                'count': 50,
                'basis': 100
            },
            {
                'column': '25-29',
                'expression': '',
                'count': 50,
                'basis': 100
            },
        ],
        'age and gender': [
            {
                'column': 'male and 20-24',
                'expression': '',
                'count': 30,
                'basis': 100
            },
            {
                'column': 'male and 25-29',
                'expression': '',
                'count': 30,
                'basis': 100
            },
            {
                'column': 'female and 20-24',
                'expression': '',
                'count': 20,
                'basis': 100
            },
            {
                'column': 'female 25-29',
                'expression': '',
                'count': 10,
                'basis': 100
            },
        ]
    }

    def Validate(self):
        for banner in self.banners:
            total = 0
            basis = -1
            # Loop through each of the column in a banner
            for column in self.banners[banner]:
                # Checking that the basis for each column is matching
                prev_basis = basis
                basis = column['basis']
                if prev_basis != -1 and basis != prev_basis:
                    raise Exception('basis values of columns did not match for banner: ' + banner)
                # Summing up the count values
                total = total + column['count']
            # Check that the count adds up to the basis
            if total != basis:
                raise Exception('the total of count values: ' + str(total) + ' does not equal the basis: ' + str(basis) + ' for banner: ' + banner)
        print('DataTable successfully validated!')


if __name__=='__main__':
    DataTable().Validate()