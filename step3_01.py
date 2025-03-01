import string


def generate_cipher_table(keyword):
    alphabet = string.ascii_uppercase.replace("J", "")  # Виключаємо 'J'
    key_letters = "".join(
        sorted(set(keyword), key=keyword.index)
    )  # Видаляємо дублікати, зберігаючи порядок
    remaining_letters = "".join([c for c in alphabet if c not in key_letters])
    cipher_table = key_letters + remaining_letters
    return cipher_table


def split_text(text):
    text = text.replace("J", "I").upper()
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if a not in string.ascii_uppercase:
            pairs.append(a)
            i += 1
            continue
        if i + 1 < len(text):
            b = text[i + 1]
            if b not in string.ascii_uppercase:
                pairs.append(a + "X")
                pairs.append(b)
                i += 2
            elif a == b:
                pairs.append(a + "X")
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:
            pairs.append(a + "X")
            i += 1

    if len(pairs[-1]) == 1 and pairs[-1] not in string.ascii_uppercase:
        pairs[-1] = pairs[-1] + "X"

    return pairs


def playfair_encrypt(text, keyword):
    cipher_table = generate_cipher_table(keyword)
    text_pairs = split_text(text)
    encrypted_text = ""

    for pair in text_pairs:
        if len(pair) == 1:
            encrypted_text += pair
            continue

        a, b = pair
        if a not in cipher_table:
            encrypted_text += a
            continue
        if b not in cipher_table:
            encrypted_text += b
            continue

        row_a, col_a = divmod(cipher_table.index(a), 5)
        row_b, col_b = divmod(cipher_table.index(b), 5)

        if row_a == row_b:
            encrypted_text += cipher_table[row_a * 5 + (col_a + 1) % 5]
            encrypted_text += cipher_table[row_b * 5 + (col_b + 1) % 5]
        elif col_a == col_b:
            encrypted_text += cipher_table[((row_a + 1) % 5) * 5 + col_a]
            encrypted_text += cipher_table[((row_b + 1) % 5) * 5 + col_b]
        else:
            encrypted_text += cipher_table[row_a * 5 + col_b]
            encrypted_text += cipher_table[row_b * 5 + col_a]

    return encrypted_text


def playfair_decrypt(encrypted_text, keyword):
    cipher_table = generate_cipher_table(keyword)
    text_pairs = split_text(encrypted_text)
    decrypted_text = ""

    for pair in text_pairs:
        if len(pair) == 1:
            decrypted_text += pair
            continue

        a, b = pair
        if a not in cipher_table:
            decrypted_text += a
            continue
        if b not in cipher_table:
            decrypted_text += b
            continue

        row_a, col_a = divmod(cipher_table.index(a), 5)
        row_b, col_b = divmod(cipher_table.index(b), 5)

        if row_a == row_b:
            decrypted_text += cipher_table[row_a * 5 + (col_a - 1) % 5]
            decrypted_text += cipher_table[row_b * 5 + (col_b - 1) % 5]
        elif col_a == col_b:
            decrypted_text += cipher_table[((row_a - 1) % 5) * 5 + col_a]
            decrypted_text += cipher_table[((row_b - 1) % 5) * 5 + col_b]
        else:
            decrypted_text += cipher_table[row_a * 5 + col_b]
            decrypted_text += cipher_table[row_b * 5 + col_a]

    # Видаляємо додані символи 'X', які були додані для парності, лише якщо вони не зустрічаються між двома однаковими літерами
    decrypted_text = decrypted_text.replace("X", "")
    return decrypted_text.replace("X", "")


# Читання зашифрованого тексту з файлу
def read_plain_text(filename):
    with open(filename, "r") as file:
        return file.read()


plaintext_filename = "plaintext.txt"
text = read_plain_text(plaintext_filename)
# text = "The artist is the creator of beautiful things."
keyword = "MATRIX"
encrypted_text = playfair_encrypt(text, keyword)
print(f"Encrypted Text:\n {encrypted_text}")
decrypted_text = playfair_decrypt(encrypted_text, keyword)
print(f"Decrypted Text:\n {decrypted_text}")
