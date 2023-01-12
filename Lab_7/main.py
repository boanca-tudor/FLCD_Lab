from Parser import Parser
from ParserOutput import ParserOutput
from Test import Test
from grammar import Grammar

if __name__ == '__main__':

    # Grammar for testing purposes
    grammar3 = Grammar.get_grammar_from_file("g3.txt")
    parser3 = Parser(grammar3)
    test = Test(parser3, grammar3)

    # Grammar for example purposes
    grammar = Grammar.get_grammar_from_file("g1.txt")
    parser = Parser(grammar)

    parserOutput = ParserOutput("out1.txt", "seq.txt", parser)
    parserOutput.writeToFile()

    # Grammar for the minilanguage
    grammar1 = Grammar.get_grammar_from_file("g2.txt")
    parser1 = Parser(grammar1)

    parserOutput1 = ParserOutput("out2.txt", "pif.out", parser1)
    parserOutput1.writeToFile()

