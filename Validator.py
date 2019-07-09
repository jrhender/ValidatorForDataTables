from pyparsing import *

def upper_case_it(tokens):
  return [t.upper() for t in tokens]

prefix = 'A Fist Full of' + White()
fist_contents = Word(alphas)

fist_contents.setParseAction(upper_case_it)

title_parser = Combine(prefix + fist_contents)

for title in (
  'A Fistful of Dollars',
  'A Fistful of Spaghetti',
  'A Fistful of Doughnuts',
):
print(title_parser.parseString(title))