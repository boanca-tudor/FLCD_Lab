import copy

from Node import Node, NodeHelper


class Parser:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__productions = self.rearrangeProductions()
        self.__first = self.first()
        self.__follow = self.follow()
        self.__parseTable = self.parseTable()
        self.__input_stack = None
        self.__work_stack = None
        self.__sequence = []
        self.__parserOutputString = []

    @property
    def returnParserOutputString(self):
        return self.__parserOutputString

    @property
    def returnParseTable(self):
        return self.__parseTable

    @property
    def returnFirst(self):
        return self.__first

    @property
    def returnFollow(self):
        return self.__follow

    '''
        Return the number of the given production, which has to be associated with the given nonterminal.
    '''
    def getNumberOfProduction(self, nonTerminal, prod):
        i = 1
        for p in self.__productions:
            for pp in self.__productions[p]:
                if pp == prod and nonTerminal == p:
                    return i
                i += 1

    '''
        Returns the production based on the order number given as argument.
    '''
    def getProductionBasedOnNumber(self, number):
        i = 1
        for p in self.__productions:
            for pp in self.__productions[p]:
                if i == number:
                    return pp
                i += 1
        return None

    '''
        Returns the production, if exists, which generates the given terminal, starting from the given nonTerminal.
    '''
    def returnProductionWhichIsGeneratingTheTerminal(self, nonterminal, terminal):
        for prod in self.__productions[nonterminal]:
            for elem in prod:
                if terminal in elem:
                    return prod
        for prod in self.__productions[nonterminal]:
            for elem in prod:
                if elem in self.__grammar.get_nonterminals:
                    # if the terminal can be generated from the nonTerminal, it has to be in the first table of the
                    # nonTerminals of the production, or of the nonTerminals which can be generated from the nonTerminals
                    # of the production
                    if terminal in self.__first[elem]:
                        return prod

    '''
        Returns the epsilon production of the given nonTerminal, if it has any.
    '''
    def returnEpsilonProductionOfNonterminal(self, nonTerminal):
        for prod in self.__productions[nonTerminal]:
            for elem in prod:
                if '"epsilon"' in elem:
                    return prod

    '''
        Splits the productions of the grammar into lists of strings for easier usage.
    '''
    def rearrangeProductions(self):
        productions = self.__grammar.get_productions
        productionsRearranged = dict()
        for nonTerminal in self.__grammar.get_nonterminals:
            productionsRearranged[nonTerminal] = []
        # since it contains space, which cannot be shown in the file, since space is the symbol I am splitting by
        productionsRearranged['simple_declaration'] = [['type', '" "', 'identifier']]
        for nonTerminal in productions:
            if nonTerminal != 'simple_declaration':
                for productionPart in productions[nonTerminal]:
                    current_production_part = []
                    while productionPart.find(' ') != -1:
                        index_space = productionPart.find(' ')
                        current_production_part.append(productionPart[0:index_space])
                        productionPart = productionPart[index_space + 1:len(productionPart)]
                    current_production_part.append(productionPart[0:len(productionPart)])
                    productionsRearranged[nonTerminal].append(current_production_part)
        return productionsRearranged

    '''
        Generates and returns the first table of the grammar.
    '''
    def first(self):
        current_first = dict()

        # initialization of the first of terminals
        for terminal in self.__grammar.get_terminals:
            current_first[terminal.strip('"')] = [terminal.strip('"')]
        nextSymbolToLookInto = dict()

        for nonTerminal in self.__grammar.get_nonterminals:
            current_first[nonTerminal] = []
            nextSymbolToLookInto[nonTerminal] = []

        # initialization of the first of nonTerminals
        for nonTerminal in self.__grammar.get_nonterminals:
            for prod in self.__productions[nonTerminal]:
                if prod[0].strip('"') in self.__grammar.get_terminals:
                    current_first[nonTerminal].append(prod[0].strip('"'))

        # saving the terminals to look into in a list
        for nonTerminal in self.__grammar.get_nonterminals:
            for prodToLookInto in self.__productions[nonTerminal]:
                if prodToLookInto[0].strip('"') not in self.__grammar.get_terminals \
                        and prodToLookInto[0] != nonTerminal \
                        and prodToLookInto[0] not in nextSymbolToLookInto[nonTerminal]:
                    nextSymbolToLookInto[nonTerminal].append(prodToLookInto[0])
        next_first = copy.deepcopy(current_first)

        while True:
            for nonTerminal in self.__grammar.get_nonterminals:
                # for each symbol we have to look into
                for nextSymbol in nextSymbolToLookInto[nonTerminal]:
                    # get the productions of that symbol
                    for prod in self.__productions[nextSymbol]:
                        if prod[0].strip('"') in self.__grammar.get_terminals and prod[0].strip('"') not in next_first[nonTerminal]:
                            next_first[nonTerminal].append(prod[0].strip('"'))

            # auxiliary dictionary for computing the next to look into list
            nextSymbolsToLookIntoFirst = dict()
            for nonTerminal in self.__grammar.get_nonterminals:
                nextSymbolsToLookIntoFirst[nonTerminal] = []

            for nonTerminal in self.__grammar.get_nonterminals:
                for eachNext in nextSymbolToLookInto[nonTerminal]:
                    for prodToLookInto in self.__productions[eachNext]:
                        if prodToLookInto[0].strip('"') not in self.__grammar.get_terminals \
                                and prodToLookInto[0] != nonTerminal \
                                and prodToLookInto[0] not in nextSymbolsToLookIntoFirst[nonTerminal]:
                            nextSymbolsToLookIntoFirst[nonTerminal].append(prodToLookInto[0])

            nextSymbolToLookInto = nextSymbolsToLookIntoFirst

            # if the previous iteration matches the current one, we stop the execution and the last version will be
            # out first table
            if current_first == next_first:
                break
            else:
                current_first = copy.deepcopy(next_first)

        return next_first

    '''
        Generated and returns the follow table of the grammar.
    '''
    def follow(self):

        # initialization of the nonterminals with empty list
        current_follow = dict()
        for nonTerminal in self.__grammar.get_nonterminals:
            current_follow[nonTerminal] = []

        # initialization of the starting symbol with epsilon
        current_follow[self.__grammar.get_starting_symbol] = ['epsilon']

        next_follow = copy.deepcopy(current_follow)

        while True:
            for nonTerminal in self.__grammar.get_nonterminals:
                for production in self.__productions:
                    for productionEntry in self.__productions[production]:
                        if nonTerminal in productionEntry:

                            # if there is at least a symbol(terminal or nonTerminal) after the nonTerminal
                            if productionEntry.index(nonTerminal) + 1 != len(productionEntry):

                                # if the production contains a terminal
                                if productionEntry[productionEntry.index(nonTerminal) + 1].find('"') != -1:

                                    start_index_symbol_after_nonterminal = productionEntry.index(nonTerminal) + 1
                                    end_index_symbol_after_nonterminal = len(productionEntry[productionEntry.index(nonTerminal) + 1]) - 1
                                    for element in self.__first[productionEntry[start_index_symbol_after_nonterminal][1:end_index_symbol_after_nonterminal]]:
                                        # copy the previous values of the follow in the current one
                                        for previousValues in current_follow[nonTerminal]:
                                            if previousValues not in next_follow[nonTerminal]:
                                                next_follow[nonTerminal].append(previousValues.strip('"'))
                                        for entryFromFollowFromLeftHandSideProduction in self.__first[productionEntry[productionEntry.index(nonTerminal) + 1][1:len(productionEntry[productionEntry.index(nonTerminal) + 1]) - 1]]:
                                            if entryFromFollowFromLeftHandSideProduction not in next_follow[nonTerminal]:
                                                next_follow[nonTerminal].append(entryFromFollowFromLeftHandSideProduction.strip('"'))
                                else:
                                    for element in self.__first[productionEntry[productionEntry.index(nonTerminal) + 1]]:
                                        if element == 'epsilon':
                                            # if the first of the next Symbol contains epsilon, we append to the follow list
                                            # of the nonterminal the previous iteration's results from the left-hand side
                                            # of the visited production
                                            for previousValues in current_follow[production]:
                                                if previousValues not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(previousValues.strip('"'))
                                        else:
                                            for entryFromFollowFromLeftHandSideProduction in current_follow[production]:
                                                if entryFromFollowFromLeftHandSideProduction not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(
                                                        entryFromFollowFromLeftHandSideProduction.strip('"'))

                                            for entryFromFirstOfNonterminalAfter in self.__first[productionEntry[productionEntry.index(nonTerminal) + 1]]:
                                                if entryFromFirstOfNonterminalAfter not in next_follow[nonTerminal]:
                                                    next_follow[nonTerminal].append(entryFromFirstOfNonterminalAfter.strip('"'))
                            else:
                                # if there is nothing after the current nonterminal -> only epsilon
                                for entryFromFollowFromLeftHandSideProduction in current_follow[production]:
                                    if entryFromFollowFromLeftHandSideProduction not in next_follow[nonTerminal]:
                                        next_follow[nonTerminal].append(entryFromFollowFromLeftHandSideProduction.strip('"'))

            if current_follow == next_follow:
                break
            else:
                current_follow = copy.deepcopy(next_follow)
        return next_follow

    '''
        Computes and returns the parse table of the grammar.
    '''
    def parseTable(self):

        # initialization
        parseTable = dict()
        for terminal in self.__grammar.get_terminals:
            if terminal != 'epsilon':
                for nonTerminal in self.__grammar.get_nonterminals:
                    parseTable[(nonTerminal, terminal.strip('"'))] = []
                for terminal2 in self.__grammar.get_terminals:
                    if terminal2 != 'epsilon':
                        if terminal2.strip('"') == terminal.strip('"'):
                            parseTable[(terminal2.strip('"'), terminal.strip('"'))] = ['pop']
                        else:
                            parseTable[(terminal2.strip('"'), terminal.strip('"'))] = []
                parseTable[('$', terminal.strip('"'))] = []
                parseTable[(terminal.strip('"'), '$')] = []
        for nonTerminal in self.__grammar.get_nonterminals:
            parseTable[(nonTerminal, '$')] = []
        parseTable[('$', '$')] = ['acc']

        # parse table
        for nonTerminal in self.__grammar.get_nonterminals:
            for terminal in self.__grammar.get_terminals:
                # since in the parseTable the symbol of epsilon is replaced by $, we have to be careful that we do not
                # put epsilon as a key of the parseTable
                if terminal != 'epsilon':

                    if terminal not in self.__first[nonTerminal]:
                        # we cannot get to that terminal directly from the nonTerminal
                        parseTable[(nonTerminal, terminal.strip('"'))] = ['err']
                    else:
                        production = self.returnProductionWhichIsGeneratingTheTerminal(nonTerminal, terminal)
                        numberOfProduction = self.getNumberOfProduction(nonTerminal, self.returnProductionWhichIsGeneratingTheTerminal(nonTerminal, terminal))
                        parseTable[(nonTerminal, terminal.strip('"'))] = (production, numberOfProduction)

                else:
                    if terminal in self.__first[nonTerminal]:
                        for elem in self.__follow[nonTerminal]:
                            production = self.returnEpsilonProductionOfNonterminal(nonTerminal)
                            numberOfProduction = self.getNumberOfProduction(nonTerminal, self.returnEpsilonProductionOfNonterminal(nonTerminal))

                            if elem != 'epsilon':
                                parseTable[(nonTerminal, elem.strip('"'))] = (production, numberOfProduction)

                            if elem == 'epsilon':
                                parseTable[(nonTerminal, '$')] = (production, numberOfProduction)

        # every unfilled entry means that we cannot get from the first key to the other
        for i in parseTable:
            if len(parseTable[i]) == 0:
                parseTable[i] = ['err']

        return parseTable

    '''
        Parses a given sequence and returns the truth value of the syntactical correctness of the sequence and in case
        it is syntactically correct, it returns the production string.
    '''
    def parseSequence(self, sequence):

        # the entries of the sequence
        self.__input_stack = sequence
        self.__input_stack.append('$')
        self.__input_stack.reverse()

        # the currently used productions
        self.__work_stack = ['$', self.__grammar.get_starting_symbol]

        # the production string
        self.__sequence = []

        while True:
            self.__parserOutputString.append(copy.deepcopy("input stack:\n" + str(self.__input_stack)))
            self.__parserOutputString.append(copy.deepcopy("work stack:\n" + str(self.__work_stack)))
            self.__parserOutputString.append(copy.deepcopy("production string:\n" + str(self.__sequence)))
            self.__parserOutputString.append('\n')

            # since spaces were not added in the symbolTable, we have to exclude them
            if self.__work_stack[-1].strip('"') == ' ':
                self.__work_stack.pop(-1)
                continue

            try:
                seq = self.__parseTable[(self.__work_stack[-1].strip('"'), self.__input_stack[-1].strip('"'))]

                # the sequence is accepted
                if seq == ['acc']:
                    break

                # the top of the input stack and work stack are identical
                elif seq == ['pop']:
                    self.__input_stack.pop(-1)
                    self.__work_stack.pop(-1)

                # the sequence has syntactical errors
                elif seq == ['err']:
                    self.__parserOutputString.append("ERROR AT SYMBOL: " + self.__input_stack[-1].strip('"'))
                    return False, None

                # if epsilon appears, we only pop from the work stack
                elif ['"epsilon"'] in seq:
                    self.__work_stack.pop(-1)
                    self.__sequence.append(seq[1])

                # if the symbol can be generated form the production in the work stack
                else:
                    self.__work_stack.pop(-1)
                    for i in range(len(seq[0])):
                        self.__work_stack.append(seq[0][len(seq[0]) - i - 1].strip('"'))
                    self.__sequence.append(seq[1])

            # if the entries don't exist in the parseTable
            except KeyError:
                self.__parserOutputString.append("ERROR AT SYMBOL: " + self.__input_stack[-1].strip('"'))
                return False, None

        self.__parserOutputString.append(copy.deepcopy("input stack:\n" + str(self.__input_stack)))
        self.__parserOutputString.append(copy.deepcopy("work stack:\n" + str(self.__work_stack)))
        self.__parserOutputString.append(copy.deepcopy("production string:\n" + str(self.__sequence)))
        self.__parserOutputString.append('\n')

        return True, self.__sequence

    '''
        Creates the parse tree of the parsed sequence, using the returned production string.
    '''
    def createParseTree(self, productionString):
        helperNodeList = []
        nodeStack = []
        productionIndex = 0
        nodeNumber = 0

        node = NodeHelper(self.__grammar.get_starting_symbol)
        node.sibling = 0
        nodeNumber += 1
        node.index = nodeNumber

        helperNodeList.append(node)
        nodeStack.append(node)

        maxLevel = -1
        nodesPerLevel = {}

        while productionIndex < len(productionString):
            currentNode = nodeStack[0]

            # if a terminal appears, we pop it, since it cannot create new Node entries
            if currentNode.value.strip('"') in self.__grammar.get_terminals:
                nodeStack.remove(nodeStack[0])
                continue

            production = self.getProductionBasedOnNumber(productionString[productionIndex])
            nodesToAdd = []

            # creating the child nodes of the current node by looking in the productions from the production string
            for i in range(0, len(production)):
                child = NodeHelper(production[i])
                child.father = currentNode
                child.level = currentNode.level + 1

                # computing the maximum Level of the parsing tree
                if child.level > maxLevel:
                    maxLevel = child.level

                if child.level in nodesPerLevel:
                    nodesPerLevel[child.level].append(child)
                else:
                    nodesPerLevel[child.level] = [child]

                helperNodeList.append(child)
                nodesToAdd.append(child)

            # reinitializing the nodeStack by popping the already visited node and replacing it with its production
            index = nodeStack.index(currentNode)
            del nodeStack[index]
            for i in range(index, index + len(nodesToAdd)):
                nodeStack.insert(i, nodesToAdd[i])

            productionIndex += 1

        currentLevel = 0
        currentIndex = 1

        # computing the index of each node based on the level attribute from the NodeHelper object
        while currentLevel <= maxLevel:
            for i in range(len(helperNodeList)):
                if helperNodeList[i].level == currentLevel:
                    helperNodeList[i].index = currentIndex
                    currentIndex += 1
            currentLevel += 1

        # computing the right sibling of each node after the indexes are set for every node
        for level in nodesPerLevel:
            for i in range(len(nodesPerLevel[level])):
                if i == len(nodesPerLevel[level]) - 1:
                    nodesPerLevel[level][i].sibling = 0
                else:
                    if nodesPerLevel[level][i].father == nodesPerLevel[level][i + 1].father \
                            or nodesPerLevel[level][i].father.sibling == nodesPerLevel[level][i + 1].father.index:
                        nodesPerLevel[level][i].sibling = nodesPerLevel[level][i + 1].index
                    else:
                        nodesPerLevel[level][i].sibling = 0

        nodeList = []

        # creating the nodeList from the helperNodeList
        for helperNode in helperNodeList:
            node = Node(helperNode.value)
            node.sibling = helperNode.sibling
            node.index = helperNode.index
            if helperNode.father is not None:
                node.father = helperNode.father.index
            else:
                node.father = 0
            nodeList.append(node)

        return nodeList
