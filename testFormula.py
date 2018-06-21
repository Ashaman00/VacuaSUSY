from math import gcd
from dualities import *
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(l):
        for elt in l:
            yield elt

# Conditions :
# N >= 2
# m divides N
# 0 <= n <= m-1
# d divides N
# 0 <= t <= d-1


def gcds(*args):
    if len(args) == 0:
        return 0
    la = list(args)
    while len(la) != 1:
        a, b = la.pop(), la.pop()
        la.append(gcd(a, b))
    return la[0]


def divisors(nb):
    for i in range(1, nb):
        if nb % i == 0:
            yield i
    yield nb


def e1(N, m, n, d, t):
    return gcds(d, m, N // d, N // m, t, n)


def e1e2(N, m, n, d, t):
    return gcds(N * m // d, N * d // m, N * t // m + N * n // d)


def all_theories(Nmax):
    for N in tqdm(range(2, Nmax + 1)):
        for m in divisors(N):
            for n in range(m):
                yield N, m, n


def all_sublattices(N):
    for d in divisors(N):
        for t in range(d):
            yield d, t


def verify_duality(dual=Sduality):
    ok = True
    for N, m, n in all_theories(30):
        for d, t in all_sublattices(N):
            lhs = e1e2(N, m, n, d, t)
            rhs = e1e2(N, *dual.theory(N, m, n), *dual.sublattice(N, d, t))
            lhs2 = e1(N, m, n, d, t)
            rhs2 = e1(N, *dual.theory(N, m, n), *dual.sublattice(N, d, t))
            if lhs != rhs or lhs2 != rhs2:
                print(f'Error N={N}, m={m}, n={n}, d={d}, t={t}')
                ok = False
    if ok:
        print('No errors')


def get_sum(N, m, n):
    res = {}
    for d, t in all_sublattices(N):
        ve1e2 = e1e2(N, m, n, d, t)
        ve1 = e1(N, m, n, d, t)
        try:
            res[(ve1, ve1e2 // ve1)] += ve1e2
        except KeyError:
            res[(ve1, ve1e2 // ve1)] = ve1e2
    return res


def verify_duality_sum(duality=Sduality):
    ok = True
    for N, m, n in all_theories(30):
        res = get_sum(N, m, n)
        res_dual = get_sum(N, *duality.theory(N, m, n))
        if res != res_dual:
            print(f'Error at N={N}')
            print(res)
            print(res_dual)
            ok = False
    if ok:
        print('No errors')


# verify_duality()
# verify_duality(Tduality)

# verify_duality_sum()
# verify_duality_sum(Tduality)
