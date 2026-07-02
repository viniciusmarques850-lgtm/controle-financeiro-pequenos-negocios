from database import conectar
from datetime import date

def adicionar_lancamento(descricao, valor, tipo, categoria, data=None):
    if data is None:
        data = date.today().isoformat()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO lancamentos (descricao, valor, tipo, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (descricao, valor, tipo, categoria, data))

    conn.commit()
    conn.close()
    print(f"Lancamento '{descricao}' adicionado.")

def listar_lancamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lancamentos ORDER BY data DESC')
    lancamentos = cursor.fetchall()
    conn.close()
    return lancamentos

def deletar_lancamento(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lancamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print(f"Lancamento {id} removido.")

def resumo_mes(ano, mes):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tipo, SUM(valor) as total
        FROM lancamentos
        WHERE strftime('%Y', data) = ? AND strftime('%m', data) = ?
        GROUP BY tipo
    ''', (str(ano), str(mes).zfill(2)))

    resultado = cursor.fetchall()
    conn.close()

    resumo = {'entrada': 0.0, 'saida': 0.0}
    for row in resultado:
        resumo[row['tipo']] = row['total']

    resumo['saldo'] = resumo['entrada'] - resumo['saida']
    return resumo