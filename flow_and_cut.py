from collections import deque
#  Часть 1. Поиск максимального потока и минимального разреза

def edmonds_karp(u, s, t, names):
    n = len(u)
    r = [row[:] for row in u]              
    flow = [[0] * n for _ in range(n)]
    total = 0
    log = []

    while True:
        prev = [-1] * n
        prev[s] = s
        q = deque([s])
        while q and prev[t] == -1:
            x = q.popleft()
            for y in range(n):
                if prev[y] == -1 and r[x][y] > 0:
                    prev[y] = x
                    q.append(y)
        if prev[t] == -1:
            break

        path, cur = [], t
        while cur != s:
            path.append(cur)
            cur = prev[cur]
        path.append(s)
        path.reverse()

        delta = min(r[path[i]][path[i + 1]] for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            x, y = path[i], path[i + 1]
            flow[x][y] += delta
            r[x][y] -= delta
            r[y][x] += delta
        total += delta
        log.append(([names[v] for v in path], delta))

    seen = [False] * n
    seen[s] = True
    q = deque([s])
    while q:
        x = q.popleft()
        for y in range(n):
            if not seen[y] and r[x][y] > 0:
                seen[y] = True
                q.append(y)
    S = [names[i] for i in range(n) if seen[i]]
    T = [names[i] for i in range(n) if not seen[i]]
    return total, flow, (S, T), log

#  Часть 2. Пересчёт при увеличении дуг минимального разреза

def recompute(ac=4, dt=8):
    cap2 = [row[:] for row in cap]         
    cap2[index['a']][index['c']] = ac
    cap2[index['d']][index['t']] = dt
    return edmonds_karp(cap2, index['s'], index['t'], names)


def print_table(title, key_name, key_values, key_param):
    print("=" * 70)
    print(title)
    print("=" * 70)
    print(f"{key_name:<14}{'|x*|':<10}{'минимальный разрез':<35}")
    print("-" * 70)
    for val in key_values:
        result = recompute(**{key_param: val})
        v, _, (S, T), _ = result
        cut = "{" + ", ".join(S) + "} | {" + ", ".join(T) + "}"
        print(f"{val:<14}{v:<10g}{cut:<35}")
    print()


#  Исходные данные варианта 4

names = ['s', 'a', 'b', 'c', 'd', 't']
index = {name: k for k, name in enumerate(names)}
arcs = [('s', 'a', 8), ('s', 'b', 9), ('a', 'c', 4), ('a', 'd', 5),
        ('b', 'd', 7), ('c', 't', 6), ('d', 't', 8)]

n = len(names)
cap = [[0] * n for _ in range(n)]
for i, j, c in arcs:
    cap[index[i]][index[j]] = c


val, flow, (S, T), log = edmonds_karp(cap, index['s'], index['t'], names)

print("Исходная задача:")
print(f"  Максимальный поток |x*| = {val}")
print(f"  Минимальный разрез     = S = {S}, T = {T}")
print()

print_table(
    title="Увеличение только дуги (a, c)",
    key_name="u(a, c)",
    key_values=[4, 5, 6, 7, 20],
    key_param="ac",
)

print_table(
    title="Увеличение только дуги (d, t)",
    key_name="u(d, t)",
    key_values=[8, 10, 12, 14, 20],
    key_param="dt",
)