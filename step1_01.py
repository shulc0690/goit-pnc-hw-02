def generate_vigenere_table():
    table = []
    for i in range(26):
        row = [(chr(((i + j) % 26) + 65)) for j in range(26)]
        table.append(row)
    return table


def vigenere_encrypt(plain_text, key):
    table = generate_vigenere_table()
    key = key.upper()
    encrypted_text = ""

    key_len = len(key)
    key_index = 0

    for char in plain_text:
        if char.isalpha():
            row = ord(key[key_index % key_len]) - 65
            col = ord(char.upper()) - 65
            encrypted_char = table[row][col]
            if char.islower():
                encrypted_char = encrypted_char.lower()
            encrypted_text += encrypted_char
            key_index += 1
        else:
            encrypted_text += char

    return encrypted_text


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


# Читання початкового тексту з файлу
def read_plain_text(filename):
    with open(filename, "r") as file:
        return file.read()


# Запис зашифрованого тексту у файл
def write_encrypted_text(filename, encrypted_text):
    with open(filename, "w") as file:
        file.write(encrypted_text)


# Запис розшифрованого тексту у файл
def write_decrypted_text(filename, decrypted_text):
    with open(filename, "w") as file:
        file.write(decrypted_text)


# Приклад використання
plain_text_filename = "plaintext.txt"
encrypted_text_filename = "encrypted.txt"
decrypted_text_filename = "decrypted.txt"
key = "CRYPTOGRAPHY"

# Читаємо початковий текст з файлу
plain_text = read_plain_text(plain_text_filename)

# Шифруємо текст
encrypted_text = vigenere_encrypt(plain_text, key)
write_encrypted_text(encrypted_text_filename, encrypted_text)

# Розшифровуємо текст
decrypted_text = vigenere_decrypt(encrypted_text, key)
write_decrypted_text(decrypted_text_filename, decrypted_text)

print(f"Cipher text:\n {encrypted_text}")
print(f"Plain text:\n {decrypted_text}")
