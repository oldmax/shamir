import random
from fractions import gcd

ran = random.SystemRandom()

class Polynomial(object):
    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.simplify()

    @classmethod
    def list_simplify(self, coeffs):
        i = 0
        while coeffs[i] == 0:
            i += 1
        return coeffs[i:]

    def pad(self, c_1, c_2):
        diff = len(c_1) - len(c_2)
        if diff < 0:
            return ([0]*abs(diff) + c_1, c_2)
        if diff > 0:
            return (c_1, [0]*diff + c_2)
        return (c_1[::], c_2[::])   

    def simplify(self):
        self.coeffs = Polynomial.list_simplify(self.coeffs)

    def __mul__(self, other):
        cs_1, cs_2 = self.pad(self.coeffs, other.coeffs)
        out = [0]*(len(cs_1) + len(cs_2))
        for i_1, c_1 in enumerate(cs_1):
            for i_2, c_2 in enumerate(cs_2):
                out[i_1 + i_2 + 1] += c_1*c_2
        out = Polynomial.list_simplify(out)
        return Polynomial(out)

    def __add__(self, other):
        cs_1, cs_2 = self.pad(self.coeffs, other.coeffs)
        return Polynomial([i + j for i, j in zip(cs_1, cs_2)])

def is_prime(p, iters = 40):
    for i in xrange(iters):
        x = ran.randint(2, p - 1)
        s, d = 0, p - 1
        while d % 2 == 0:
            s += 1
            d /= 2
        if pow(x, d, p) != 1:
            for r in xrange(s):
                if pow(x, pow(2, r)*d, p) == p - 1:
                    break
            else:
                return False
    return True

def generate_coeffs(p, m):
    return (ran.randint(1, p) for i in range(m - 1))

def mod_inverse(n, p):
    n, i = n % p, 1
    while n > 1:
        q, n = p / n, p % n
        i = (-i * q) % p
    if n == 1:
        return i
