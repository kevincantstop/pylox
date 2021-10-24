def load(file):
    with open(file) as reader:
        code = reader.read()
    return code
