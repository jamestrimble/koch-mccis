import sys


class Graph(object):
    def __init__(self, n, labels):
        self.n = n
        self.adjmat = [[0] * n for _ in range(n)]
        self.labels = labels

    def add_edge(self, v, w):
        self.adjmat[v][w] = 1
        self.adjmat[w][v] = 1


def enumerate_c_cliques(C, P, D, S, T, g_adj, g_c_edges, G_vertices):
    if not P and not S:
        print([G_vertices[v] for v in C])
        return
    for u in list(P):
        P.remove(u)
        P_ = set(P)
        D_ = set(D)
        S_ = set(S)
        N = g_adj[u]
        for v in list(D_):
            if (v, u) in g_c_edges:
                if v in T:
                    S_.add(v)
                else:
                    P_.add(v)
                D_.remove(v)
        C.add(u)
        enumerate_c_cliques(C, P_ & N, D_ & N, S_ & N, T, g_adj, g_c_edges, G_vertices)
        C.remove(u)
        S.add(u)


def find_maximal_common_subgraphs(F, H, connected=False):
    F_labels = set(F.labels)
    H_labels = set(H.labels)
    G_vertices = []
    for label in F_labels & H_labels:
        F_vertices = [v for v in range(F.n) if F.labels[v] == label]
        H_vertices = [v for v in range(H.n) if H.labels[v] == label]
        for v in F_vertices:
            for w in H_vertices:
                G_vertices.append((v, w))
    # g is isomorphic to G, but has integers instead of vertex pairs as vertices
    g_adj = {v: set() for v in range(len(G_vertices))}
    g_c_edges = set()
    for i, (u1, u2) in enumerate(G_vertices):
        for j, (w1, w2) in enumerate(G_vertices):
            if j <= i:
                continue
            if u1 == w1:
                continue
            if u2 == w2:
                continue
            if F.adjmat[u1][w1] != H.adjmat[u2][w2]:
                continue
            g_adj[i].add(j)
            g_adj[j].add(i)
            if F.adjmat[u1][w1]:
                g_c_edges.add((i, j))
                g_c_edges.add((j, i))

    T = set()
    for u in range(len(G_vertices)):
        P = set()
        D = set()
        S = set()
        N = g_adj[u]
        for v in N:
            if (u, v) in g_c_edges:
                if v in T:
                    S.add(v)
                else:
                    P.add(v)
            else:
                D.add(v)
        enumerate_c_cliques(set([u]), P, D, S, T, g_adj, g_c_edges, G_vertices)
        T.add(u)


def read_instance(filename):
    with open(filename, "r") as f:
        lines = [line.strip().split() for line in f.readlines()]
    n = int(lines[0][0])
    edge_count = int(lines[0][1])
    G = Graph(n, lines[1])
    for e in lines[2:]:
        G.add_edge(int(e[0]), int(e[1]))
    return G


if __name__ == "__main__":
    G = read_instance(sys.argv[1])
    H = read_instance(sys.argv[2])
    find_maximal_common_subgraphs(G, H, connected=True)
