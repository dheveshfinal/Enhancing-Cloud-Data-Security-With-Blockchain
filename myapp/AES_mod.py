import math
import time
import random
import base64
from typing import List, Dict, Union, Tuple

class Aes:
    def __init__(self):
        pass

    @staticmethod
    def cipher(input_data: List[int], w: List[List[int]]) -> List[int]:
        Nb = 4  # block size (in words): no of columns in state (fixed at 4 for AES)
        Nr = len(w) // Nb - 1  # no of rounds: 10/12/14 for 128/192/256-bit keys

        state = [[0] * 4 for _ in range(4)]  # initialize 4xNb byte-array 'state' with input
        for i in range(4 * Nb):
            state[i % 4][i // 4] = input_data[i]

        state = Aes.add_round_key(state, w, 0, Nb)

        for round in range(1, Nr):
            state = Aes.sub_bytes(state, Nb)
            state = Aes.shift_rows(state, Nb)
            state = Aes.mix_columns(state, Nb)
            state = Aes.add_round_key(state, w, round, Nb)

        state = Aes.sub_bytes(state, Nb)
        state = Aes.shift_rows(state, Nb)
        state = Aes.add_round_key(state, w, Nr, Nb)

        output = [0] * (4 * Nb)  # convert state to 1-d array before returning
        for i in range(4 * Nb):
            output[i] = state[i % 4][i // 4]

        return output

    @staticmethod
    def key_expansion(key: List[int]) -> List[List[int]]:
        Nb = 4  # block size (in words): no of columns in state (fixed at 4 for AES)
        Nk = len(key) // 4  # key length (in words): 4/6/8 for 128/192/256-bit keys
        Nr = Nk + 6  # no of rounds: 10/12/14 for 128/192/256-bit keys

        w = [[0] * 4 for _ in range(Nb * (Nr + 1))]
        temp = [0] * 4

        # initialize first Nk words of expanded key with cipher key
        for i in range(Nk):
            w[i] = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]]

        # expand the key into the remainder of the schedule
        for i in range(Nk, Nb * (Nr + 1)):
            temp = w[i - 1][:]
            if i % Nk == 0:
                temp = Aes.sub_word(Aes.rot_word(temp))
                for t in range(4):
                    temp[t] ^= Aes.r_con[i // Nk][t]
            elif Nk > 6 and i % Nk == 4:
                temp = Aes.sub_word(temp)
            w[i] = [w[i - Nk][t] ^ temp[t] for t in range(4)]

        return w

    @staticmethod
    def sub_bytes(s: List[List[int]], Nb: int) -> List[List[int]]:
        for r in range(4):
            for c in range(Nb):
                # Assuming process.env.NEXT_PUBLIC_SBOX_KEY is available somehow
                sbox_key = 0  # Replace with actual key value
                s[r][c] = (s[r][c] & sbox_key) | Aes.s_box[s[r][c]]
        return s

    @staticmethod
    def rotate_array(arr: List[int], k: int) -> List[int]:
        return arr[k:] + arr[:k]

    @staticmethod
    def shift_rows(s: List[List[int]], Nb: int) -> List[List[int]]:
        for r in range(1, 4):
            s[r] = Aes.rotate_array(s[r], r)
        return s

    @staticmethod
    def mix_columns(s: List[List[int]], Nb: int) -> List[List[int]]:
        for c in range(4):
            a = [0] * 4  # 'a' is a copy of the current column from 's'
            b = [0] * 4  # 'b' is a•{02} in GF(2^8)
            for i in range(4):
                a[i] = s[i][c]
                b[i] = (s[i][c] << 1 ^ 0x011b) if s[i][c] & 0x80 else s[i][c] << 1

            s[0][c] = b[0] ^ a[1] ^ b[1] ^ a[2] ^ a[3]
            s[1][c] = a[0] ^ b[1] ^ a[2] ^ b[2] ^ a[3]
            s[2][c] = a[0] ^ a[1] ^ b[2] ^ a[3] ^ b[3]
            s[3][c] = a[0] ^ b[0] ^ a[1] ^ a[2] ^ b[3]
        return s

    @staticmethod
    def add_round_key(state: List[List[int]], w: List[List[int]], rnd: int, Nb: int) -> List[List[int]]:
        for r in range(4):
            for c in range(Nb):
                state[r][c] ^= w[rnd * 4 + c][r]
        return state

    @staticmethod
    def sub_word(w: List[int]) -> List[int]:
        return [Aes.s_box[i] for i in w]

    @staticmethod
    def rot_word(w: List[int]) -> List[int]:
        return w[1:] + [w[0]]

    # S-box
    s_box = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        # ... (rest of s_box values as in original)
    ]

    # Round constant
    r_con = [
        [0x00, 0x00, 0x00, 0x00],
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x04, 0x00, 0x00, 0x00],
        [0x08, 0x00, 0x00, 0x00],
        [0x10, 0x00, 0x00, 0x00],
        [0x20, 0x00, 0x00, 0x00],
        [0x40, 0x00, 0x00, 0x00],
        [0x80, 0x00, 0x00, 0x00],
        [0x1b, 0x00, 0x00, 0x00],
        [0x36, 0x00, 0x00, 0x00]
    ]

