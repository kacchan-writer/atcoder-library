# AtCoder Python Library

Pythonの典型アルゴリズム48種と、出典URLを自動挿入するVS Codeスニペット。
標準ライブラリだけで動きます。各ファイルの冒頭に用途・条件・計算量・APIを記載しています。

**収録した48種の実装はすべてOpenAI CodexによるAI生成コードです。**
確認済みの参照資料と、日本の著作権法に基づく運用方針は [PROVENANCE.md](PROVENANCE.md) に記載しています。

## VS Codeで使う

1. `snippets/atcoder-python.code-snippets` を、作業フォルダの `.vscode/` にコピーします。
2. `.py` ファイルの行頭で `acuf` などを入力し、`Ctrl+Space` で候補を選びます。
3. `editor.tabCompletion` を `onlySnippets` にすると、呼出名の後に `Tab` でも展開できます。

JSON形式の `.code-workspace` を使っている場合は、次のコマンドでも導入できます。
最初の作業フォルダにスニペットを配置し、Tab展開を設定します。既存ファイルを変更する場合はバックアップします。

```sh
python tools/install_snippets.py --workspace-file /path/to/AtCoder.code-workspace
```

フォルダを直接開いている場合は `--folder /path/to/project` を指定してください（この場合は設定を変更しません）。
[VS Code公式スニペットガイド](https://code.visualstudio.com/docs/editing/userdefinedsnippets)

例えば `acuf` で出典コメントと `DSU` の定義を展開した後、下に `uf = DSU(N)` と書いて使います。
`acbfs` はBFS、`acseg` はセグメント木、`acbs` は二分探索です。
スニペットは各ファイルの関数・クラス・importを挿入します。末尾の実行例は挿入しません。
入力処理、関数の呼び出し、答えの出力は問題に合わせて記述してください。

## コンテストで使う前に

[AtCoder公式ルール（2026-10-14確認）](https://info.atcoder.jp/entry/llm-rules-ja)では、
AIで事前作成したコードは開始前のWeb公開と、コピー時の参照URL添付が条件です。
AI利用の明示は不要とされています。開催中のAI生成・修正・補完は原則禁止です。

- 使用する版がコンテスト開始前に**公開済み**であることを確認してください。ローカルの作成日・commit日時だけでは公開の証拠になりません。
- 展開した `# Source: https://github.com/.../blob/<commit>/...` を提出コードに残してください。
- スニペットは変更されないコミットを参照します。更新する場合も、対象コードとスニペットを開始前にpushしてください。
- 手動コピーするときはGitHubでそのファイルのpermalinkを取り、同様にコメントへ添付してください。
- 静的なスニペット展開は保存済み文字列の挿入です。AI補完機能とは別です。

公式の対象は開催中のABC・ARC・AGCです。適用時には最新の公式規定も確認してください。

## 収録一覧

| 呼出名 | 典型・コード | 主なAPI |
|---|---|---|
| `acsum` | [累積和・二次元累積和](library/prefix_sum.py) | prefix_sum(a)、range_sum(p,l,r)、prefix_sum_2d(grid)、rect_sum(p,top,left,bottom,right)。 |
| `acfreq` | [辞書・出現回数・同じ値のペア](library/frequency.py) | equal_pairs(a) -> 同値ペア数。Counter(a) -> 値ごとの頻度。 |
| `acbs` | [二分探索・bisect](library/binary_search.py) | boundary(ok,ng,check)。bisect_left(a,x)はx以上が始まる位置、bisect_rightはxより大きい位置。 |
| `acimos` | [いもす法・差分配列](library/imos.py) | imos(n, updates)。updatesは(l,r,加算値)の列。 |
| `accoord` | [座標圧縮](library/coordinate_compression.py) | compress(a) -> (圧縮後の列, 番号から元の値へ戻す列)。 |
| `acbit` | [bit全探索](library/bit_enumeration.py) | count_subset_sum(a,target) -> 合計がtargetになる部分集合の個数。 |
| `acnum` | [GCD・約数列挙・素数のふるい](library/number_theory.py) | gcd(a,b)、lcm(a,b)、divisors(n)、sieve(n) -> n以下の素数リスト。 |
| `acmerge` | [区間の合併](library/interval_merge.py) | merge_intervals(intervals) -> [(l,r), ...]。 |
| `actwo` | [尺取り法](library/two_pointers.py) | count_sum_at_most(a,k)。 |
| `acsumk` | [累積和＋辞書](library/prefix_hash.py) | count_sum_equal(a,k)。 |
| `acbfs` | [BFS・多始点BFS](library/bfs.py) | bfs(graph,sources) -> 距離。grid_bfs(grid,start) -> 四近傍距離。 |
| `acdfs` | [DFS・連結成分・木の帰りがけ順](library/dfs.py) | components(graph) -> 成分番号。tree_order(graph,root) -> (親配列,親が先の順序)。 |
| `acuf` | [Union-Find / DSU](library/union_find.py) | DSU(n)。merge(a,b)は併合したらTrue、same(a,b)、size(a)、leader(a)。 |
| `acheap` | [ヒープ・上位K個の維持](library/heap.py) | TopK(k).add(x)、.total。heapqは最小ヒープ。 |
| `acgreedy` | [貪欲法・区間スケジューリング](library/interval_greedy.py) | schedule(intervals) -> 採用する区間の列。 |
| `acknap` | [動的計画法・0/1ナップサック](library/knapsack.py) | knapsack(items,capacity)。itemsは(重量,価値)の列。 |
| `acdijkstra` | [Dijkstra法](library/dijkstra.py) | dijkstra(graph,start)。graph[v]は(行先,重み)の列。 |
| `actopo` | [トポロジカルソート・DAG上のDP](library/topological_sort.py) | topological_sort(graph) -> 順序またはNone。longest_path(graph)。 |
| `aclis` | [最長増加部分列 / LIS](library/lis.py) | lis_length(a) -> 長さ。 |
| `acbitree` | [Fenwick Tree / BIT・転倒数](library/fenwick_tree.py) | Fenwick(n).add(i,x)、prefix(r)、sum(l,r)。inversions(a)。 |
| `acseg` | [セグメント木](library/segment_tree.py) | SegTree(a,op,e).set(i,x)、prod(l,r)。例: 和はop=lambda a,b:a+b、e=0。 |
| `accomb` | [組合せ・階乗・逆元](library/combinations.py) | Combinations(N,mod).choose(n,r)。0<=n<=N、範囲外のrは0。 |
| `acmitm` | [半分全列挙](library/meet_in_middle.py) | subset_sums(a)、count_subset_sum(a,target)。 |
| `actsp` | [bit DP・巡回セールスマン](library/bit_dp.py) | tsp(cost) -> 最小巡回費用またはinf。costはN×N。 |
| `ac01bfs` | [0-1 BFS](library/zero_one_bfs.py) | zero_one_bfs(graph,start)。graph[v]は(行先,0または1)。 |
| `acfloyd` | [Warshall-Floyd法](library/floyd_warshall.py) | floyd_warshall(n,edges,directed=True)。edgesは(u,v,w)、未到達inf。 |
| `ackruskal` | [最小全域木・Kruskal法](library/kruskal.py) | kruskal(n,edges) -> (合計費用,採用辺)。edgesは(u,v,w)。 |
| `aclca` | [ダブリング・LCA](library/doubling_lca.py) | LCA(graph,root=0).lca(u,v)、ancestor(v,k)、distance(u,v)。 |
| `actreedp` | [木DP・独立集合の数え上げ](library/tree_dp.py) | independent_sets(graph,mod=1000000007)。 |
| `acdigitdp` | [桁DP](library/digit_dp.py) | count_digit_sum_multiple(bound,divisor,mod=1000000007)。 |
| `acintervaldp` | [区間DP・隣接併合](library/interval_dp.py) | merge_cost(a) -> 最小総費用。 |
| `acz` | [Z algorithm・文字列の前方一致](library/z_algorithm.py) | z_algorithm(s) -> 各suffixとsの最長共通接頭辞の長さ。 |
| `acscc` | [強連結成分分解 / SCC](library/scc.py) | scc(graph) -> (各頂点の成分番号, 成分ごとの頂点リスト)。 |
| `ac2sat` | [2-SAT](library/two_sat.py) | two_sat(n,clauses) -> bool列またはNone。節(i,f,j,g)は(x_i==f) OR (x_j==g)。 |
| `aclazy` | [遅延セグメント木・区間加算と区間和](library/lazy_segment_tree.py) | RangeAddSum(a).add(l,r,x)、sum(l,r)。再帰の深さはO(log N)。 |
| `acreroot` | [全方位木DP・全頂点からの距離和](library/rerooting.py) | all_distance_sums(graph) -> 各頂点から全頂点への距離和。 |
| `acmo` | [Moのアルゴリズム・区間の種類数](library/mo.py) | distinct_queries(a,queries) -> 入力順の答え。queriesは(l,r)。 |
| `acmat` | [行列累乗](library/matrix_power.py) | matmul(a,b,mod)、matpow(a,exponent,mod=1000000007)。 |
| `acflow` | [最大流・最小カット / Dinic](library/max_flow.py) | Dinic(n).add_edge(u,v,cap)、flow(s,t)、min_cut(s) -> 到達可否。 |
| `acmatching` | [二部マッチング・増加路](library/bipartite_matching.py) | matching(graph,right_size) -> (個数,各左頂点の相手)。graphは左→右の隣接リスト、未割当-1。 |
| `acntt` | [NTT・畳み込み](library/ntt.py) | convolution(a,b) -> 長さlen(a)+len(b)-1の係数。空列を含むと[]。 |
| `acmcf` | [最小費用流・ポテンシャル](library/min_cost_flow.py) | min_cost_flow(n,edges,s,t,limit) -> (流量,総費用)。edgesは(u,v,容量,単位費用)。毎回新規計算。 |
| `achld` | [Heavy-Light Decomposition / 重軽分解](library/hld.py) | HLDPathSum(graph,values).add(v,x)、path_sum(u,v)。両端の頂点も含む。 |
| `aclichao` | [Li Chao Tree・直線の最小値](library/li_chao_tree.py) | LiChao(xs).add_line(a,b)、query(x)。xは初期xs内の値。 |
| `acrollback` | [Rollback Union-Find](library/rollback_dsu.py) | RollbackDSU(n).merge(a,b)、same(a,b)、snapshot()、rollback(token)。 |
| `acsos` | [部分集合ゼータ変換・Möbius反転 / SOS DP](library/sos_dp.py) | subset_zeta(a)、subset_mobius(a)。元配列を変更せず新しいリストを返す。 |
| `acsa` | [Suffix Array・LCP](library/suffix_array.py) | suffix_array(s)、lcp_array(s,sa)。lcp[i]はsa[i]とsa[i+1]の一致長。 |
| `achull` | [凸包・単調鎖法](library/convex_hull.py) | convex_hull(points) -> 反時計回りの頂点列。始点は末尾に重複しない。cross(o,a,b)は外積。 |

詳しい適用条件・計算量と練習問題のリンクは [catalog.json](catalog.json) にあります。
分類C〜G・それ以上は学習上の目安で、公式難易度や出題位置ではありません。

## 複数の典型を組み合わせる

グローバル名が重複するコードがあります。両方を貼る際は同名の関数・補助クラスを確認し、必要なら手動で名前を変えてください。
例えばbit全探索と半分全列挙の `count_subset_sum` は同じ目的の別実装です。

- `count_subset_sum`: bit_enumeration, meet_in_middle
- `scc`: scc, two_sat

## 検証

```sh
python -B tests/verify.py
python -B tests/verify.py --snippets
```

前者は48個のデモ・全探索などの独立な小規模参照解・境界ケース・2500頂点の構造チェックを行います。
後者は実際のスニペットを復元して同じ参照解と照合し、公開コードとの一致・参照コミットを確認します。
今回の公開版の検証結果は [docs/validation.json](docs/validation.json) に記録しています。
再実行時の結果は `.validation/source.json` と `.validation/snippets.json` に保存されます。
AtCoderへの提出・ACや各問題の最大制約での速度は未確認です。
とくにNTT、Mo、2-SAT、遅延セグメント木などはPythonでの実行時間・メモリを別途判断してください。
実装はAI生成のPython教材由来で、公式AC Libraryと同一のAPI・性能ではありません。

## スニペットを更新する

コンテスト開始前に実行してください。

1. 実装・索引・出典説明（`library/`、`catalog.json`、`PROVENANCE.md`）の変更を検証し、Gitにコミットします。
2. `python tools/build_snippets.py --ref HEAD` を実行します。
3. `python -B tests/verify.py --snippets` を実行します。
4. 生成された `snippets/` をコミットしてpushし、対象コミットが公開状態で見えることを確認します。
5. 作業フォルダの `.vscode/` に新しいスニペットをコピーします。

生成器はローカルの未コミットの変更を取り込まず、指定コミットのコードと現在のコードが違う場合は停止します。
スニペットに埋め込まれた参照先を、コードの内容を確かめずに差し替えないでください。

## コードの出典とAI利用

- **作成方法:** 48種はOpenAI Codexが2026-10-12に生成したPython教材を元にしています。公開用の整理・検証・スニペット・文書の作成にもCodexを使用しています。
- **参照資料:** 作成時に閲覧したAC Library公式資料などを [PROVENANCE.md](PROVENANCE.md) に記録しています。AI生成の表示と、実装のコミット固定URLを各スニペットに添付します。
- **調査・対応の範囲:** 未知のAI学習元を際限なく追跡することを公開の前提にはしません。具体的な転用元や、第三者コードの特徴的な表現との一致が判明した場合は、該当箇所・元作者・元URL・許諾条件を確認し、出典の追記やコードの修正など必要な対応を行います。

日本の著作権法ではアルゴリズム自体は保護対象外で、具体的なコードの創作的表現が保護され得ます。
本リポジトリでは、この区別と類似性・依拠性を基準に扱います。出典やAI利用の表示だけで利用許諾の代わりにはなりません。
根拠と運用の詳細は [PROVENANCE.md](PROVENANCE.md) を参照してください。

第三者向けの利用ライセンスは未設定です。
