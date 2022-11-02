import re

from SymbolTable import *
from PIF import *


class Scanner:
    def __init__(self):
        self.__symbol_table = SymbolTable()
        self.__pif = PIF()
        self.__tokens_path = 'token.in'
        self.__tokens = []
        self.__separators = []
        self.__operators = []
        self.__reserved_words = []

        self.__get_all_tokens()

    def __get_all_tokens(self):
        tokens_file = open(self.__tokens_path, 'r')

        while True:
            line = tokens_file.readline()

            if not line:
                break
            self.__tokens.append(line.strip())

        self.__operators = self.__tokens[:15]
        self.__separators = self.__tokens[15:26]
        self.__separators.append(' ')
        self.__separators.remove('')
        self.__reserved_words = self.__tokens[26:39]

    @property
    def operators(self):
        return self.__operators

    @property
    def separators(self):
        return self.__separators

    @property
    def reserved_words(self):
        return self.__reserved_words

    @property
    def pif(self):
        return self.__pif

    @property
    def symbol_table(self):
        return self.__symbol_table

    def split_file(self, file_path: str):
        try:
            file = open(file_path, "r")
            text = file.read()

            for separator in self.__separators[:-1]:
                text = text.replace(separator, " " + separator + " ")
            tokens = text.split()

            return tokens
        except Exception as ex:
            print(ex)

    def scan(self, file_path: str):
        tokens = self.split_file(file_path)

        identifier_regex = re.compile("^[a-zA-Z]+[a-zA-Z0-9_]*$")
        numerical_constant_regex = re.compile("^[0-9]$")
        string_constant_regex = re.compile('^"[a-zA-Z]*"$')
        char_constant_regex = re.compile("^'[a-zA-Z]'$")
        for token in tokens:
            if token in self.__operators:
                self.__pif.add((token, -1), "operator")
            elif token in self.__separators:
                self.__pif.add((token, -1), "separator")
            elif token in self.__reserved_words:
                self.__pif.add((token, -1), "reserved word")
            elif identifier_regex.match(token):
                if self.__symbol_table.has_identifier(token):
                    self.__pif.add((token, self.__symbol_table.get_identifier_position(token)), "identifier")
                    continue
                self.__symbol_table.insert_identifier(token)
                self.__pif.add((token, self.__symbol_table.get_identifier_position(token)), "identifier")
            elif numerical_constant_regex.match(token):
                token = int(token)
                if self.__symbol_table.has_constant(token):
                    self.__pif.add((token, self.__symbol_table.get_constant_position(token)), "constant")
                    continue
                self.__symbol_table.insert_constant(token)
                self.__pif.add((token, self.__symbol_table.get_constant_position(token)), "constant")
            elif string_constant_regex.match(token):
                token = token.strip('"')
                if self.__symbol_table.has_constant(token):
                    self.__pif.add((token, self.__symbol_table.get_constant_position(token)), "constant")
                    continue
                self.__symbol_table.insert_constant(token)
                self.__pif.add((token, self.__symbol_table.get_constant_position(token)), "constant")
            elif char_constant_regex.match(token):
                token = token.strip("'")
                if self.__symbol_table.has_constant(token):
                    self.__pif.add((token, self.__symbol_table.get_constant_position(token)), "constant")
                    continue
                self.__symbol_table.insert_constant(token)
                self.__pif.add((token, self.__symbol_table.get_constant_position(token)), "constant")
            else:
                print("Lexical error at token : " + token)
                return

        pif_file = open("PIF.out", "w")
        pif_file.write("PIF : \n")
        pif_file.write(str(self.__pif))

        pif_file.close()

        st_file = open("ST.out", "w")
        st_file.write("Symbol Table : \n")
        st_file.write(str(self.__symbol_table))
