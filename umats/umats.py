'''
@authors: Phillip Davis and Logan Richardson, 2022


'''

from copy import deepcopy
from gettext import find
from tkinter import W
import click

from itertools import chain, combinations
from time import sleep
from math import comb, e, pow
from random import randrange, choice, random


class Number:
    def __init__(self) -> None:
        self.val = 0

def powerset(s):
    s = list(s)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def gen_combos(m):
    return sorted(list(powerset({i for i in range(1,m + 1)})), key=len)

def gen_umat(m):
    return { (j, i) : 0 for i in range(2, m + 1) for j in range(1, i) }

def main():
    choose_method()

'''
checks by brute force whether there exists any uni-colored sets of size k
over a given coloring of a given upper-m matrix

'''

@click.command()
@click.option("--method")
def choose_method(method):
    if method not in {"anneal", "brute", "check"}:
        click.UsageError("USAGE: method must be 'anneal,' 'brute,' or 'check' ")

    m = click.prompt("Please enter a size configuration: ", type=int)    
    configs = gen_configs(m)

    k = click.prompt("What size k are we trying to exclude?", type=int)


    if method == "check":
        coloring = click.prompt("Please enter a binary string to apply as a coloring", type=str)
        coloring = coloring[::-1] 
                                # for some reason you can
                                # reverse a string in python
                                # this way
        if len(coloring) > find_shift_len(m):
            click.BadParameter("Coloring is not the same size as the m-matrix.")

        # this is really stupid
        # first sorts by first coordinate
        # then sorts by second coordinate
        # so the coloring can be applied in a uniform way
        sorted_keys = sorted(sorted(configs[0].keys(), key = lambda i: i[len(i) - 1]), key = lambda i: i[:-1])
        apply_str_coloring(configs[0], sorted_keys, coloring)

        if check_combos(configs[1], configs[0], k):
            click.secho(f"There are no unicolored sets of size {k} over the m-matrix!", fg="green")

    if method == "brute":
        brute_force(configs[0], configs[1], m, k)
    if method == "anneal":
        sorted_keys = sorted(sorted(configs[0].keys(), key = lambda i: i[len(i) - 1]), key = lambda i: i[:-1])
        anneal(configs[0], configs[1], m=m, K=k, T=k)


def gen_configs(m):
    return (  gen_umat(m), gen_combos(m) )

def anneal(umat, keys, m, its=1000, T=4, r=.95, K=4):
    shift_len = find_shift_len(m)
    coloring = gen_random_coloring(shift_len)
    apply_str_coloring(umat, keys, coloring)
    training_umat = deepcopy(umat)

    for i in range(its):
        current_fitness = fitness(umat, coloring, K)

        if current_fitness <= K:
            click.secho(f"YOU FOUND IT : ", fg="green")
            click.secho(f"{ umat }")
            return

        next_coloring = mut(coloring, shift_len, dist = round(T))
        apply_coloring(training_umat, keys, Number(), shift_len)
        next_fitness = fitness(training_umat, next_coloring, K)

        delta = next_fitness - current_fitness
        
        if delta < 0:
            pass
        else:
            power = delta / T
            prob = pow(e, power)
            umat = umat if random() > prob else training_umat
            
        T *= r



def brute_force(umat, combos, m, k):
    combos = gen_combos(m)
    print(combos)
    umat = gen_umat(m) 
    sorted_key_list = sorted(umat.keys(), key=len) # doesn't matter what order we assign the keys in as
                                                   # long as it's the same order every time
    shift_len = (m - 1) * m / 2 + 1 # number of cells in the umat
    print(shift_len)

    counter = Number()

    for i in range(1 << int(shift_len)):
        apply_coloring(umat, sorted_key_list, counter, shift_len) 
        if check_combos(combos, umat, k):
            print(f"There are no unicolored sets of size {k} on :  \n {umat}")

def find_shift_len(m):
    return (m - 1) * m / 2 + 1

def mut(coloring, shift_len, dist: int =1): # select dist random points and invert them
    coloring = list(coloring)
    for i in range(dist + 1):
        select = 1 << randrange(1, shift_len)
        coloring[select] = str(~ int(coloring[select]))
    return str(coloring)
    

def gen_random_coloring(shift_len):
    coloring = ""
    for i in range(int(shift_len)):
        coloring += choice(['0', '1'])
    return coloring


def apply_str_coloring(umat, keys, coloring):
    for key, color in zip(keys, coloring):
        umat[key] = int(color)

def apply_coloring(umat, keys, number, shift_len):
    coloring = number.val
    #change color formatting for higher values of m
    c = list("{:b}".format(coloring).zfill(int(shift_len)))
    for key, color in zip(keys, c):
        umat[key] = int(color)
    number.val += 1

'''
@param combos : all possible combos over this map
@param umat : upper-m matrix
@param k : size of set that the function seeks to exclude
@returns : whether it succeeds in excluding or not 
'''

def check_combos(combos, umat, k) -> bool: 
    uni_sums = {0, comb(k, 2)}
    start, end = find_start_end(combos, k)
    for combo in combos[start : end + 1]:
        sum = 0
        for i, first in enumerate(combo[:(len(combo) - 1)]): #(1,2,3)
            for second in combo[i + 1:]:
                try:
                    sum += umat[first,second]
                except KeyError as ke:
                    print(umat)
                    print(ke)
                    raise Exception
        if sum in uni_sums:
            print(f"{combo} is a unicolored set on \n{umat}.")
            return False
    return True
    
def find_start_end(combos, k) -> tuple:     
    start: int
    end: int
    start_found: bool = False
    for i in range(len(combos)):
        if not start_found and len(combos[i]) == k:
            start = i
            start_found = True
        if len(combos[i]) == k + 1:
            end = i # the range will take care of the extra element in the contexts in which it's called
            break
    return start, end

def fitness(umat, combos, k) -> int: # similar to check combo but returns the 
                                     # number of bad sets it finds
    score = 0
    uni_sums = {0, comb(k, 2)}
    start, end = find_start_end(combos, k)
    for combo in combos[start : end + 1]:
        sum = 0
        for i, first in enumerate(combo[:(len(combo) - 1)]): #(1,2,3)
            for second in combo[i + 1:]:
                try:
                    sum += umat[first,second]
                except KeyError as ke:
                    print(umat)
                    print(ke)
                    raise Exception
        if sum in uni_sums:
            score += 1 
    return score

if __name__ == "__main__":
    main()