from grammar import Grammar

if __name__ == '__main__':
    grammar = Grammar.get_grammar_from_file("g1.txt")
    print(grammar.get_terminals)
    print(grammar.get_nonterminals)
    print(grammar.get_productions)
    print(grammar.get_starting_symbol)

    print(grammar.get_productions_for_nonterminal("decllist"))

    print(grammar.verify_CFG())

    grammar = Grammar.get_grammar_from_file("g2.txt")
    print(grammar.get_terminals)
    print(grammar.get_nonterminals)
    print(grammar.get_productions)
    print(grammar.get_starting_symbol)

    print(grammar.get_productions_for_nonterminal("expression"))

    print(grammar.verify_CFG())
