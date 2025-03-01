from collections import Counter
import re


def kasiski_examination(cipher_text):
    repeats = {}
    for i in range(len(cipher_text) - 2):
        trigram = cipher_text[i : i + 3]
        if trigram in repeats:
            repeats[trigram].append(i)
        else:
            repeats[trigram] = [i]

    distances = []
    for indices in repeats.values():
        if len(indices) > 1:
            for i in range(len(indices) - 1):
                distances.append(indices[i + 1] - indices[i])

    common_factors = {}
    for distance in distances:
        for i in range(2, distance):
            if distance % i == 0:
                if i in common_factors:
                    common_factors[i] += 1
                else:
                    common_factors[i] = 1

    likely_key_lengths = [
        k
        for k, v in sorted(
            common_factors.items(), key=lambda item: item[1], reverse=True
        )
    ]
    return likely_key_lengths


def calculate_ic(text):
    n = len(text)
    frequency = Counter(text)
    ic = sum(f * (f - 1) for f in frequency.values()) / (n * (n - 1))
    return ic


def friedman_test(cipher_text):
    n = len(cipher_text)
    freq = Counter(cipher_text)

    numerator = sum(f * (f - 1) for f in freq.values())
    denominator = n * (n - 1)
    ic = numerator / denominator

    expected_ic_random = 1 / 26
    expected_ic_english = 0.068

    key_length_estimate = (expected_ic_english - expected_ic_random) / (
        ic - expected_ic_random
    )
    return round(key_length_estimate)


def split_text_by_key_length(text, key_length):
    return [
        "".join([text[i] for i in range(j, len(text), key_length)])
        for j in range(key_length)
    ]


def get_most_frequent_letter(text):
    frequency = Counter(text)
    most_common_letter, _ = frequency.most_common(1)[0]
    return most_common_letter


def find_key(cipher_text, key_length):
    cipher_text_split = split_text_by_key_length(cipher_text, key_length)
    key = ""
    for part in cipher_text_split:
        most_common_letter = get_most_frequent_letter(part)
        shift = (ord(most_common_letter) - ord("E")) % 26
        key += chr(65 + shift)
    return key


def vigenere_decrypt(cipher_text, key):
    table = generate_vigenere_table()
    key = key.upper()
    decrypted_text = ""

    key_len = len(key)
    key_index = 0

    for char in cipher_text:
        if char.isalpha():
            row = ord(key[key_index % key_len]) - 65
            col = table[row].index(char.upper())
            decrypted_char = chr(col + 65)
            if char.islower():
                decrypted_char = decrypted_char.lower()
            decrypted_text += decrypted_char
            key_index += 1
        else:
            decrypted_text += char

    return decrypted_text


def generate_vigenere_table():
    table = []
    for i in range(26):
        row = [(chr(((i + j) % 26) + 65)) for j in range(26)]
        table.append(row)
    return table


# Читання зашифрованого тексту з файлу
def read_cipher_text(filename):
    with open(filename, "r") as file:
        return file.read()


cipher_text_filename = "encrypted.txt"

# Читаємо зашифрований текст з файлу
cipher_text = read_cipher_text(cipher_text_filename)
# Застосування методу Касіскі для визначення ймовірної довжини ключа
likely_key_lengths = kasiski_examination(cipher_text)
print(f"Posible lenth of key: {likely_key_lengths}")

# Застосування тесту Фрідмана для оцінки довжини ключа
estimated_key_length = friedman_test(cipher_text)
print(f"Posible lenth of key: {estimated_key_length}")

# Знаходження ключа на основі ймовірної довжини ключа
if likely_key_lengths:
    key_length = likely_key_lengths[0]
else:
    key_length = estimated_key_length

key = find_key(cipher_text, key_length)
print(f"Secret key: {key}")

# Розшифрування тексту за допомогою знайденого ключа
decrypted_text = vigenere_decrypt(cipher_text, key)
print(f"Plain text: {decrypted_text}")
