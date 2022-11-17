class FiniteAutomata:
    def __init__(self, file_path: str):
        self.__states = []
        self.__alphabet = []
        self.__transitions = dict()
        self.__final_states = []
        self.__separator = ","
        self.__transition_separator = "-"
        self.__read_from_file(file_path)

    def __read_from_file(self, file_path: str):
        file = open(file_path, "r")

        self.__states = file.readline().strip().split(self.__separator)

        for state in self.__states:
            self.__transitions[state] = []

        self.__alphabet = file.readline().strip().split(self.__separator)

        transitions = file.readline().strip().split(self.__separator)

        for tran in transitions:
            parts = tran.split(self.__transition_separator)
            self.__transitions[parts[0]].append((parts[1], parts[2]))

        self.__final_states = file.readline().strip().split(self.__separator)

    def __is_deterministic(self):
        for state in self.__states:
            symbols = []
            for (symbol, _) in self.__transitions[state]:
                if symbol not in symbols:
                    symbols.append(symbol)

            if len(symbols) != len(self.__transitions[state]):
                return False

        return True

    def accepts(self, sequence):
        if not self.__is_deterministic():
            return False

        current_state = self.__states[0]

        for i in range(len(sequence)):
            current_symbol = sequence[i]
            available_transitions = self.__transitions[current_state]

            if len(available_transitions) == 0:
                return False

            found = False
            for (transition_symbol, next_state) in self.__transitions[current_state]:
                if current_symbol == transition_symbol:
                    current_state = next_state
                    found = True

            if not found:
                return False

        return True
