class Test:

    def __init__(self, parser, grammar):
        self.__parser = parser
        self.__grammar = grammar
        self.testFirst()
        self.testFollow()
        self.testParsingTable()
        self.testParsingMethod()
        self.testParseTree()

    def testFirst(self):
        first = self.__parser.returnFirst
        assert first['S'] == ['(', 'a']
        assert first['A'] == ['+', 'epsilon']
        assert first['B'] == ['(', 'a']
        assert first['C'] == ['*', 'epsilon']
        assert first['D'] == ['(', 'a']
        assert first['a'] == ['a']

        for terminal in self.__grammar.get_terminals:
            assert len(first[terminal]) == 1

        for nonTerminal in self.__grammar.get_nonterminals:
            assert len(first[nonTerminal]) != 0

    def testFollow(self):
        follow = self.__parser.returnFollow
        assert 'epsilon' in follow['S']
        assert ')' in follow['S']
        assert 'epsilon' in follow['A']
        assert ')' in follow['A']
        assert 'epsilon' in follow['B']
        assert ')' in follow['B']
        assert '+' in follow['B']
        assert 'epsilon' in follow['C']
        assert ')' in follow['C']
        assert '+' in follow['C']
        assert 'epsilon' in follow['D']
        assert ')' in follow['D']
        assert '+' in follow['D']
        assert '*' in follow['D']

        # the follow method is only defined for the nonTerminals, therefore none of the terminals have an entry in the
        # follow table
        for terminal in self.__grammar.get_terminals:
            try:
                assert 'epsilon' in follow[terminal]
            except KeyError:
                pass

    def testParsingTable(self):
        parseTable = self.__parser.returnParseTable

        assert parseTable[('S', 'a')] == (['B', 'A'], 1)
        assert parseTable[('a', 'a')] == ['pop']
        assert parseTable[('D', '(')] == (['"("', 'S', '")"'], 7)
        assert parseTable[('A', ')')] == (['"epsilon"'], 3)
        assert parseTable[('C', '*')] == (['"*"', 'D', 'C'], 5)
        assert parseTable[('a', '*')] == ['err']
        assert parseTable[('$', '$')] == ['acc']

        for terminal1 in self.__grammar.get_terminals:
            for terminal2 in self.__grammar.get_terminals:
                if terminal1 != 'epsilon' and terminal2 != 'epsilon':
                    if terminal1 != terminal2:
                        assert parseTable[(terminal1, terminal2)] == ['err']
                    else:
                        assert parseTable[(terminal1, terminal2)] == ['pop']

    def testParsingMethod(self):
        truthValue, productionString = self.__parser.parseSequence(['a', '*', '(', 'a', '+', 'a', ')'])
        assert truthValue is True
        truthValue, productionString = self.__parser.parseSequence(['(', 'a', '(', 'a', ')', ')'])
        assert truthValue is False
        truthValue, productionString = self.__parser.parseSequence(['(', 'a', ')'])
        assert truthValue is True
        truthValue, productionString = self.__parser.parseSequence(['c', 'd', 'e', 'f'])
        assert truthValue is False
        truthValue, productionString = self.__parser.parseSequence(['a', '*', 'a', '+', 'a'])
        assert truthValue is True
        truthValue, productionString = self.__parser.parseSequence(['a', '*', 'a', '+', 'a', ')'])
        assert truthValue is False
        truthValue, productionString = self.__parser.parseSequence(['a', '*', '(', 'a', '+', 'a', ')'])
        assert truthValue is True
        truthValue, productionString = self.__parser.parseSequence(['a', 'a', 'a'])
        assert truthValue is False
        truthValue, productionString = self.__parser.parseSequence(['a', '*', '(', 'a', '+', 'a', '*','(', 'a', '+', 'a', ')', ')'])
        assert truthValue is True

    def testParseTree(self):
        truthValue, productionString = self.__parser.parseSequence(['a', '*', '(', 'a', '+', 'a', ')'])
        parseTree = self.__parser.createParseTree(productionString)
        parseTree.sort(key=lambda x: x.index)

        # the indexing starts at 1
        assert parseTree[0].index == 1

        # the root node has no father or sibling
        assert parseTree[0].father == 0
        assert parseTree[0].sibling == 0

        assert parseTree[5].value == '"epsilon"'
        assert parseTree[13].value == '"epsilon"'
        assert parseTree[22].value == '"epsilon"'
        assert parseTree[25].value == '"epsilon"'
        assert parseTree[27].value == '"epsilon"'

        assert parseTree[18].index == 19
        assert parseTree[18].value == '"+"'
        assert parseTree[18].father == 16
        assert parseTree[18].sibling == 20

        assert parseTree[8].index == 9
        assert parseTree[8].value == "D"
        assert parseTree[8].father == 5
        assert parseTree[8].sibling == 10

        assert parseTree[24].index == 25
        assert parseTree[24].value == "C"
        assert parseTree[24].father == 20
        assert parseTree[24].sibling == 26
