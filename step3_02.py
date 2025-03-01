def vigenere_encrypt(plaintext, key):
    encrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord("A")
            if char.isupper():
                encrypted_char = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            else:
                encrypted_char = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text


def create_table(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    table = []
    for char in key.upper():
        if char not in table and char != "J":
            table.append(char)
    for char in alphabet:
        if char not in table:
            table.append(char)
    return table


def playfair_encrypt(plaintext, table):
    def get_position(char):
        index = table.index(char)
        return index // 5, index % 5

    encrypted_text = ""
    plaintext = (
        plaintext.upper()
        .replace("J", "I")
        .replace(" ", "")
        .replace(".", "")
        .replace("'", "")
        .replace(",", "")
        .replace("-", "")
    )
    if len(plaintext) % 2 != 0:
        plaintext += "X"

    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i + 1]
        row_a, col_a = get_position(a)
        row_b, col_b = get_position(b)

        if row_a == row_b:
            encrypted_text += table[row_a * 5 + (col_a + 1) % 5]
            encrypted_text += table[row_b * 5 + (col_b + 1) % 5]
        elif col_a == col_b:
            encrypted_text += table[((row_a + 1) % 5) * 5 + col_a]
            encrypted_text += table[((row_b + 1) % 5) * 5 + col_b]
        else:
            encrypted_text += table[row_a * 5 + col_b]
            encrypted_text += table[row_b * 5 + col_a]

    return encrypted_text


# Читання зашифрованого тексту з файлу
def read_plain_text(filename):
    with open(filename, "r") as file:
        return file.read()


plaintext_filename = "plaintext.txt"
plaintext = read_plain_text(plaintext_filename)

vigenere_key = "KEY"
playfair_key = "CRYPTO"


vigenere_encrypted = vigenere_encrypt(plaintext, vigenere_key)
print(f"Vigenere Encrypted:\n {vigenere_encrypted}")

playfair_table = create_table(playfair_key)
playfair_encrypted = playfair_encrypt(vigenere_encrypted, playfair_table)
playfair_encrypted += "."  # Додаємо крапку назад до зашифрованого тексту
print(f"Playfair Encrypted: {playfair_encrypted}")
