from itertools import islice

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
M = len(ALPHABET)

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def find_b(x, y, m, a):
    return (y - a*x) % m

def inverse_by_modulo(a, m):
    (r, r_next) = (a, m)
    (u, u_next) = (1, 0)

    while r_next > 0:
        q = r // r_next
        (r, r_next) = (r_next, r - q * r_next)
        (u, u_next) = (u_next, u - q * u_next)

    return u % m

def solve_linear_comparison(x_1, x_2, y_1, y_2, m=M**2):
    x = x_2 - x_1
    y = y_2 - y_1

    solutions = []
    d = gcd(x, m)

    if d == 1:
        a = inverse_by_modulo(x, m)*y % m
        solutions.append((a, find_b(x_1, y_1, m, a)))
    else:
        q = y % d
        if q:
            return solutions
        
        x_0 = x // d
        y_0 = y // d
        m_0 = m // d

        a_0 = inverse_by_modulo(x_0, m_0)*y_0 % m_0

        for i in range(d):
            a = (a_0 + i * m_0) % m
            b = find_b(x_1, y_1, m, a)
            solutions.append((a, b))

    return solutions

def prob_dist_2_no_intersect(text):
    dist = {}
    count = 0
    for i in range(0, len(text)-1, 2):
        bigram = text[i:i+2]
        dist[bigram] = dist.get(bigram, 0) + 1
        count += 1
    for k in dist:
        dist[k] /= count
    return dist

def dist_max_n(dist, n):
    return sorted(dist, key=dist.get, reverse=True)[:n]

def bigram_to_num(bigram):
    return ALPHABET.find(bigram[0]) * M + ALPHABET.find(bigram[1])

def num_to_bigram(num):
    return ALPHABET[num // M] + ALPHABET[num % M]

def athens_bigram_decrypt(a, b, ciphertext, m=M**2):
    cleartext = ""
    a_inv = inverse_by_modulo(a, m)
    for i in range(0, len(ciphertext)-1, 2):
        y = bigram_to_num(ciphertext[i:i+2])
        x = (a_inv * (y - b)) % m
        cleartext += num_to_bigram(x)
    return cleartext

def detect_cleartext():
    pass

def main():
    most_common_cleartext = ["ст", "но", "то", "на", "ен"]

    file = open("./variant_10.txt")
    ciphertext = file.read()

    most_common_ciphertext = dist_max_n(
        prob_dist_2_no_intersect(ciphertext),
        5
    )

    print(f"clear: {most_common_cleartext}")
    print(f"cipher: {most_common_ciphertext}")

    clear = list(map(lambda b: bigram_to_num(b), most_common_cleartext))
    cipher = list(map(lambda b: bigram_to_num(b), most_common_ciphertext))

    solutions = solve_linear_comparison(clear[0], clear[1], cipher[0], cipher[1])
    print(athens_bigram_decrypt(solutions[0][0], solutions[0][1], ciphertext))

if __name__ == "__main__":
    main()