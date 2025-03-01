def get_permutation_order(keyword):
    """Отримуємо порядок перестановки для ключа"""
    return sorted(range(len(keyword)), key=lambda x: keyword[x])

def create_matrix(text, rows, cols, fill_char="^"):
    """Створює матрицю з тексту, заповнюючи порожні місця '^'."""
    matrix = [list(text[i * cols:(i + 1) * cols]) for i in range(rows)]
    while len(matrix[-1]) < cols:
        matrix[-1].append(fill_char)
    return matrix

def encrypt_double_transposition(text, key1, key2):
    """Шифрування подвійною перестановкою"""
    text = text.replace(" ", "~")  # Видаляємо пробіли
    key1_order = get_permutation_order(key1)
    key2_order = get_permutation_order(key2)

    cols = len(key1)
    rows = -(-len(text) // cols)  # Округлення вгору
    matrix = create_matrix(text, rows, cols)

    # 1. Переставляємо стовпці за key1
    transposed_matrix = [[row[i] for i in key1_order] for row in matrix]

    # 2. Переставляємо рядки за key2 (забезпечуємо коректний розмір)
    sorted_row_indices = sorted(range(rows), key=lambda x: key2_order[x % len(key2_order)])
    final_matrix = [transposed_matrix[i] for i in sorted_row_indices]

    encrypted_text = ''.join(''.join(row) for row in final_matrix)
    return encrypted_text

def decrypt_double_transposition(ciphertext, key1, key2):
    """Розшифрування подвійною перестановкою"""
    key1_order = get_permutation_order(key1)
    key2_order = get_permutation_order(key2)

    cols = len(key1)
    rows = -(-len(ciphertext) // cols)  # Округлення вгору
    matrix = [[''] * cols for _ in range(rows)]

    # 1. Відновлюємо порядок рядків (відповідно до перестановки)
    sorted_row_indices = sorted(range(rows), key=lambda x: key2_order[x % len(key2_order)])
    reverse_row_order = {old: new for old, new in enumerate(sorted_row_indices)}

    # 2. Заповнюємо матрицю зашифрованим текстом
    index = 0
    for i in range(rows):
        for j in range(cols):
            matrix[reverse_row_order[i]][j] = ciphertext[index]
            index += 1

    # 3. Відновлюємо порядок стовпців
    decrypted_matrix = [[row[i] for i in sorted(range(cols), key=lambda x: key1_order[x])] for row in matrix]
    decrypted_text = ''.join(''.join(row) for row in decrypted_matrix)
    return decrypted_text.rstrip("^").replace("~"," ")  # Видаляємо зайві 'X'

# Читання зашифрованого тексту з файлу
def read_plain_text(filename):
    with open(filename, "r") as file:
        return file.read()
    
# Приклад використання алгоритму для довгого тексту
key1 = "SECRET"
key2 = "CRYPTO"

plaintext_filename = "plaintext.txt"
plaintext = read_plain_text(plaintext_filename)

ciphertext = encrypt_double_transposition(plaintext, key1, key2)
decrypted_text = decrypt_double_transposition(ciphertext, key1, key2)

print(f"Зашифрований текст:\n {ciphertext}")
print(f"Розшифрований текст:\n {decrypted_text}")
