from math import gcd
from collections import namedtuple


def bezout(m, n):
    if n == 0:
        return 1, 0
    u, v = bezout(n, m % n)
    return v, u - (m // n) * v


def Sdual_theory(N, m, n):
    u, v = bezout(m, n)
    mp = N // gcd(m, n)
    return mp, (-v * N // m) % mp


def Tdual_theory(N, m, n):
    return m, (n + N // m) % m


def Sdual_sublattice(N, d, t):
    return Sdual_theory(N, d, t)


def Tdual_sublattice(N, d, t):
    return d, (t - N // d) % d


def no_dual(N, m, n):
    return m, n


def Sdual_point(p):
    a, b = p
    return b, -a


def Tdual_point(p):
    a, b = p
    return a - b, b


def no_dual_point(p):
    return p


Duality = namedtuple('Duality', ['theory', 'sublattice', 'point', 'name'])
Sduality = Duality(Sdual_theory, Sdual_sublattice, Sdual_point, 'S-duality')
Tduality = Duality(Tdual_theory, Tdual_sublattice, Tdual_point, 'T-duality')
no_duality = Duality(no_dual, no_dual, no_dual_point, 'Normal')
