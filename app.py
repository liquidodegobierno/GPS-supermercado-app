import streamlit as st
import matplotlib.pyplot as plt
import json, heapq
from itertools import combinations

# =============================
# 1. JSON del supermercado
# =============================
supermercado_json = """ ... (tu JSON de antes aquí) ... """
data = json.loads(supermercado_json)
grafo = data["nodos"]
estantes = data["estantes"]
entrada = data["entrada"]

# =============================
# 2. Coordenadas
# =============================
# Coordenadas de los nodos en el plano (X, Y)
coordenadas = {
    "A4": (0, 4), "A3": (0, 3), "A2": (0, 2), "A1": (0, 1), "A0": (0, 0),
    "B4": (1, 4), "B3": (1, 3), "B2": (1, 2), "B1": (1, 1), "B0": (1, 0),
    "C4": (2, 4), "C3": (2, 3), "C2": (2, 2), "C1": (2, 1), "C0": (2, 0),
    "D4": (3, 4), "D3": (3, 3), "D2": (3, 2), "D1": (3, 1), "D0": (3, 0),
    "E4": (4, 4), "E3": (4, 3), "E2": (4, 2), "E1": (4, 1), "E0": (4, 0)
}


# =============================
# 3. Dijkstra
# =============================
def dijkstra_path(grafo, start, goal):
    dist = {n: float("inf") for n in grafo}
    prev = {n: None for n in grafo}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == goal: break
        for v in grafo.get(u, []):
            if v not in grafo: continue
            nd = d + 1
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))

# =============================
# 4. Held-Karp TSP
# =============================
def tsp_route(targets, grafo, entrada):
    dist, path_map = {}, {}
    for a in targets:
        for b in targets:
            if a == b: continue
            p = dijkstra_path(grafo, a, b)
            dist[(a,b)] = len(p)-1
            path_map[(a,b)] = p

    n = len(targets)
    C, parent = {}, {}
    for k in range(1, n-1):
        C[(1<<k, k)] = dist[(targets[0], targets[k])]
        parent[(1<<k, k)] = 0

    from itertools import combinations
    for s in range(2, n-1):
        for subset in combinations(range(1,n-1), s):
            bits = sum(1<<bit for bit in subset)
            for k in subset:
                prev_bits = bits & ~(1<<k)
                best, argmin = float("inf"), None
                for m in subset:
                    if m==k: continue
                    val = C[(prev_bits,m)] + dist[(targets[m], targets[k])]
                    if val < best: best, argmin = val, m
                C[(bits,k)] = best
                parent[(bits,k)] = argmin

    bits_all = (1<<(n-1)) - 2
    best_cost, last = float("inf"), None
    for k in range(1,n-1):
        val = C[(bits_all,k)] + dist[(targets[k], targets[-1])]
        if val < best_cost: best_cost, last = val, k

    route_idx = [n-1, last]
    bits, cur = bits_all, last
    while bits:
        prev = parent[(bits,cur)]
        bits &= ~(1<<cur)
        cur = prev
        if cur != 0:
            route_idx.append(cur)
    route_idx.append(0)
    route_idx = route_idx[::-1]

    full_path = []
    for i in range(len(route_idx)-1):
        a, b = targets[route_idx[i]], targets[route_idx[i+1]]
        seg = path_map[(a,b)]
        if not full_path: full_path.extend(seg)
        else: full_path.extend(seg[1:])
    return full_path, best_cost

# =============================
# 5. Dibujar ruta
# =============================
def dibujar_ruta(ruta, lista_compra):
    fig, ax = plt.subplots(figsize=(6,6))
    for nodo, vecinos in grafo.items():
        for vecino in vecinos:
            if nodo in coordenadas and vecino in coordenadas:
                x1,y1 = coordenadas[nodo]; x2,y2 = coordenadas[vecino]
                ax.plot([x1,x2],[y1,y2],"lightgray",linestyle="--",zorder=1)
    for nodo,(x,y) in coordenadas.items():
        if nodo in estantes:
            ax.scatter(x,y,c="orange",s=200,marker="s",zorder=2)
            ax.text(x,y+0.2,nodo,ha="center",fontsize=8)
        else:
            ax.scatter(x,y,c="skyblue",s=100,zorder=2)
            ax.text(x,y-0.2,nodo,ha="center",fontsize=8)
    xs=[coordenadas[n][0] for n in ruta]
    ys=[coordenadas[n][1] for n in ruta]
    ax.plot(xs,ys,c="red",linewidth=2,zorder=3)
    ax.set_title(f"Ruta para: {', '.join(lista_compra)}")
    ax.axis("off")
    st.pyplot(fig)

# =============================
# 6. Interfaz Streamlit
# =============================
st.title("🛒 Guía de supermercado")

lista_texto = st.text_input("Introduce tu lista de compra (separa con comas)", "Latas, Preparados, Panaderia")
if st.button("Generar ruta"):
    lista_compra = [p.strip() for p in lista_texto.split(",") if p.strip()]
    targets = [entrada] + [estantes[p] for p in lista_compra if p in estantes] + [entrada]
    ruta, costo = tsp_route(targets, grafo, entrada)

    st.write("### Lista de compra:", lista_compra)
    st.write("### Ruta óptima:", " → ".join(ruta))
    st.write(f"### Coste (nº pasos): {costo}")

    dibujar_ruta(ruta, lista_compra)
