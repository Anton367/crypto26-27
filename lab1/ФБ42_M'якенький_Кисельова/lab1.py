import re

def preprocess(filename):
    file = open(filename, "r")
    text = file.read()
    text = text.lower()
    text = re.sub(r'[^а-яё\s]', '', text) # only russian
    text = re.sub(r'\s+', ' ', text) # only spaces
    text_nospaces = re.sub(r' ', '', text)
    return (text, text_nospaces)

def prob_dist_1(text):
    dist = {}
    for symbol in text:
        dist[symbol] = dist.get(symbol, 0) + 1
    for k in dist.keys():
        dist[k] /= len(text)
    return dist

def prob_dist_2(text):
    dist = {}
    for i in range(0, len(text)-1):
        bigram = text[i:i+2]
        dist[bigram] = dist.get(bigram, 0) + 1
    for k in dist.keys():
        dist[k] /= len(text) - 1
    return dist

def prob_dist_2_no_intersect(text):
    dist = {}
    for i in range(0, len(text)-1, 2):
        bigram = text[i:i+2]
        dist[bigram] = dist.get(bigram, 0) + 1
    for k in dist.keys():
        dist[k] /= len(text) - 1
    return dist


def main():
    text, text_nospaces = preprocess("TEXT_UTF8")
    dist = prob_dist_1(text)
    print(dist)
    dist = prob_dist_2(text)
    print(dist)

if __name__ == "__main__":
    main()