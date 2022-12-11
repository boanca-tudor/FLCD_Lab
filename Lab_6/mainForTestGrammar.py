from grammar import Grammar

if __name__ == '__main__':
    grammar1 = Grammar.get_grammar_from_file("g1.txt")
    print(grammar1.get_terminals)
    print(grammar1.get_nonterminals)
    print(grammar1.get_productions)
    print(grammar1.get_starting_symbol)

    print(grammar1.get_productions_for_nonterminal("decllist"))

    print(grammar1.verify_CFG())

    print('\n\n\n')

    grammar2 = Grammar.get_grammar_from_file("g2.txt")
    print(grammar2.get_terminals)
    print(grammar2.get_nonterminals)
    print(grammar2.get_productions)
    print(grammar2.get_starting_symbol)

    print(grammar2.get_productions_for_nonterminal("simplstmt"))
    print(grammar2.get_productions_for_nonterminal("program"))

    print(grammar2.verify_CFG())
