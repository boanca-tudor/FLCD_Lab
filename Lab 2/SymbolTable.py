from HashTable import *


class SymbolTable:
    def __init__(self):
        self.__identifiers = HashTable()
        self.__constants = HashTable()

    @property
    def identifiers(self):
        return self.__identifiers

    @property
    def constants(self):
        return self.__constants

    def insert_identifier(self, new_element):
        if type(new_element) is str:
            self.__identifiers.insert(new_element)

    def insert_constant(self, new_element):
        self.__constants.insert(new_element)

    def has_identifier(self, element):
        return self.__identifiers.has_element(element)

    def has_constant(self, element):
        return self.__constants.has_element(element)
