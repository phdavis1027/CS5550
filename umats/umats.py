'''
@authors: Phillip Davis and Logan Richardson, 2022


'''

from itertools import chain, combinations
from time import sleep

coloring = 0

def powerset(s):
    s = list(s)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def main():
    m = 10
    combos = sorted(list(powerset({i for i in range(1,m + 1)})), key=len)
    umat = { (j, i) : 0 for i in range(2, m) for j in range(1, i) }
    sorted_key_list = sorted(umat.keys(), key=len)
    for i in range(1 << 36):
        gen_coloring(umat, sorted_key_list) 
        if check_combos(combos, umat):
            print(f"umat {umat} has no unicolored sets of size 3")


def gen_coloring(umat, keys):
    global coloring
    #change color formatting for higher values of m
    c = list("{:036b}".format(coloring)) 
    for key, color in zip(keys, c):
        umat[key] = int(color)
    coloring += 1
        

def check_combos(combos, umat) -> bool:
    for combo in combos[56:125]:
        sum = 0
        for i, first in enumerate(combo[:(len(combo) - 1)]): #(1,2,3)
            for j, second in enumerate(combo[i + 1:]):
                sum += umat[first,second]
        if sum == 3 or sum == 0:
            return False
    return True
    


if __name__ == "__main__":
    main()