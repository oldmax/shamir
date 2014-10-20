import random

ran = random.SystemRandom()

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
