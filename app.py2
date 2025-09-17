def dibujar_ruta(ruta, lista_compra):
    fig, ax = plt.subplots(figsize=(6,6))

    # Dibujar conexiones del grafo
    for nodo, vecinos in grafo.items():
        for vecino in vecinos:
            if nodo in coordenadas and vecino in coordenadas:
                x1,y1 = coordenadas[nodo]; x2,y2 = coordenadas[vecino]
                ax.plot([x1,x2],[y1,y2],"lightgray",linestyle="--",zorder=1)

    # Dibujar nodos
    for nodo,(x,y) in coordenadas.items():
        if nodo in estantes.values():
            ax.scatter(x,y,c="orange",s=200,marker="s",zorder=2)
            ax.text(x,y+0.2,nodo,ha="center",fontsize=8,weight="bold")

            # Buscar qué categoría corresponde a este nodo
            for categoria, coord in estantes.items():
                if coord == nodo:
                    ax.text(x,y-0.3,categoria,ha="center",fontsize=8,color="brown")
        else:
            ax.scatter(x,y,c="skyblue",s=100,zorder=2)
            ax.text(x,y-0.2,nodo,ha="center",fontsize=8)

    # Dibujar ruta
    xs=[coordenadas[n][0] for n in ruta]
    ys=[coordenadas[n][1] for n in ruta]
    ax.plot(xs,ys,c="red",linewidth=2,zorder=3)

    ax.set_title(f"Ruta para: {', '.join(lista_compra)}")
    ax.axis("off")
    st.pyplot(fig)
