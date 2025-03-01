# import numpy as np


def get_permutation_order(keyword):
    """Отримуємо порядок перестановки стовпців на основі ключового слова."""
    return sorted(range(len(keyword)), key=lambda x: keyword[x])


def encrypt_transposition(text, keyword):
    """Шифрування методом простої перестановки."""
    text = text.replace(" ", "~")  # Видаляємо пробіли
    key_length = len(keyword)
    order = get_permutation_order(keyword)

    # Додаємо заповнювачі '^', щоб текст ділився на довжину ключа
    while len(text) % key_length != 0:
        text += "^"

    # Формуємо матрицю (рядки по key_length символів)
    num_rows = len(text) // key_length
    matrix = [
        list(text[i * key_length : (i + 1) * key_length]) for i in range(num_rows)
    ]
    # Читаємо стовпці в порядку, заданому ключовим словом
    encrypted_text = "".join("".join(row[i] for row in matrix) for i in order)
    return encrypted_text


def decrypt_transposition(ciphertext, keyword):
    """Розшифрування методом простої перестановки."""
    key_length = len(keyword)
    order = get_permutation_order(keyword)

    num_rows = len(ciphertext) // key_length
    matrix = [[""] * key_length for _ in range(num_rows)]

    # Розподіляємо символи в стовпці згідно з порядком
    col = 0
    for i in order:
        for row in range(num_rows):
            matrix[row][i] = ciphertext[col]
            col += 1
    # Об'єднуємо рядки для отримання вихідного тексту
    decrypted_text = "".join("".join(row) for row in matrix)
    return decrypted_text.rstrip("^").replace("~", " ")  # Видаляємо заповнювачі


# Читання зашифрованого тексту з файлу
def read_plain_text(filename):
    with open(filename, "r") as file:
        return file.read()


plaintext_filename = "plaintext.txt"
keyword = "SECRET"
# plaintext = read_plain_text(plaintext_filename)

plaintext = "Theonlythingwehavetofears" # if need to add 5 more charachters
ciphertext = encrypt_transposition(plaintext, keyword)
decrypted_text = decrypt_transposition(ciphertext, keyword)

print(f"Зашифрований текст:\n {ciphertext}")
print(f"Розшифрований текст:\n {decrypted_text}")
