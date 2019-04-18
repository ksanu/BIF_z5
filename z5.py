import hashlib
import binascii


def reduction(hex_hasz_x):
    return "452101" + hex_hasz_x[0:4]

#hasz(x) = pierwsze_56_bitów(MD5(MD5(x)))
def hasz(x):
    un_hex_x = binascii.unhexlify(x)#hex zmieniamy na string ascii
    x =un_hex_x
    md5_1 = hashlib.md5()
    md5_1.update(x)
    r = md5_1.digest()

    md5_2 = hashlib.md5()
    md5_2.update(r)
    r = md5_2.hexdigest()

    #first_56_bits = r[0:14]
   # return first_56_bits
    return r


# node -1 jeżeli nie istnieje
class Node:
    def __init__(self,number, my_hash):
        self.number = number
        self.my_hash = my_hash
        self.prev_nodes = list()
        self.next_nodes = list()


#x1 = 0x 452101fe10345a4c8b7d248649cfd
current_elem_number=0
n = Node(current_elem_number, hasz('452101fe10345a4c8b7d248649cfd'))
all_nodes = list()
all_nodes.append(n)


def getnextnode(current_node_number):
    current_node = all_nodes[current_node_number]
    if len(current_node.next_nodes) == 0:
        new_hash = hasz(current_node.my_hash)
        next_node_number = -1
        for n in all_nodes:
            if n.my_hash == new_hash:
                next_node_number = n.number
                n.prev_nodes.append(current_node.number)
        if next_node_number == -1:
            #dodajemy nowy
            current_node.next_nodes.append(len(all_nodes))
            new_node = Node(len(all_nodes), new_hash)
            new_node.prev_nodes.append(current_node.number)
            all_nodes.append(new_node)
        else:
            #dodajemy tylko wskaźnik na istniejący node
            current_node.next_nodes.append(next_node_number)

    return current_node.next_nodes[0]





def floyd(f, x0):
    # Main phase of algorithm: finding a repetition x_i = x_2i.
    # The hare moves twice as quickly as the tortoise and
    # the distance between them increases by 1 at each step.
    # Eventually they will both be inside the cycle and then,
    # at some point, the distance between them will be
    # divisible by the period λ.
    tortoise = f(x0)  # f(x0) is the element/node next to x0.
    hare = f(f(x0))
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(f(hare))

    print "Żółw złapał zająca. Poprzednie wierzchołki:"
    print all_nodes[hare].prev_nodes
    print "Node:\thasz:"
    for n in all_nodes[hare].prev_nodes:
        print("%d\t%s" % (n, all_nodes[n].my_hash))


floyd(getnextnode, 0)
