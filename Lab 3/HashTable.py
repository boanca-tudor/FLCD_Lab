class HashTable:
    def __init__(self):
        self.__max_size = 4096
        self.__hash_table = [None] * self.__max_size

    def __hash_function(self, element):
        if type(element) is str:
            return sum(ord(character) for character in element) % self.__max_size
        if type(element) is int:
            return element % self.__max_size
        return None

    def insert(self, new_element):
        position = self.__hash_function(new_element)
        if position is None:
            return False
        if self.__hash_table[position] is None:
            self.__hash_table[position] = [new_element]
        else:
            for element in self.__hash_table[position]:
                if element is new_element:
                    return
                else:
                    self.__hash_table[position].append(new_element)
        return True

    def get_index(self, element):
        position = self.__hash_function(element)

        if self.__hash_table[position] is None:
            return None
        else:
            if element in self.__hash_table[position]:
                return self.__hash_table[position].index(element)
            return None

    def get_hash(self, element):
        return self.__hash_function(element)

    def has_element(self, element):
        position = self.__hash_function(element)

        if self.__hash_table[position] is None:
            return False
        else:
            return element in self.__hash_table[position]

    def __str__(self):
        string = ""

        for i in range(len(self.__hash_table)):
            if self.__hash_table[i] is not None:
                string += str(i) + " - " + str(self.__hash_table[i]) + "\n"

        return string
