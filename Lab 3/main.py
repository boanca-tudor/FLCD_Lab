from Scanner import *

if __name__ == '__main__':
    scanner = Scanner()

    print(scanner.operators)
    print(scanner.separators)
    print(scanner.reserved_words)

    scanner.scan("p3.txt")
