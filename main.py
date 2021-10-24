from lang import Lang

if __name__ == '__main__':
    l = Lang("prog/test.lox")
    v = l.exec()

    print(v)
