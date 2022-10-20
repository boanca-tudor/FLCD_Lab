from HashTable import *
from SymbolTable import *

if __name__ == '__main__':
    table = HashTable()

    table.insert("string1")
    assert(table.has_element("string1"))
    assert(table.has_element("string2") is False)
    # assert(table.has_element("string3"))

    print("Passed string test")

    table.insert(112)
    assert(table.has_element(112))
    assert(table.has_element(151232) is False)
    # assert(table.has_element(319532))

    print("Passed int test")

    assert(table.get_index(1215) is None)
    assert(table.get_index("string1") == 0)
    # assert(table.get_index("abcd") is not None)

    print("Passed get test")

    sym_table = SymbolTable()

    sym_table.insert_constant("string1")
    assert(sym_table.has_constant("string1"))
    assert(sym_table.has_identifier("string1") is False)
    assert(sym_table.has_constant("string2") is False)

    sym_table.insert_identifier(112)
    assert(sym_table.has_identifier(112) is False)
    sym_table.insert_identifier("id1")
    assert(sym_table.has_identifier("id1"))

    print("Passed symbol table test")


