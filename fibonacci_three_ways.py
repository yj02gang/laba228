import sys
import time
import matplotlib.pyplot as plt

sys.setrecursionlimit(20000)

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 1.0,
    "grid.color": "#cccccc",
    "grid.linewidth": 0.7,
    "figure.dpi": 110,
})


def fib_rec(n):
    return n if n < 2 else fib_rec(n - 1) + fib_rec(n - 2)


def fib_memo(n, cache=None):
    if cache is None:
        cache = {}
    if n < 2:
        return n
    if n in cache:
        return cache[n]
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]


def fib_dp(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


print("Контрольные значения:")
print(f"{'N':<6}{'рекурсия':<15}{'мемоhизация':<15}{'ДП':<15}")
for n in (10, 20, 30):
    print(f"{n:<6}{fib_rec(n):<15}{fib_memo(n, {}):<15}{fib_dp(n):<15}")


def measure(func, n_values, reset_cache=False):
    times = []
    for n in n_values:
        t0 = time.perf_counter()
        if reset_cache:
            func(n, {})
        else:
            func(n)
        times.append(time.perf_counter() - t0)
    return times


Ns_rec = list(range(5, 31, 2))
t_rec = measure(fib_rec, Ns_rec)

print("\nВремя рекурсии:")
for n, t in zip(Ns_rec, t_rec):
    print(f"  N = {n:<4}  t = {t:.6f} с")

Ns_big = list(range(200, 10001, 400))
t_memo = measure(fib_memo, Ns_big, reset_cache=True)
t_dp = measure(fib_dp, Ns_big)

print("\nВремя мемоhизации (фрагмент):")
for n, t in zip(Ns_big[::5], t_memo[::5]):
    print(f"  N = {n:<6}  t = {t:.6f} с")

print("\nВремя динамического программирования (фрагмент):")
for n, t in zip(Ns_big[::5], t_dp[::5]):
    print(f"  N = {n:<6}  t = {t:.6f} с")


def draw_plot(x, y, title, color, log_scale=False, filename=None):
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(
        x, y,
        marker='o',
        markersize=6,
        markerfacecolor=color,        
        markeredgecolor=color,       
        markeredgewidth=1.2,
        linewidth=1.8,
        color=color,
    )
    if log_scale:
        ax.set_yscale('log')
    ax.set_xlabel('N — номер числа Фибоначчи')
    ax.set_ylabel('время, с')
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    if filename:
        fig.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()


draw_plot(Ns_rec, t_rec, 'Рекурсия', color='#1f4e79',
          log_scale=True, filename='fib_rec.png')

draw_plot(Ns_big, t_memo, 'Меморизация', color='#8b4513',
          filename='fib_memo.png')

draw_plot(Ns_big, t_dp, 'Динамическое программирование', color='#2e7d32',
          filename='fib_dp.png')


print("\nСводка по всем методам (первая и последняя точки):")
print(f"{'N':<8}{'рекурсия':<14}{'меморизация':<14}{'ДП':<14}")
print(f"{Ns_rec[0]:<8}{t_rec[0]:<14.6f}{'—':<14}{'—':<14}")
print(f"{Ns_rec[-1]:<8}{t_rec[-1]:<14.6f}{'—':<14}{'—':<14}")
print(f"{Ns_big[0]:<8}{'—':<14}{t_memo[0]:<14.6f}{t_dp[0]:<14.6f}")
print(f"{Ns_big[-1]:<8}{'—':<14}{t_memo[-1]:<14.6f}{t_dp[-1]:<14.6f}")