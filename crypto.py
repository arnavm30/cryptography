import string
import math
import random

# ASCII codes for A and Z
ascii_A = ord('A')
ascii_Z = ord('Z')
num_letters = len(string.ascii_uppercase)

def shift_ch(ch, offset):
    ascii_ch = ord(ch)
    # Check whether ASCII code of ch falls within range of alphabetic characters
    if ascii_A <= ascii_ch <= ascii_Z:
        ascii_ch += offset
        # Check whether to wrap around
        if ascii_ch > ascii_Z:
            ascii_ch -= num_letters
        
    # Convert ASCII code back to a character
    return chr(ascii_ch)

# Caesar Cipher
# Arguments: string, integer
# Returns: string
def encrypt_caesar(plaintext, offset):
    # modulus applied to remove excess shifting
    offset %= num_letters

    return ''.join([shift_ch(ch, offset) for ch in plaintext])

# Arguments: string, integer
# Returns: string
def decrypt_caesar(ciphertext, offset):
    # -offset used to undo offset that shifted plaintext to ciphertext
    return encrypt_caesar(ciphertext, -offset)

# Vigenere Cipher
# Arguments: string, string
# Returns: string
def encrypt_vigenere(plaintext, keyword):
    # new_keyword made to match length of plaintext
    new_keyword = math.ceil(len(plaintext)/len(keyword)) * keyword
    new_keyword = new_keyword[:len(plaintext)]

    # Subtracting ASCII code of each character by ASCII code of A to get offset
    # of each character for shift_ch
    return ''.join([shift_ch(plaintext[i], ord(new_keyword[i]) - ascii_A) 
                    for i in range(len(plaintext))])

# Arguments: string, string
# Returns: string
def decrypt_vigenere(ciphertext, keyword):
    # Finding the numerical offset (ascii_Z + 1 - ord(ch)) that undoes the offset
    # applied to plaintext to get ciphertext for each character, then adding ascii_A to 
    # get the offset as an ASCII code, which gets converted to an alphabetic character 
    new_keyword = ''.join([chr(ascii_Z + 1 - ord(ch) + ascii_A)
                           for ch in keyword])

    return encrypt_vigenere(ciphertext, new_keyword)

def coprime(Q):
    R = random.randint(2, Q - 1)
    while math.gcd(R, Q) != 1:
        R = random.randint(2, Q - 1)

    return R

# Merkle-Hellman Knapsack Cryptosystem
# Arguments: integer
# Returns: tuple (W, Q, R) - W a length-n tuple of integers, Q and R both integers
def generate_private_key(n=8):
    W = [random.randint(1, 5)]
    for _ in range(n):
        W.append(random.randint(sum(W) + 1, sum(W) * 2))
    Q = W.pop()
    W = tuple(W)
    R = coprime(Q)

    return (W, Q, R)

# Arguments: tuple (W, Q, R) - W a length-n tuple of integers, Q and R both integers
# Returns: B - a length-n tuple of integers
def create_public_key(private_key):
    W, Q, R = private_key
    B = tuple([(R * w) % Q for w in W])

    return B

# Arguments: string, tuple B
# Returns: list of integers
def encrypt_mhkc(plaintext, public_key):
    C = []
    for M in plaintext:
        # [2:] to slice off '0b' prefix of string returned by bin()
        # zfill pads 0s to beginning to ensure len(str) = 8
        bits = [int(i) for i in bin(ord(M))[2:].zfill(8)]
        C.append(sum([bits[i] * public_key[i]
                      for i in range(len(public_key))]))

    return C

def mod_inverse(R, Q):
    for S in range(2, Q):
        if (R * S) % Q == 1:
            return S

    return None

# Arguments: list of integers, private key (W, Q, R) with W a tuple.
# Returns: bytearray or str of plaintext
def decrypt_mhkc(ciphertext, private_key):
    W, Q, R = private_key
    S = mod_inverse(R, Q)
    decrypted = ''

    for C in ciphertext:
        C_p = (C * S) % Q
        C_p_decrypted = []

        for w in reversed(W):
            if w <= C_p:
                C_p_decrypted.append('1')
                C_p -= w
            else:
                C_p_decrypted.append('0')
        decrypted += chr(int(''.join(reversed(C_p_decrypted)), 2))

    return decrypted

def main():
    # Testing code here
    pass

if __name__ == "__main__":
    main()