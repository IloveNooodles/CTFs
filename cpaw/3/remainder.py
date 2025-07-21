from Cryptodome.Util.number import inverse
# x ≡ 32134 (mod 1584891)
# x ≡ 193127 (mod 3438478)

a1, m1 = 32134, 1584891
a2, m2 = 193127, 3438478

M = m1 * m2
M1 = M // m1
M2 = M // m2

inv1 = inverse(M1, m1)
inv2 = inverse(M2, m2)

x = (a1 * M1 * inv1 + a2 * M2 * inv2) % M
print(x)
