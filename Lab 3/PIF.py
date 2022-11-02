class PIF:
    def __init__(self):
        self.__tokens = []
        self.__type = []

    def add(self, elem, _type):
        self.__tokens.append(elem)
        self.__type.append(_type)

    def __str__(self):
        string = ""

        for i in range(len(self.__tokens)):
            string = string + str(self.__tokens[i][0]) + " - " + str(self.__tokens[i][1]) + " -> "
            string = string + str(self.__type[i]) + "\n"

        return string
