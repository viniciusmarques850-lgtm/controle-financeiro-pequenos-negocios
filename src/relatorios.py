import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # necessário no Windows sem interface gráfica

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import conectar

REPORTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'docs', 'prints')

def grafico_por_categoria(ano, mes):
    """Gera gráfico de barras com gastos por categoria no mês."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT categoria, SUM(valor) as total
        FROM lancamentos
        WHERE tipo = 'saida'
        AND strftime('%Y', data) = ?
        AND strftime('%m', data) = ?
        GROUP BY categoria
        ORDER BY total DESC
    ''', (str(ano), str(mes).zfill(2)))

    dados = cursor.fetchall()
    conn.close()

    if not dados:
        print("Nenhum dado encontrado para esse periodo.")
        return

    categorias = [row['categoria'] for row in dados]
    valores = [row['total'] for row in dados]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(categorias, valores, color='#e74c3c')

    ax.set_title(f'Gastos por Categoria — {mes:02d}/{ano}', fontsize=14)
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Total (R$)')

    for bar, valor in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 5,
                f'R${valor:.2f}',
                ha='center', fontsize=10)

    plt.tight_layout()

    nome_arquivo = os.path.join(REPORTS_PATH, f'gastos_{ano}_{mes:02d}.png')
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Grafico salvo em: {nome_arquivo}")

if __name__ == '__main__':
    grafico_por_categoria(2026, 7)