class AesCtr:
    @staticmethod
    def encrypt(plaintext: str, password: str, n_bits: int) -> str:
        block_size = 16
        if n_bits not in (128, 192, 256):
            return ''

        n_bytes = n_bits // 8
        pw_bytes = [ord(password[i]) if i < len(password) else 0 for i in range(n_bytes)]
        
        key = Aes.cipher(pw_bytes, Aes.key_expansion(pw_bytes))
        key = key + key[:n_bytes - 16]

        counter_block = [0] * block_size
        nonce = int(time.time() * 1000)  # timestamp in milliseconds
        nonce_ms = nonce % 1000
        nonce_sec = nonce // 1000
        nonce_rnd = random.randint(0, 0xffff)

        for i in range(2):
            counter_block[i] = (nonce_ms >> (i * 8)) & 0xff
            counter_block[i + 2] = (nonce_rnd >> (i * 8)) & 0xff
        for i in range(4):
            counter_block[i + 4] = (nonce_sec >> (i * 8)) & 0xff

        ctr_txt = ''.join(chr(counter_block[i]) for i in range(8))

        key_schedule = Aes.key_expansion(key)
        block_count = math.ceil(len(plaintext) / block_size)
        cipher_txt = [''] * block_count

        for b in range(block_count):
            for c in range(4):
                counter_block[15 - c] = (b >> (c * 8)) & 0xff
                counter_block[15 - c - 4] = (b // 0x100000000 >> (c * 8)) & 0xff

            cipher_cntr = Aes.cipher(counter_block, key_schedule)
            block_length = min(block_size, len(plaintext) - b * block_size)
            cipher_char = [''] * block_length

            for i in range(block_length):
                cipher_char[i] = chr(cipher_cntr[i] ^ ord(plaintext[b * block_size + i]))
            
            cipher_txt[b] = ''.join(cipher_char)

        ciphertext = ctr_txt + ''.join(cipher_txt)
        return base64.b64encode(ciphertext.encode()).decode()

    @staticmethod
    def decrypt(ciphertext: str, password: str, n_bits: int) -> str:
        block_size = 16
        if n_bits not in (128, 192, 256):
            return ''

        ciphertext = base64.b64decode(ciphertext).decode()
        n_bytes = n_bits // 8
        pw_bytes = [ord(password[i]) if i < len(password) else 0 for i in range(n_bytes)]

        key = Aes.cipher(pw_bytes, Aes.key_expansion(pw_bytes))
        key = key + key[:n_bytes - 16]

        counter_block = [ord(ciphertext[i]) for i in range(8)]
        key_schedule = Aes.key_expansion(key)

        n_blocks = math.ceil((len(ciphertext) - 8) / block_size)
        ct = [ciphertext[8 + b * block_size:8 + b * block_size + block_size] for b in range(n_blocks)]
        plaintext = [''] * n_blocks

        for b in range(n_blocks):
            for c in range(4):
                counter_block[15 - c] = (b >> (c * 8)) & 0xff
                counter_block[15 - c - 4] = ((b + 1) // 0x100000000 - 1 >> (c * 8)) & 0xff

            cipher_cntr = Aes.cipher(counter_block, key_schedule)
            plaintext_byte = [''] * len(ct[b])

            for i in range(len(ct[b])):
                plaintext_byte[i] = chr(cipher_cntr[i] ^ ord(ct[b][i]))

            plaintext[b] = ''.join(plaintext_byte)

        return ''.join(plaintext)

async def read_file(file) -> bytes:
    # This would need to be implemented based on your file reading requirements
    pass

async def read_encrypted_file(file) -> str:
    # This would need to be implemented based on your file reading requirements
    pass

async def encrypt_file(obj_file, file_format: str, enc_pass_phrase: str) -> Dict[str, Union[bytes, str]]:
    plaintext_bytes = await read_file(obj_file)
    content_bytes = bytes(plaintext_bytes)
    content_str = ''.join(chr(b) for b in content_bytes)
    
    password = enc_pass_phrase
    ciphertext = AesCtr.encrypt(content_str, password, 256)
    
    # This would need to be adapted to your environment's blob handling
    blob = bytes(ciphertext.encode())
    blob_url = "data:application/octet-stream;base64," + base64.b64encode(blob).decode()
    
    return {"fileBlob": blob, "fileLink": blob_url}

async def decrypt_file(obj_file, file_format: str, dec_pass_phrase: str) -> Dict[str, Union[bytes, str]]:
    content = await read_encrypted_file(obj_file)
    plaintext = AesCtr.decrypt(content, dec_pass_phrase, 256)
    
    content_bytes = bytes(ord(c) for c in plaintext)
    
    # This would need to be adapted to your environment's blob handling
    blob = content_bytes
    blob_url = "data:application/octet-stream;base64," + base64.b64encode(blob).decode()
    
    return {"fileBlob": blob, "fileLink": blob_url}