import random

# verifica se um número é primo
# utilizado para gerar os números primos 'p' e 'q do rsa
def is_prime(n):
    if n <= 1: return False

    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False

    return True

# calcula o máximo divisor comum entre 'a' e 'b'
# usado para garantir que 'e' e 'phi' sejam coprimos
def gcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a

# calcula o inverso modular de 'a' em relação a 'm'
# esse passo é essencial para encontrar o expoente privado 'd'
def modinv(a, m):
    m0, x0, x1 = m, 0, 1

    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0

    return x1 + m0 if x1 < 0 else x1

# gera um par de chaves rsa (pública e privada)
def generate_keys():
    # seleciona números primos dentro de um intervalo
    primes = [i for i in range(100, 300) if is_prime(i)]
    p = random.choice(primes)
    q = random.choice(primes)

    # como os primos são relativamente pequenos (100 a 300), este código é apenas didático e não seguro para uso real

    while q == p: # garante que 'p' e 'q' sejam diferentes
        q = random.choice(primes)

    n = p * q
    phi = (p - 1) * (q - 1)

    # escolhe 'e' aleatório que seja coprimo de 'phi'
    e = random.randrange(2, phi)

    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # calcula o inverso modular para obter 'd'
    d = modinv(e, phi)
    
    return ((e, n), (d, n))

# criptografa uma mensagem usando a chave pública do destinatário
def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

# descriptografa uma mensagem usando a chave privada do destinatário
def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])
