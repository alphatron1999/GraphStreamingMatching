import os
import sys
import math
from collections import namedtuple
import networkx as nx
import random
from tqdm import tqdm

in_file_name = sys.argv[1]
# if not os.path.exists(in_file_name):
os.system("python preprocess.py "+in_file_name[:-3]+"mtx")
# print("Data Shuffled")
inp = open(in_file_name,'r')
read_inp = lambda: [int(i) for i in inp.readline().strip().split()]
a_end, b_end = read_inp()
n,num_edges = read_inp()
data_begin = inp.tell()
refresh_stream = lambda: inp.seek(data_begin)
matching_size = lambda x: len(x.E)

all_node_set = set([i for i in range(n)])

Matching  = namedtuple('Matching', ['A','B','E'])

def init_matching():
    return Matching([-1]*n,[-1]*n,[])

def greedy_add(M,e,A = all_node_set,B = all_node_set):
    u,v = e
    if (u in A) and (v in B) and (M.A[u] == -1) and (M.B[v]==-1):
        M.A[u] = v
        M.B[v] = u
        M.E.append(e)

def greedy_matching():
    M = init_matching()
    for i in range(num_edges):
        greedy_add(M,read_inp())
    refresh_stream()
    return M

def augment(M_0, M_1, M_2):
    #   Bu --(M_1)-- A --(M_0)-- B --(M_2)-- Au

    M_aug = init_matching()
    for a_u,b in M_2.E:
        a = M_0.B[b]
        b_u = M_1.A[a]
        M_aug.E.append((a_u, b))
        M_aug.E.append((a, b_u))
        M_aug.A[a] = b_u
        M_aug.A[a_u] = b
        M_aug.B[b_u] = a
        M_aug.B[b] = a_u

    for a,b in M_0.E:
        if M_aug.A[a] == -1 and M_aug.B[b] == -1:
            M_aug.E.append((a,b))
            M_aug.A[a] = b
            M_aug.B[b] = a

    for a,b in M_1.E:
        if M_aug.A[a] == -1 and M_aug.B[b] == -1:
            M_aug.E.append((a,b))
            M_aug.A[a] = b
            M_aug.B[b] = a

    return M_aug

def three_pass_matching():
    M_g = greedy_matching()
    A_l = set(M_g.B)
    B_l = all_node_set - set(M_g.A)
    M_l = init_matching()
    for i in range(num_edges):
        greedy_add(M_l,read_inp(),A_l,B_l)
    refresh_stream()
    A_r  = all_node_set - set(M_g.B)
    B_r = set([b for b in range(n) if (M_g.B[b]!=-1 and M_l.A[M_g.B[b]]!=-1)])
    M_r = init_matching()
    for i in range(num_edges):
        greedy_add(M_r,read_inp(),A_r,B_r)
    refresh_stream()
    return augment(M_g, M_l, M_r)

def one_pass_matching():
    alpha, beta = 0.4312, 0.7595
    alpha_m, beta_m = math.floor(alpha*num_edges), math.floor(beta*num_edges)

    M_g = init_matching()
    M_0 = init_matching()
    for i in range(alpha_m):
        edge = read_inp()
        greedy_add(M_g, edge)
        greedy_add(M_0, edge)

    A_1 = set(M_0.B)
    B_1 = all_node_set - set(M_0.A)
    M_1 = init_matching()
    for i in range(alpha_m, beta_m):
        edge = read_inp()
        greedy_add(M_g, edge)
        greedy_add(M_1, edge, A_1, B_1)

    A_2 = all_node_set - set(M_0.B)
    B_2 = set([b for b in range(n) if (M_0.B[b]!=-1 and M_1.A[M_0.B[b]]!=-1)])
    M_2 = init_matching()
    for i in range(beta_m, num_edges):
        edge = read_inp()
        greedy_add(M_g, edge)
        greedy_add(M_2, edge, A_2, B_2)
    refresh_stream()
    return max(M_g,augment(M_0, M_1, M_2), key = matching_size)

