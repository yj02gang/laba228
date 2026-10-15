from itertools import combinations

p = [72, 120, 144, 84, 66, 108]   
a = [12, 24, 36, 30, 27, 42]     
B = 60                           
n = len(p)


def knapsack_greedy(p, a, B):
    order = sorted(range(len(p)), key=lambda i: p[i] / a[i], reverse=True)
    w, v, items = 0, 0, []
    for i in order:
        if w + a[i] <= B:
            w += a[i]
            v += p[i]
            items.append(i + 1)
    return v, sorted(items), w


# 2. Динамическое программирование 
def knapsack_dp(p, a, B):
    n = len(p)
    D = [[0] * (B + 1) for _ in range(n + 1)]
    for k in range(1, n + 1):
        for w in range(B + 1):
            D[k][w] = D[k - 1][w]
            if a[k - 1] <= w:
                D[k][w] = max(D[k][w], p[k - 1] + D[k - 1][w - a[k - 1]])

    w, items = B, []
    for k in range(n, 0, -1):
        if D[k][w] != D[k - 1][w]:
            items.append(k)
            w -= a[k - 1]
    return D[n][B], sorted(items), B - w


#  3. Полный перебор 
def knapsack_bruteforce(p, a, B):
    best_v, best_set = 0, ()
    for mask in range(1 << n):
        w = v = 0
        items = []
        for i in range(n):
            if mask & (1 << i):
                w += a[i]
                v += p[i]
                items.append(i + 1)
        if w <= B and v > best_v:
            best_v = v
            best_set = tuple(items)
    return best_v, sorted(best_set)


v_g, items_g, w_g = knapsack_greedy(p, a, B)
v_dp, items_dp, _ = knapsack_dp(p, a, B)
v_bf, items_bf = knapsack_bruteforce(p, a, B)

print("Удельные ценности p_j / a_j:")
for j in range(n):
    print(f"  предмет {j+1}: {p[j]} / {a[j]} = {p[j]/a[j]:.2f}")

print("\nЖадный алгоритм:")
print(f"  набор = {items_g},  вес = {w_g},  ценность = {v_g}")

print("\nДинамическое программирование:")
print(f"  набор = {items_dp},  ценность = {v_dp}")

print("\nПолный перебор (проверка):")
print(f"  набор = {items_bf},  ценность = {v_bf}")

print("\nСравнение:")
print(f"  жадный     : {v_g}")
print(f"  ДП         : {v_dp}")
print(f"  полный     : {v_bf}")
print(f"  отставание жадного от оптимума: {v_dp - v_g}")
