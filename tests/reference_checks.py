"""Independent brute-force and structural checks for the 48 algorithms."""
from pathlib import Path
from collections import Counter
from itertools import combinations, permutations, product
from functools import lru_cache
import ast
import hashlib
import json
import math
import random
import runpy
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT
CATALOG = json.loads((BASE / 'catalog.json').read_text(encoding='utf-8'))['algorithms']
RNG = random.Random(20261012)
CHECKS = Counter()
MODULES = {}


def eq(name, actual, expected):
    CHECKS[name] += 1
    assert actual == expected, (name, actual, expected)


def check(name, condition):
    eq(name, bool(condition), True)


def mod(name):
    return MODULES[name]


def graph_of(n, edges, directed=False):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph


def reachability(graph):
    # Boolean transitive closure: DFS/BFS/SCCの実装と独立な参照。
    n = len(graph)
    reach = [[i == j or j in graph[i] for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] |= reach[i][k] and reach[k][j]
    return reach


def shortest(n, edges, source):
    # Bellman-Fordの層別更新。n-1辺までの全経路を覆う。
    dist = [math.inf] * n
    dist[source] = 0
    for _ in range(n - 1):
        nxt = dist.copy()
        for u, v, w in edges:
            nxt[v] = min(nxt[v], dist[u] + w)
        dist = nxt
    return dist


def tree(n):
    return graph_of(n, [(v, RNG.randrange(v)) for v in range(1, n)])


def path_vertices(graph, source, target):
    parent = {source: None}
    queue = [source]
    for v in queue:
        for u in graph[v]:
            if u not in parent:
                parent[u] = v
                queue.append(u)
    result = []
    v = target
    while v is not None:
        result.append(v)
        v = parent[v]
    return result


def test_c():
    for _ in range(80):
        n = RNG.randrange(11)
        a = [RNG.randrange(-5, 6) for _ in range(n)]
        m = mod('prefix_sum')
        p = m['prefix_sum'](a)
        for l in range(n+1):
            for r in range(l, n+1):
                eq('prefix_sum', m['range_sum'](p, l, r), sum(a[l:r]))
        h, w = RNG.randrange(5), RNG.randrange(5)
        grid = [[RNG.randrange(-5, 6) for _ in range(w)] for _ in range(h)]
        p2 = m['prefix_sum_2d'](grid)
        if h:
            for __ in range(10):
                y1, y2 = sorted([RNG.randrange(h+1), RNG.randrange(h+1)])
                x1, x2 = sorted([RNG.randrange(w+1), RNG.randrange(w+1)])
                eq('prefix_sum', m['rect_sum'](p2, y1, x1, y2, x2), sum(sum(row[x1:x2]) for row in grid[y1:y2]))
        eq('frequency', mod('frequency')['equal_pairs'](a), sum(a[i] == a[j] for i in range(n) for j in range(i+1,n)))
        bound = RNG.randrange(50)
        eq('binary_search', mod('binary_search')['boundary'](-1, 51, lambda x: x <= bound), bound)
        eq('binary_search', mod('binary_search')['boundary'](51, -1, lambda x: x >= bound), bound)
        updates, ref = [], [0]*n
        for __ in range(12):
            l, r = sorted([RNG.randrange(n+1), RNG.randrange(n+1)])
            x = RNG.randrange(-5, 6)
            updates.append((l,r,x))
            for i in range(l,r):
                ref[i] += x
        eq('imos', mod('imos')['imos'](n, updates), ref)
        compressed, values = mod('coordinate_compression')['compress'](a)
        eq('coordinate_compression', [values[x] for x in compressed], a)
        eq('coordinate_compression', values, sorted(set(a)))
        for i in range(n):
            for j in range(n):
                eq('coordinate_compression', compressed[i] < compressed[j], a[i] < a[j])
        target = RNG.randrange(-8, 9)
        expected = sum(sum(a[i] for i in range(n) if bits[i]) == target for bits in product((0,1), repeat=n))
        eq('bit_enumeration', mod('bit_enumeration')['count_subset_sum'](a,target), expected)
        intervals = [tuple(sorted((RNG.randrange(-4,7), RNG.randrange(-4,7)))) for __ in range(9)]
        result = mod('interval_merge')['merge_intervals'](intervals)
        eq('interval_merge', {x for l,r in result for x in range(l,r)}, {x for l,r in intervals for x in range(l,r)})
        check('interval_merge', all(l<r for l,r in result) and all(result[i][1] < result[i+1][0] for i in range(len(result)-1)))
    for n in range(1, 151):
        m = mod('number_theory')
        eq('number_theory', m['divisors'](n), [d for d in range(1,n+1) if n%d == 0])
        eq('number_theory', m['sieve'](n), [x for x in range(2,n+1) if all(x%d for d in range(2,x))])
    eq('number_theory', mod('number_theory')['sieve'](0), [])


def test_d():
    for _ in range(90):
        n = RNG.randrange(10)
        a = [RNG.randrange(5) for __ in range(n)]
        k = RNG.randrange(-1, 12)
        eq('two_pointers', mod('two_pointers')['count_sum_at_most'](a,k), sum(sum(a[l:r]) <= k for l in range(n) for r in range(l+1,n+1)))
        a = [RNG.randrange(-3,4) for __ in range(n)]
        eq('prefix_hash', mod('prefix_hash')['count_sum_equal'](a,k), sum(sum(a[l:r]) == k for l in range(n) for r in range(l+1,n+1)))
        top = mod('heap')['TopK'](k := RNG.randrange(n+3))
        for i,x in enumerate(a):
            top.add(x)
            eq('heap', top.total, sum(sorted(a[:i+1], reverse=True)[:k]))
        items = [(RNG.randrange(6),RNG.randrange(-3,10)) for __ in range(n)]
        capacity = RNG.randrange(12)
        expected = max(sum(v for (w,v),b in zip(items,bits) if b) for bits in product((0,1), repeat=n) if sum(w for (w,v),b in zip(items,bits) if b) <= capacity)
        eq('knapsack', mod('knapsack')['knapsack'](items,capacity), expected)
        intervals = [(x := RNG.randrange(-5,5), x+RNG.randrange(1,6)) for __ in range(n)]
        best = 0
        for bits in product((0,1), repeat=n):
            chosen = sorted(p for p,b in zip(intervals,bits) if b)
            if all(chosen[i][1] <= chosen[i+1][0] for i in range(len(chosen)-1)):
                best = max(best,len(chosen))
        eq('interval_greedy', len(mod('interval_greedy')['schedule'](intervals)), best)
        n = RNG.randrange(1,10)
        edges = [(i,j) for i in range(n) for j in range(i,n) if RNG.random() < .2]
        graph = graph_of(n,edges)
        reach = reachability(graph)
        labels = mod('dfs')['components'](graph)
        uf = mod('union_find')['DSU'](n)
        incremental = [[] for __ in range(n)]
        for u,v in edges:
            before = reachability(incremental)
            eq('union_find', uf.merge(u,v), not before[u][v])
            incremental[u].append(v)
            incremental[v].append(u)
        for i in range(n):
            eq('union_find', uf.size(i), sum(reach[i]))
            for j in range(n):
                eq('dfs', labels[i] == labels[j], reach[i][j])
                eq('union_find', uf.same(i,j), reach[i][j])
        sources = [RNG.randrange(n) for __ in range(RNG.randrange(n+1))]
        ref = [math.inf] * n
        directed_edges = [(v,u,1) for v,row in enumerate(graph) for u in row]
        for s in sources:
            d = shortest(n,directed_edges,s)
            ref = [min(a,b) for a,b in zip(ref,d)]
        eq('bfs', mod('bfs')['bfs'](graph,sources), [-1 if x == math.inf else x for x in ref])
        g = tree(n)
        parent, order = mod('dfs')['tree_order'](g)
        eq('dfs', sorted(order), list(range(n)))
        check('dfs', all(parent[v] in g[v] and order.index(parent[v]) < order.index(v) for v in range(1,n)))
        h,w = RNG.randrange(1,5),RNG.randrange(1,5)
        grid = [''.join('#' if RNG.random()<.3 else '.' for __ in range(w)) for ___ in range(h)]
        edges = []
        for y in range(h):
            for x in range(w):
                if grid[y][x] == '#':
                    continue
                for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if 0<=yy<h and 0<=xx<w and grid[yy][xx]!='#':
                        edges.append((y*w+x,yy*w+xx,1))
        expected = shortest(h*w,edges,0) if grid[0][0]!='#' else [math.inf]*(h*w)
        expected = [-1 if d == math.inf else d for d in expected]
        eq('bfs', mod('bfs')['grid_bfs'](grid,(0,0)), [expected[y*w:(y+1)*w] for y in range(h)])


def test_e():
    for _ in range(70):
        n = RNG.randrange(1,9)
        edges = [(u,v,RNG.randrange(8)) for u in range(n) for v in range(n) if RNG.random()<.2]
        graph = [[] for __ in range(n)]
        for u,v,w in edges:
            graph[u].append((v,w))
        source = RNG.randrange(n)
        eq('dijkstra', mod('dijkstra')['dijkstra'](graph,source), shortest(n,edges,source))
        dag = [[j for j in range(i+1,n) if RNG.random()<.3] for i in range(n)]
        m = mod('topological_sort')
        order = m['topological_sort'](dag)
        check('topological_sort', len(order)==n and all(order.index(v)<order.index(u) for v,row in enumerate(dag) for u in row))
        def depth(v):
            return max((1+depth(u) for u in dag[v]), default=0)
        eq('topological_sort', m['longest_path'](dag), max(map(depth,range(n))))
        a = [RNG.randrange(-4,5) for __ in range(n)]
        subs = [[x for x,b in zip(a,bits) if b] for bits in product((0,1), repeat=n)]
        eq('lis', mod('lis')['lis_length'](a), max(len(s) for s in subs if all(s[i]<s[i+1] for i in range(len(s)-1))))
        target = RNG.randrange(-10,11)
        eq('meet_in_middle', mod('meet_in_middle')['count_subset_sum'](a,target), sum(sum(s)==target for s in subs))
        eq('fenwick_tree', mod('fenwick_tree')['inversions'](a), sum(a[i]>a[j] for i in range(n) for j in range(i+1,n)))
        bit = mod('fenwick_tree')['Fenwick'](n)
        ref = [0]*n
        seg = mod('segment_tree')['SegTree'](ref,lambda a,b:a+b,0)
        segmin = mod('segment_tree')['SegTree'](ref)
        for __ in range(30):
            i,x = RNG.randrange(n),RNG.randrange(-10,11)
            bit.add(i,x)
            ref[i] += x
            seg.set(i,ref[i])
            segmin.set(i,ref[i])
            l,r = sorted((RNG.randrange(n+1),RNG.randrange(n+1)))
            eq('fenwick_tree',bit.sum(l,r),sum(ref[l:r]))
            eq('segment_tree',seg.prod(l,r),sum(ref[l:r]))
            eq('segment_tree',segmin.prod(l,r),min(ref[l:r],default=math.inf))
    # 非可換演算で左右の結合順を検証。
    s = mod('segment_tree')['SegTree'](list('abcdef'),lambda a,b:a+b,'')
    for l in range(7):
        for r in range(l,7):
            eq('segment_tree',s.prod(l,r),'abcdef'[l:r])
    eq('segment_tree',mod('segment_tree')['SegTree']([]).prod(0,0),math.inf)
    eq('fenwick_tree',mod('fenwick_tree')['Fenwick'](0).sum(0,0),0)
    eq('topological_sort',mod('topological_sort')['topological_sort']([[1],[0]]),None)
    eq('topological_sort',mod('topological_sort')['longest_path']([]),0)
    eq('lis',mod('lis')['lis_length']([]),0)
    eq('meet_in_middle',mod('meet_in_middle')['count_subset_sum']([],0),1)
    for p in (2,7,101,998244353):
        nmax = min(p-1,35)
        c = mod('combinations')['Combinations'](nmax,p)
        for n in range(nmax+1):
            for r in range(-1,n+2):
                eq('combinations',c.choose(n,r),math.comb(n,r)%p if 0<=r<=n else 0)
    for _ in range(40):
        n = RNG.randrange(0,7)
        cost = [[0 if i==j else (RNG.randrange(-2,9) if RNG.random()<.8 else math.inf) for j in range(n)] for i in range(n)]
        expected = 0 if n<=1 else min(sum(cost[u][v] for u,v in zip((0,)+p,p+(0,))) for p in permutations(range(1,n)))
        eq('bit_dp',mod('bit_dp')['tsp'](cost),expected)


def test_f():
    for _ in range(70):
        n = RNG.randrange(1,9)
        edges = [(u,v,RNG.randrange(2)) for u in range(n) for v in range(n) if RNG.random()<.22]
        graph = [[] for __ in range(n)]
        for u,v,w in edges:
            graph[u].append((v,w))
        eq('zero_one_bfs',mod('zero_one_bfs')['zero_one_bfs'](graph,0),shortest(n,edges,0))
        edges = [(u,v,RNG.randrange(-5,8)) for u in range(n) for v in range(u+1,n) if RNG.random()<.4]
        eq('floyd_warshall',mod('floyd_warshall')['floyd_warshall'](n,edges),[shortest(n,edges,s) for s in range(n)])
        g = tree(n)
        root = RNG.randrange(n)
        lca = mod('doubling_lca')['LCA'](g,root)
        for u in range(n):
            ancestors = path_vertices(g,root,u)
            for k in range(n+2):
                eq('doubling_lca',lca.ancestor(u,k),ancestors[k] if k<len(ancestors) else -1)
            for v in range(n):
                other = set(path_vertices(g,root,v))
                expected = next(x for x in ancestors if x in other)
                eq('doubling_lca',lca.lca(u,v),expected)
                eq('doubling_lca',lca.distance(u,v),len(path_vertices(g,u,v))-1)
        edges = [(v,u) for v,row in enumerate(g) for u in row if v<u]
        expected = sum(not any(bits[u] and bits[v] for u,v in edges) for bits in product((0,1),repeat=n))
        eq('tree_dp',mod('tree_dp')['independent_sets'](g,13),expected%13)
        bound,d = RNG.randrange(501),RNG.randrange(1,13)
        eq('digit_dp',mod('digit_dp')['count_digit_sum_multiple'](str(bound),d,97),sum(sum(map(int,str(x)))%d==0 for x in range(1,bound+1))%97)
        a = tuple(RNG.randrange(1,10) for __ in range(RNG.randrange(7)))
        @lru_cache(None)
        def brute_merge(seq):
            if len(seq)<=1:
                return 0
            return min(seq[i]+seq[i+1]+brute_merge(seq[:i]+(seq[i]+seq[i+1],)+seq[i+2:]) for i in range(len(seq)-1))
        eq('interval_dp',mod('interval_dp')['merge_cost'](a),brute_merge(a))
        s = ''.join(RNG.choice('abc') for __ in range(RNG.randrange(25)))
        expected = []
        for i in range(len(s)):
            k = 0
            while i+k<len(s) and s[k]==s[i+k]:
                k+=1
            expected.append(k)
        eq('z_algorithm',mod('z_algorithm')['z_algorithm'](s),expected)
    eq('tree_dp',mod('tree_dp')['independent_sets']([]),1)
    eq('floyd_warshall',mod('floyd_warshall')['floyd_warshall'](2,[(0,1,3),(0,1,1)],False),[[0,1],[1,0]])
    check('floyd_warshall',mod('floyd_warshall')['floyd_warshall'](1,[(0,0,-1)])[0][0]<0)
    for _ in range(60):
        n = RNG.randrange(1,6)
        edges = [(v,RNG.randrange(v),RNG.randrange(-5,9)) for v in range(1,n)]
        for __ in range(RNG.randrange(4)):
            edges.append((RNG.randrange(n),RNG.randrange(n),RNG.randrange(-5,9)))
        best = math.inf
        for chosen in combinations(edges,n-1):
            reach = reachability(graph_of(n,[(u,v) for u,v,w in chosen]))
            if all(reach[0]):
                best = min(best,sum(w for u,v,w in chosen))
        cost,chosen = mod('kruskal')['kruskal'](n,edges)
        eq('kruskal',cost,best)
        eq('kruskal',len(chosen),n-1)
    eq('kruskal',mod('kruskal')['kruskal'](3,[(0,1,2)])[0],2)


def test_g():
    for _ in range(75):
        n = RNG.randrange(0,9)
        graph = [[u for u in range(n) if RNG.random()<.25] for v in range(n)]
        reach = reachability(graph)
        ids,groups = mod('scc')['scc'](graph)
        eq('scc',sorted(v for group in groups for v in group),list(range(n)))
        for v in range(n):
            for u in range(n):
                eq('scc',ids[v]==ids[u],reach[v][u] and reach[u][v])
            check('scc',all(ids[v]<=ids[u] for u in graph[v]))
        n = RNG.randrange(1,7)
        clauses = [(RNG.randrange(n),bool(RNG.randrange(2)),RNG.randrange(n),bool(RNG.randrange(2))) for __ in range(RNG.randrange(15))]
        def feasible(bits):
            return all(bits[i]==f or bits[j]==g for i,f,j,g in clauses)
        possible = any(feasible(bits) for bits in product((False,True),repeat=n))
        answer = mod('two_sat')['two_sat'](n,clauses)
        eq('two_sat',answer is not None,possible)
        if answer is not None:
            check('two_sat',feasible(answer))
        n = RNG.randrange(12)
        a = [RNG.randrange(-9,10) for __ in range(n)]
        lazy = mod('lazy_segment_tree')['RangeAddSum'](a)
        for __ in range(35):
            l,r = sorted((RNG.randrange(n+1),RNG.randrange(n+1)))
            if RNG.random()<.6:
                x = RNG.randrange(-7,8)
                lazy.add(l,r,x)
                for i in range(l,r):
                    a[i]+=x
            else:
                eq('lazy_segment_tree',lazy.sum(l,r),sum(a[l:r]))
        queries = [tuple(sorted((RNG.randrange(n+1),RNG.randrange(n+1)))) for __ in range(20)]
        eq('mo',mod('mo')['distinct_queries'](a,queries),[len(set(a[l:r])) for l,r in queries])
        g = tree(n) if n else []
        expected = [sum(len(path_vertices(g,v,u))-1 for u in range(n)) for v in range(n)]
        eq('rerooting',mod('rerooting')['all_distance_sums'](g),expected)
        k,t,p = RNG.randrange(1,5),RNG.randrange(9),RNG.choice([1,7,101])
        a = [[RNG.randrange(-3,4) for __ in range(k)] for ___ in range(k)]
        result = [[int(i==j)%p for j in range(k)] for i in range(k)]
        for __ in range(t):
            result = [[sum(result[i][z]*a[z][j] for z in range(k))%p for j in range(k)] for i in range(k)]
        eq('matrix_power',mod('matrix_power')['matpow'](a,t,p),result)
        left,right = RNG.randrange(7),RNG.randrange(7)
        graph = [[u for u in range(right) if RNG.random()<.4] for __ in range(left)]
        def brute(v, used):
            if v==left:
                return 0
            return max([brute(v+1,used)]+[1+brute(v+1,used | {u}) for u in graph[v] if u not in used])
        count,match = mod('bipartite_matching')['matching'](graph,right)
        eq('bipartite_matching',count,brute(0,set()))
        eq('bipartite_matching',len(set(x for x in match if x>=0)),count)
        check('bipartite_matching',all(x<0 or x in graph[v] for v,x in enumerate(match)))
        n = RNG.randrange(2,8)
        edges = [(RNG.randrange(n),RNG.randrange(n),RNG.randrange(5)) for __ in range(RNG.randrange(18))]
        cuts = [{0} | {i+1 for i,b in enumerate(bits) if b} for bits in product((0,1),repeat=n-2)]
        expected = min(sum(c for u,v,c in edges if u in cut and v not in cut) for cut in cuts)
        net = mod('max_flow')['Dinic'](n)
        for edge in edges:
            net.add_edge(*edge)
        eq('max_flow',net.flow(0,n-1),expected)
        cut = net.min_cut(0)
        eq('max_flow',sum(c for u,v,c in edges if cut[u] and not cut[v]),expected)
        eq('max_flow',net.flow(0,n-1),0)
    eq('two_sat',mod('two_sat')['two_sat'](0,[]),[])
    eq('two_sat',mod('two_sat')['two_sat'](1,[(0,True,0,True),(0,False,0,False)]),None)


def test_advanced():
    for _ in range(80):
        a = [RNG.randrange(-20,21) for __ in range(RNG.randrange(25))]
        b = [RNG.randrange(-20,21) for __ in range(RNG.randrange(25))]
        expected = [0]*(len(a)+len(b)-1) if a and b else []
        for i,x in enumerate(a):
            for j,y in enumerate(b):
                expected[i+j] += x*y
        eq('ntt',mod('ntt')['convolution'](a,b),[x%998244353 for x in expected])
        n = RNG.randrange(1,12)
        g = tree(n)
        values = [RNG.randrange(-10,11) for __ in range(n)]
        hld = mod('hld')['HLDPathSum'](g,values)
        for __ in range(25):
            v,x = RNG.randrange(n),RNG.randrange(-10,11)
            hld.add(v,x)
            values[v]+=x
            u,v = RNG.randrange(n),RNG.randrange(n)
            eq('hld',hld.path_sum(u,v),sum(values[x] for x in path_vertices(g,u,v)))
        xs = sorted(set(RNG.randrange(-15,16) for __ in range(n)))
        lc = mod('li_chao_tree')['LiChao'](xs)
        lines = []
        eq('li_chao_tree',lc.query(xs[0]),math.inf)
        for __ in range(20):
            line = (RNG.randrange(-10,11),RNG.randrange(-20,21))
            lines.append(line)
            lc.add_line(*line)
            for x in xs:
                eq('li_chao_tree',lc.query(x),min(a*x+b for a,b in lines))
        uf = mod('rollback_dsu')['RollbackDSU'](n)
        edges,snapshots = [],[(uf.snapshot(),[])]
        for __ in range(35):
            if RNG.random()<.2:
                token,old_edges = snapshots.pop()
                uf.rollback(token)
                edges=old_edges.copy()
                if not snapshots:
                    snapshots.append((uf.snapshot(),edges.copy()))
            elif RNG.random()<.25:
                snapshots.append((uf.snapshot(),edges.copy()))
            else:
                u,v = RNG.randrange(n),RNG.randrange(n)
                uf.merge(u,v)
                edges.append((u,v))
            reach = reachability(graph_of(n,edges))
            u,v = RNG.randrange(n),RNG.randrange(n)
            eq('rollback_dsu',uf.same(u,v),reach[u][v])
        size=1<<RNG.randrange(7)
        a=[RNG.randrange(-5,6) for __ in range(size)]
        z=mod('sos_dp')['subset_zeta'](a)
        eq('sos_dp',z,[sum(a[s] for s in range(size) if s & mask == s) for mask in range(size)])
        eq('sos_dp',mod('sos_dp')['subset_mobius'](z),a)
        s=''.join(RNG.choice('abあ') for __ in range(RNG.randrange(25)))
        sa=mod('suffix_array')['suffix_array'](s)
        eq('suffix_array',sa,sorted(range(len(s)),key=lambda i:s[i:]))
        expected=[]
        for i,j in zip(sa,sa[1:]):
            k=0
            while i+k<len(s) and j+k<len(s) and s[i+k]==s[j+k]:
                k+=1
            expected.append(k)
        eq('suffix_array',mod('suffix_array')['lcp_array'](s,sa),expected)
        points = list(set((RNG.randrange(-4,5),RNG.randrange(-4,5)) for __ in range(RNG.randrange(12))))
        # Jarvis march: 整列して積む方式とは独立に、全候補を走査して次の極点を選ぶ。
        if len(points)<=1:
            expected=set(points)
        else:
            cur=min(points)
            expected=set()
            while cur not in expected:
                expected.add(cur)
                nxt=next(p for p in points if p!=cur)
                for p in points:
                    cross=(nxt[0]-cur[0])*(p[1]-cur[1])-(nxt[1]-cur[1])*(p[0]-cur[0])
                    d=lambda q:(q[0]-cur[0])**2+(q[1]-cur[1])**2
                    if cross<0 or (cross==0 and d(p)>d(nxt)):
                        nxt=p
                cur=nxt
        hull=mod('convex_hull')['convex_hull'](points)
        eq('convex_hull',set(hull),expected)
        eq('convex_hull',len(hull),len(set(hull)))
        if len(hull)>=3:
            check('convex_hull',all(mod('convex_hull')['cross'](hull[i-2],hull[i-1],hull[i])>0 for i in range(len(hull))))
    for _ in range(85):
        n=RNG.randrange(2,5)
        edges=[(RNG.randrange(n),RNG.randrange(n),RNG.randrange(3),RNG.randrange(5)) for __ in range(RNG.randrange(7))]
        limit=RNG.randrange(5)
        best_flow,best_cost=0,0
        for amounts in product(*(range(c+1) for u,v,c,w in edges)):
            balance=[0]*n
            cost=0
            for amount,(u,v,c,w) in zip(amounts,edges):
                balance[u]-=amount
                balance[v]+=amount
                cost+=amount*w
            f=balance[-1]
            if not 0<=f<=limit or balance[0]!=-f or any(balance[1:-1]):
                continue
            if f>best_flow or f==best_flow and cost<best_cost:
                best_flow,best_cost=f,cost
        eq('min_cost_flow',mod('min_cost_flow')['min_cost_flow'](n,edges,0,n-1,limit),(best_flow,best_cost))
    # 最初に選んだ割当を逆辺で取り消す必要がある例。
    edges=[(0,1,1,0),(0,2,1,0),(1,3,1,0),(1,4,1,1),(2,3,1,1),(2,4,1,100),(3,5,1,0),(4,5,1,0)]
    eq('min_cost_flow',mod('min_cost_flow')['min_cost_flow'](6,edges,0,5,2),(2,2))


def stress_structure():
    # 最大制約ベンチマークではなく、深い木で再帰制限に依存しないことの検証。
    n=2500
    graph=graph_of(n,[(i,i+1) for i in range(n-1)])
    eq('dfs',len(mod('dfs')['tree_order'](graph)[1]),n)
    eq('doubling_lca',mod('doubling_lca')['LCA'](graph).distance(0,n-1),n-1)
    eq('rerooting',mod('rerooting')['all_distance_sums'](graph)[0],n*(n-1)//2)
    eq('hld',mod('hld')['HLDPathSum'](graph,[1]*n).path_sum(0,n-1),n)
    graph=graph_of(n,[(i,i+1) for i in range(n-1)],True)
    eq('scc',len(mod('scc')['scc'](graph)[1]),n)
    flow=mod('max_flow')['Dinic'](n)
    for i in range(n-1):
        flow.add_edge(i,i+1,10**40)
    eq('max_flow',flow.flow(0,n-1),10**40)

