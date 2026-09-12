import re

def preprocess(filename):
    file = open(filename, "r")
    text = file.read()
    text = text.lower()
    text = re.sub(r'[^а-яё\s]', '', text) # only russian
    text = re.sub(r'\s+', ' ', text) # only spaces
    text_nospaces = re.sub(r' ', '', text)
    return (text, text_nospaces)

def main():
    # text, text_nospaces = preprocess("TEXT_UTF8")
    pass

if __name__ == "__main__":
    main()