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
        while i < len(coeffs) and coeffs[i] == 0:
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

    def __call__(self, x, p):
        return sum([c*x**i % p for i, c in enumerate(self.coeffs[::-1])])

def interpolate(points, p):
    '''Accepts a list of tuples (x, f(x)) and returns an
       instance of Polynomial fit to those points'''
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    ls = [[] for i in xrange(len(points))]
    for i in xrange(len(points)):
        ran = range(len(points))
        ran.remove(i)
        tops, bottoms = [], []
        for j in ran:
            tops.append(Polynomial([1, -xs[j]]))
            bottoms.append(Polynomial([mod_inverse(xs[i] - xs[j], p)]))
        ls[i].extend([t*b for t, b in zip(tops, bottoms)])
    lprods = [reduce(Polynomial.__mul__, l) for l in ls]
    return reduce(Polynomial.__add__, [i*y for i, y in zip(lprods, [Polynomial([p]) for p in ys])])

def is_prime(p, iters = 50):
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

def get_prime(size_in_bits=2048):
    while True:
        p_p = ran.getrandbits(size_in_bits)
        if p_p % 2 == 0:
            p_p += 1
        if is_prime(p_p):
            return p_p

def generate_coeffs(p, k):
    return [ran.randint(1, p) for i in range(k - 1)]

def mod_inverse(n, p):
    n, i = n % p, 1
    while n > 1:
        q, n = p / n, p % n
        i = (-i * q) % p
    if n == 1:
        return i

def shamir(inp, n=5, k=3, size=2048):
    p = get_prime(size)
    coeffs = generate_coeffs(p, k)
    coeffs.append(inp)
    poly = Polynomial(coeffs)
    return [[(i, poly(i, p)) for i in range(1, n + 1)], p]

def unshamir(sham, k):
    points = set(sham[0])
    points = [points.pop() for i in range(k)]
    poly = interpolate(points, sham[1])
    return poly.coeffs[-1] % sham[1]