def two_pass_matching_r():
    p = math.sqrt(2) - 1
    num_elems = min(math.ceil(p * (b_end - a_end)),(b_end - a_end))
    B_prime = set(random.sample(range(a_end, b_end), num_elems))
    M_0 = init_matching()
    M_prime = init_matching()
    for i in range(num_edges):
        edge = read_inp()
        greedy_add(M_0, edge)
        greedy_add(M_prime, edge,B = B_prime)
    refresh_stream()
    M_1 = init_matching()
    for e in M_prime.E:
        u,v = e
        if M_0.A[u]!=-1 and M_0.B[v]==-1:
            M_1.E.append(e)
            M_1.A[u] = v
            M_1.B[v] = u
    M_2 = init_matching()
    A_2 = all_node_set - set(M_0.B)
    B_2 = set([b for b in range(n) if (M_0.B[b]!=-1 and M_1.A[M_0.B[b]]!=-1)])
    for i in range(num_edges):
        edge = read_inp()
        greedy_add(M_2, edge, A_2, B_2)
    refresh_stream()
    return augment(M_0, M_1, M_2)

def two_pass_matching_d():
    M_0 = init_matching()
    S = init_matching()
    for i in range(num_edges):
        edge = read_inp()
        greedy_add(M_0, edge)
        u,v = edge
        if S.A[u] < 3 and S.B[v] == -1:
            S.B[v] = 1
            S.A[u] = 1 if S.A[u] == -1 else (S.A[u] + 1)
            S.E.append(edge)
    refresh_stream()
    S_1 = init_matching()
    for e in S.E:
        u,v = e
        if M_0.A[u]!=-1 and M_0.B[v]==-1:
            S_1.E.append(e)
            S_1.A[u] = v
            S_1.B[v] = u
    M_2 = init_matching()
    A_2 = all_node_set - set(M_0.B)
    B_2 = set([b for b in range(n) if (M_0.B[b]!=-1 and S_1.A[M_0.B[b]]!=-1)])
    for i in range(num_edges):
        edge = read_inp()
        greedy_add(M_2, edge, A_2, B_2)
    refresh_stream()
    return augment(M_0, S_1, M_2)

if not os.path.exists(in_file_name[:-4]+"_opt.txt"):
    print("Calculating OPT")
    B = nx.Graph()
    for i in range(num_edges):
        u,v = read_inp()
        if u not in B.nodes():
            B.add_node(u, bipartite = 0)
        if v not in B.nodes():
            B.add_node(v, bipartite = 1)
        B.add_edge(u,v)
    refresh_stream()
    u = [x for x in B.nodes if B.nodes[x]['bipartite'] == 0]
    match = nx.bipartite.maximum_matching(B, top_nodes = u)
    opt_file = open(in_file_name[:-4]+"_opt.txt",'w')
    opt_file.write(str(len(match)//2)+"\n")


num_shuffles = 10
greedy_file = open(in_file_name[:-4]+"_greedy.txt",'w')
three_pass_file = open(in_file_name[:-4]+"_three_pass.txt",'w')
one_pass_file = open(in_file_name[:-4]+"_one_pass.txt",'w')
two_pass_r_file = open(in_file_name[:-4]+"_two_pass_r.txt",'w')
two_pass_d_file = open(in_file_name[:-4]+"_two_pass_d.txt",'w')

for i in tqdm(range(num_shuffles)):
    match = greedy_matching()
    greedy_file.write(str(matching_size(match))+"\n")

    match = three_pass_matching()
    three_pass_file.write(str(matching_size(match))+"\n")

    match = one_pass_matching()
    one_pass_file.write(str(matching_size(match))+"\n")

    match = two_pass_matching_r()
    two_pass_r_file.write(str(matching_size(match))+"\n")

    match = two_pass_matching_d()
    two_pass_d_file.write(str(matching_size(match))+"\n")
    if i!=num_shuffles-1:
        inp.close()
        os.system("python preprocess.py "+in_file_name[:-3]+"mtx")
        inp = open(in_file_name,'r')
        read_inp()
        read_inp()
        data_begin = inp.tell()