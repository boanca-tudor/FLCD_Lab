import copy
import re


class Parser:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__productions = self.rearrangeProductions()
        self.__first = self.first()
        self.__follow = self.follow()
        self.__parseTable = self.parseTable()

    def getNumberOfProduction(self, nonTerminal, prod):
        i = 1
        for p in self.__productions:
            for pp in self.__productions[p]:
                if pp == prod and nonTerminal == p:
                    return i
                i += 1

    def returnProductionWhichIsGeneratingTheTerminal(self, nonterminal, terminal):
        for prod in self.__productions[nonterminal]:
            for elem in prod:
                if terminal in elem:
                    return prod
        for prod in self.__productions[nonterminal]:
            for elem in prod:
                if elem in self.__grammar.get_nonterminals:
                    if '"' + terminal + '"' in self.__first[elem]:
                        return prod

    def returnEpsilonProductionOfNonterminal(self, nonTerminal):
        for prod in self.__productions[nonTerminal]:
            for elem in prod:
                if '"epsilon"' in elem:
                    return prod

    def rearrangeProductions(self):
        productions = self.__grammar.get_productions
        productionsRearranged = dict()
        for nonTerminal in self.__grammar.get_nonterminals:
            productionsRearranged[nonTerminal] = []
        productionsRearranged['simple_declaration'] = [['type', '" "', 'identifier']]
        for nonTerminal in productions:
            if nonTerminal != 'simple_declaration':
                for productionPart in productions[nonTerminal]:
                    current_production_part = []
                    while productionPart.find(' ') != -1:
                        index_space = productionPart.find(' ')
                        current_production_part.append(productionPart[0:index_space])
                        productionPart = productionPart[index_space+1:len(productionPart)]
                    current_production_part.append(productionPart[0:len(productionPart)])
                    productionsRearranged[nonTerminal].append(current_production_part)
        return productionsRearranged

    def first(self):
        current_first = dict()
        for terminal in self.__grammar.get_terminals:
            current_first[terminal] = [terminal]
        nextSymbolToLookInto = dict()
        for nonTerminal in self.__grammar.get_nonterminals:
            current_first[nonTerminal] = []
            nextSymbolToLookInto[nonTerminal] = []
        current_first[' '] = [' ']
        for nonTerminal in self.__grammar.get_nonterminals:
            for prod in self.__productions[nonTerminal]:
                if prod[0][1:len(prod[0]) - 1] in self.__grammar.get_terminals:
                    current_first[nonTerminal].append(prod[0])
        for nonTerminal in self.__grammar.get_nonterminals:
            if len(current_first[nonTerminal]) == 0:
                nextSymbolToLookInto[nonTerminal].append(self.__productions[nonTerminal][0][0])
        next_first = copy.deepcopy(current_first)
        while True:
            for nonTerminal in self.__grammar.get_nonterminals:
                for nextSymbol in nextSymbolToLookInto[nonTerminal]:
                    for prod in self.__productions[nextSymbol]:
                        if prod[0][1:len(prod[0])-1] in self.__grammar.get_terminals:
                            next_first[nonTerminal].append(prod[0])
            nextSymbolsToLookIntoFirst = dict()
            for nonTerminal in self.__grammar.get_nonterminals:
                nextSymbolsToLookIntoFirst[nonTerminal] = []
            for nonTerminal in self.__grammar.get_nonterminals:
                if len(next_first[nonTerminal]) == 0:
                    nextSymbolsToLookIntoFirst[nonTerminal].append(self.__productions[nextSymbolToLookInto[nonTerminal][0]][0][0])
            nextSymbolToLookInto = nextSymbolsToLookIntoFirst
            if current_first == next_first:
                break
            else:
                current_first = copy.deepcopy(next_first)
        print(next_first)
        return next_first

    def follow(self):
        current_follow = dict()
        for nonTerminal in self.__grammar.get_nonterminals:
            current_follow[nonTerminal] = []
        current_follow[self.__grammar.get_starting_symbol] = ['"epsilon"']
        next_follow = copy.deepcopy(current_follow)
        while True:
            for nonTerminal in self.__grammar.get_nonterminals:
                for production in self.__productions:
                    for p in self.__productions[production]:
                        if nonTerminal in p:
                            if p.index(nonTerminal) + 1 != len(p):
                                if p[p.index(nonTerminal)+1].find('"') != -1:
                                    for element in self.__first[p[p.index(nonTerminal)+1][1:len(p[p.index(nonTerminal)+1])-1]]:
                                        if element == '"epsilon"':
                                            for smth in current_follow[production]:
                                                if smth not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(smth)
                                        else:
                                            for smth in current_follow[nonTerminal]:
                                                if smth not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(smth)
                                            for smth in self.__first[p[p.index(nonTerminal)+1][1:len(p[p.index(nonTerminal)+1])-1]]:
                                                if smth not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(smth)
                                else:
                                    for element in self.__first[p[p.index(nonTerminal)+1]]:
                                        if element == '"epsilon"':
                                            for smth in current_follow[production]:
                                                if smth not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(smth)
                                        else:
                                            for smth in current_follow[nonTerminal]:
                                                if smth not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(smth)
                                            for smth in self.__first[p[p.index(nonTerminal)+1]]:
                                                if smth not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(smth)
                            else:
                                for smth in current_follow[production]:
                                    if smth not in next_follow[nonTerminal]:
                                        next_follow[nonTerminal].append(smth)
            if current_follow == next_follow:
                break
            else:
                current_follow = copy.deepcopy(next_follow)
        print(next_follow)
        return next_follow

    def parseTable(self):
        parseTable = dict()
        for terminal in self.__grammar.get_terminals:
            if terminal != 'epsilon':
                for nonTerminal in self.__grammar.get_nonterminals:
                    parseTable[(nonTerminal, terminal)] = []
                for terminal2 in self.__grammar.get_terminals:
                    if terminal2 != 'epsilon':
                        if terminal2 == terminal:
                            parseTable[(terminal2, terminal)] = ['pop']
                        else:
                            parseTable[(terminal2, terminal)] = []
                parseTable[('$', terminal)] = []
                parseTable[(terminal, '$')] = []
        for nonTerminal in self.__grammar.get_nonterminals:
            parseTable[(nonTerminal, '$')] = []
        parseTable[('$', '$')] = ['acc']
        for nonTerminal in self.__grammar.get_nonterminals:
            for terminal in self.__grammar.get_terminals:
                if terminal != 'epsilon':
                    if ('"' + terminal + '"') not in self.__first[nonTerminal]:
                        parseTable[(nonTerminal, terminal)] = ['err']
                    else:
                        parseTable[(nonTerminal, terminal)] = (self.returnProductionWhichIsGeneratingTheTerminal(nonTerminal, terminal), self.getNumberOfProduction(nonTerminal, self.returnProductionWhichIsGeneratingTheTerminal(nonTerminal, terminal)))
                else:
                    if ('"' + terminal + '"') in self.__first[nonTerminal]:
                        for elem in self.__follow[nonTerminal]:
                            if elem != '"epsilon"':
                                parseTable[(nonTerminal, elem.strip('"'))] = (self.returnEpsilonProductionOfNonterminal(nonTerminal), self.getNumberOfProduction(nonTerminal, self.returnEpsilonProductionOfNonterminal(nonTerminal)))
                            if elem == '"epsilon"':
                                parseTable[(nonTerminal, '$')] = (self.returnEpsilonProductionOfNonterminal(nonTerminal), self.getNumberOfProduction(nonTerminal, self.returnEpsilonProductionOfNonterminal(nonTerminal)))
        for i in parseTable:
            if len(parseTable[i]) == 0:
                parseTable[i] = ['err']
        return parseTable

    def parseSequence(self, word):
        input_stack = word
        input_stack.append('$')
        input_stack.reverse()
        work_stack = ['$', self.__grammar.get_starting_symbol]
        sequence = []

        while True:
            seq = self.__parseTable[(work_stack[-1].strip('"'), input_stack[-1].strip('"'))]
            if seq == ['acc']:
                break
            elif seq == ['pop']:
                input_stack.pop(-1)
                work_stack.pop(-1)
            elif seq == ['err']:
                return False
            elif ['"epsilon"'] in seq:
                work_stack.pop(-1)
                sequence.append(seq[1])
            else:
                work_stack.pop(-1)
                for i in range(len(seq[0])):
                    work_stack.append(seq[0][len(seq[0]) - i - 1].strip('"'))
                sequence.append(seq[1])

            print(input_stack)
            print(work_stack)
            print(sequence)
        return True