from re import sub

ALPHABET = "абвгдежийклмнопрстуфхцчшщъыьэюя"
ALPHABET_LEN = len(ALPHABET)

def preprocess(filename):
    file = open(filename, "r")
    text = file.read()
    text = text.lower()
    text = sub(r'[^а-я]', '', text)
    return text

def vizhener_encrypt(cleartext, key):
    r = len(key)
    ciphertext = ""
    i = 0
    for letter in cleartext:
        index = ALPHABET.find(letter)
        cipher_index = (index + i) % ALPHABET_LEN
        ciphertext += ALPHABET[cipher_index]
        i = (i + 1) % r
    return ciphertext

def occurence_number(text, letter):
    count = 0
    for lett in text:
        if lett == letter:
            count += 1
    return count

def affinity_index(text):
    result = 0
    for letter in ALPHABET:
        nt = occurence_number(text, letter)
        result += nt * (nt - 1)
    n = len(text)
    return result / (n * (n - 1))

def find_r(text, theor_aff_i, error=0.01, max_r=30):
    for r in range(2, max_r + 1):
        blocks = [affinity_index(text[i::r]) for i in range(r)]
        avg_aff_i = sum(blocks) / len(blocks)
        print(f'{r}: {avg_aff_i}')
        diff = abs(theor_aff_i - avg_aff_i)
        if diff <= error:
            return r
    return -1


def main():
    
    # 1

    text = preprocess("./TEXT_UTF8")
    keys = [
        "от",
        "спа",
        "вухо",
        "сонце",
        "договоренность"
    ]
    theor_aff_i = affinity_index(text)
    print(f"For cleartext: {theor_aff_i}")
    for key in keys:
        ciphertext = vizhener_encrypt(text, key)
        print(f"For ciphertext (key: {key}): {affinity_index(ciphertext)}")
    # as expected, I(Y) becomes smaller as r becomes bigger

    # 2
    ciphertext = preprocess('./variant_10.txt')
    print(find_r(ciphertext, theor_aff_i))
    # Reasoning for this candidate:
    # Looking at the output of find_r, it's clear that the I(Y) is closest to the theoretical one when we are checking a multiple of r. 
    # This happens because blocks created by bigger multiples are subsets of the least multiple's block, although with less data.
    # Therefore the smallest multiple is the primary candidate
    # For other candidates the rest of the multiples in our range are picked

if __name__ == "__main__":
    main()