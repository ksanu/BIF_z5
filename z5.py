import hashlib
import binascii


def reduction(hex_hasz_x):
    return "452101" + hex_hasz_x

#hasz(x) = pierwsze_56_bitów(MD5(MD5(x)))
def hasz(x):
    un_hex_x = binascii.unhexlify(x)#hex zmieniamy na ascii(binarna reprezentacja)
    md5_1 = hashlib.md5()
    md5_1.update(un_hex_x)
    r = md5_1.digest()

    md5_2 = hashlib.md5()
    md5_2.update(r)
    r2 = md5_2.hexdigest()

    first_56_bits = r2[0:14]
    #first_16_bits = r2[0:4]
    return first_56_bits
    #return r2


def next_hasz(x):
    x_in = reduction(x)
    hasz_out = hasz(x_in)
    return x_in, hasz_out

def floyd(f, x0):
    # Main phase of algorithm: finding a repetition x_i = x_2i.
    # The hare moves twice as quickly as the tortoise and
    # the distance between them increases by 1 at each step.
    # Eventually they will both be inside the cycle and then,
    # at some point, the distance between them will be
    # divisible by the period λ.
    x_in_t, tortoise = f(x0)  # f(x0) is the element/node next to x0.
    x_in_h, hare_step1 = f(x0)
    x_in_h, hare_step2 = f(hare_step1)
    while tortoise != hare_step2:
        x_in_t, tortoise = f(tortoise)
        x_in_h, hare_step1 = f(hare_step2)
        x_in_h, hare_step2 = f(hare_step1)

    # At this point the tortoise position, ν, which is also equal
    # to the distance between hare and tortoise, is divisible by
    # the period λ. So hare moving in circle one step at a time,
    # and tortoise (reset to x0) moving towards the circle, will
    # intersect at the beginning of the circle. Because the
    # distance between them is constant at 2ν, a multiple of λ,
    # they will agree as soon as the tortoise reaches index μ.

    # Find the position μ of first repetition.
    mu = 0
    tortoise = x0
    while tortoise != hare_step2:
        x_in_t, tortoise = f(tortoise)
        x_in_h, hare_step2 = f(hare_step2)  # Hare and tortoise move at same speed
        mu += 1

    print("Żółw złapał zająca.\nX1: ")
    print(x_in_t)
    print("\nX2: ")
    print(x_in_h)
    print("\nŻółw = Zając:")
    print(tortoise)
    print(hare_step2)

    # Find the length of the shortest cycle starting from x_μ
    # The hare moves one step at a time while tortoise is still.
    # lam is incremented until λ is found.
    lam = 1
    x_in_h, hare = f(tortoise)
    while tortoise != hare:
        x_in_h, hare = f(hare)
        lam += 1

    return lam, mu


#lam - długość cyklu, mu - pozycja
lam, mu = floyd(next_hasz, "66597ea2e4fe91a8747a022900")
print("lam, mu:")
print (lam, mu)

"""
Żółw złapał zająca.
X1:
452101d7d91a3a2eb09e

X2:
452101fcb52efeb25310

Żółw = Zając:
b8e5178c4598ce
b8e5178c4598ce
lam, mu:
92041718 498545622
"""