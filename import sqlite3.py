# === Importações básicas ===
import sqlite3
from datetime import datetime

# === 1. Inicializar o banco de dados ===
def criar_banco():
    con = sqlite3.connect("emocional.db")
    cursor = con.cursor()

    # Criação da tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Criação da tabela de emoções
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emocao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            data TEXT,
            emocao TEXT,
            intensidade INTEGER,
            situacao TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    con.commit()
    con.close()


# === 2. Cadastro de usuário ===
def cadastrar_usuario():
    print("\n===== CADASTRO DE USUÁRIO =====")
    nome = input("Digite seu nome: ")
    idade = input("Digite sua idade: ")
    email = input("Digite seu email: ")
    senha = input("Crie uma senha: ")

    # Verifica se os campos foram preenchidos
    if not nome or not idade or not email or not senha:
        print("Todos os campos são obrigatórios!")
        return None

    try:
        idade = int(idade)
    except ValueError:
        print("A idade deve ser um número.")
        return None

    # Salva no banco
    con = sqlite3.connect("emocional.db")
    cursor = con.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nome, idade, email, senha) VALUES (?, ?, ?, ?)",
                       (nome, idade, email, senha))
        con.commit()
        print(" Cadastro feito com sucesso!")
        return cursor.lastrowid, nome  # Retorna o ID e nome do usuário
    except sqlite3.IntegrityError:
        print("Esse email já está cadastrado.")
        return None
    finally:
        con.close()


# === 3. Menu principal ===
def mostrar_menu(usuario_id, nome):
    while True:
        print(f"\n Olá, {nome}! Escolha uma opção:")
        print("1. Registrar uma emoção")
        print("2. Ver histórico de emoções")
        print("3. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == "1":
            registrar_emocao(usuario_id)
        elif opcao == "2":
            ver_historico(usuario_id)
        elif opcao == "3":
            print(" Até logo!")
            break
        else:
            print(" Opção inválida. Tente novamente.")


# === 4A. Registrar emoção ===
def registrar_emocao(usuario_id):
    print("\n--- Registrar Emoção ---")
    emocao = input("Qual emoção você está sentindo? ")
    intensidade = input("Qual a intensidade (0 a 10)? ")
    situacao = input("O que causou isso? ")

    data = datetime.now().strftime("%Y-%m-%d %H:%M")

    con = sqlite3.connect("emocional.db")
    cursor = con.cursor()

    cursor.execute("INSERT INTO emocao (usuario_id, data, emocao, intensidade, situacao) VALUES (?, ?, ?, ?, ?)",
                   (usuario_id, data, emocao, intensidade, situacao))
    con.commit()
    con.close()
    print("Emoção registrada com sucesso!")


# === 4B. Ver histórico ===
def ver_historico(usuario_id):
    con = sqlite3.connect("emocional.db")
    cursor = con.cursor()

    cursor.execute("SELECT data, emocao, intensidade, situacao FROM emocao WHERE usuario_id = ?", (usuario_id,))
    registros = cursor.fetchall()
    con.close()

    if not registros:
        print("Nenhum registro encontrado.")
        return

    print("\n=== Histórico de Emoções ===")
    for data, emocao, intensidade, situacao in registros:
        print(f"{data} | Emoção: {emocao} | Intensidade: {intensidade} | Situação: {situacao}")


# === Execução principal ===
criar_banco()

dados = cadastrar_usuario()
if dados:
    user_id, nome = dados
    mostrar_menu(user_id, nome)
