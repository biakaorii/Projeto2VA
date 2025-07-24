import sqlite3    
import datetime    # para trabalhar com datas e horários

# classe para gerenciar o banco de dados 
class BancoDeDados:
    # inicializando a conexão com o banco de dados
    def __init__(self, nome_arquivo='emocional.db'):
        self.conn = sqlite3.connect(nome_arquivo)
        self.cursor = self.conn.cursor()
        # chama o método para criar as tabelas necessárias
        self.criar_tabelas()

    # responsável por criar todas as tabelas necessárias
    def criar_tabelas(self):
        # cria tabela de usuários com campos: id, nome, idade, email e senha
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chave primária auto incremento
            nome TEXT NOT NULL,                     -- Nome obrigatório
            idade INTEGER,                          -- Idade (opcional)
            email TEXT UNIQUE,                      -- Email único
            senha TEXT NOT NULL                     -- Senha obrigatória
        )''')

        # cria tabela do diário com campos: id, usuario_id, texto e data
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chave primária auto incremento
            usuario_id INTEGER,                     -- Referência ao usuário
            texto TEXT,                             -- Conteúdo do diário
            data TEXT,                              -- Data da entrada
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)  -- Chave estrangeira
        )''')

        # cria tabela de reflexões com campos: id, usuario_id, pergunta, resposta e data
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reflexoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chave primária auto incremento
            usuario_id INTEGER,                     -- Referência ao usuário
            pergunta TEXT,                          -- Pergunta da reflexão
            resposta TEXT,                          -- Resposta do usuário
            data TEXT,                              -- Data da reflexão
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)  -- Chave estrangeira
        )''')

        # cria tabela de emoções com campos: id, usuario_id, emocao, intensidade e data
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS emocao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chave primária auto incremento
            usuario_id INTEGER,                     -- Referência ao usuário
            emocao TEXT,                            -- Nome da emoção
            intensidade INTEGER,                    -- Intensidade de 1 a 10
            data TEXT,                              -- Data do registro
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)  -- Chave estrangeira
        )''')

        # salva todas as alterações no banco de dados
        self.conn.commit()

    # para fechar a conexão com o banco de dados
    def fechar(self):
        self.conn.close()

# classe responsável por gerenciar usuários (cadastro e login)
class Usuario:
    def __init__(self, banco):
        self.banco = banco  # referência ao banco de dados
        self.id = None      # ID do usuário
        self.nome = ""      # nome do usuário

    # para cadastrar um novo usuário no sistema
    def cadastrar(self, nome, idade, email, senha):
        try:
            # tenta inserir o novo usuário no banco de dados
            self.banco.cursor.execute("INSERT INTO usuarios (nome, idade, email, senha) VALUES (?, ?, ?, ?)", (nome, idade, email, senha))
            # confirma a inserção no banco
            self.banco.conn.commit()
            print("Cadastro feito com sucesso!")
        except sqlite3.IntegrityError:
            # se o email já existe, mostra erro
            print("Email cadastrado. Tente novamente.")

    # para fazer login no sistema
    def login(self, email, senha):
        # busca no banco um usuário com o email e senha fornecidos
        self.banco.cursor.execute("SELECT id, nome FROM usuarios WHERE email=? AND senha=?", (email, senha))
        resultado = self.banco.cursor.fetchone()  # pega o primeiro resultado
        if resultado:
            # se encontrou o usuário, salva os dados na instância
            self.id = resultado[0]    # ID do usuário
            self.nome = resultado[1]  # Nome do usuário
            return True  # login sucedido
        return False     # login falhou

# classe responsável por gerenciar o diário pessoal do usuário
class Diario:
    def __init__(self, banco, usuario):
        self.banco = banco      # referência ao banco de dados
        self.usuario = usuario  # referência ao usuário logado

    # para escrever uma nova entrada no diário
    def escrever(self):
        # solicita ao usuário o texto do diário
        texto = input("\nEscreva seu diário de hoje: ")
        # pega a data e hora atual 
        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # insere a entrada do diário no banco de dados
        self.banco.cursor.execute("INSERT INTO diario (usuario_id, texto, data) VALUES (?, ?, ?)", (self.usuario.id, texto, data))
        # confirma a inserção no banco
        self.banco.conn.commit()
        print("Diário salvo!")

    # visualizar entradas do diário
    def ver_diario(self):
        print("\nEntradas do Diário:")
        self.banco.cursor.execute("SELECT texto, data FROM diario WHERE usuario_id=? ORDER BY data DESC", (self.usuario.id,))
        entradas = self.banco.cursor.fetchall()
        if not entradas:
            print("Nenhuma entrada no diário ainda.")
        else:
            for texto, data in entradas:
                print(f"{data}: {texto}")

# classe responsável por gerenciar reflexões do usuário
class Reflexao:
    def __init__(self, banco, usuario):
        self.banco = banco     
        self.usuario = usuario  

    # conduz o usuário através de perguntas
    def refletir(self):
        # lista de perguntas para reflexão
        perguntas = [
            "O que te fez mais alegre hoje?",
            "Você enfrentou algo difícil hoje? Como lidou?",
            "Algo que gostaria de lembrar?",
        ]
        # loop de cada pergunta
        for pergunta in perguntas:
            print(f"\n{pergunta}")  # exibe a pergunta
            resposta = input("Sua resposta: ")  # coleta a resposta do usuário
            data = datetime.datetime.now().strftime("%Y-%m-%d")  # pega a data atual
            # salva a pergunta e resposta no banco de dados
            self.banco.cursor.execute("INSERT INTO reflexoes (usuario_id, pergunta, resposta, data) VALUES (?, ?, ?, ?)",
                                      (self.usuario.id, pergunta, resposta, data))
            self.banco.conn.commit()  # confirma a inserção
        print("\nReflexão concluída e salva!")  # mensagem de conclusão

# classe responsável por registrar o estado emocional do usuário
class TermometroEmocional:
    def __init__(self, banco, usuario):
        self.banco = banco     
        self.usuario = usuario  

    # para registrar uma nova emoção
    def registrar_emocao(self):
        # solicita ao usuário qual emoção está sentindo
        emocao = input("\nComo você está se sentindo agora (ex: feliz, triste, ansioso...)? ")
        # solicita a intensidade da emoção numa escala de 1 a 10
        intensidade = input("De 1 a 10, qual a intensidade dessa emoção? ")
        # pega a data e hora atual
        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # salva a emoção no banco de dados
        self.banco.cursor.execute("INSERT INTO emocao (usuario_id, emocao, intensidade, data) VALUES (?, ?, ?, ?)",
                                  (self.usuario.id, emocao, intensidade, data))

        self.banco.conn.commit()  # confirma a inserção
        print("emoção registrada")

    # para visualizar o histórico de emoções do usuário
    def ver_historico(self):
        print("\nHistórico de emoções:")
        # busca todas as emoções do usuário ordenadas por data (mais recente primeiro)
        self.banco.cursor.execute("SELECT emocao, intensidade, data FROM emocao WHERE usuario_id=? ORDER BY data DESC", (self.usuario.id,))
        # exibe cada emoção registrada
        for emocao, intensidade, data in self.banco.cursor.fetchall():
            print(f"{data}: {emocao} (intensidade {intensidade})")

# função que exibe informações de contatos de emergência para apoio emocional
def tela_emergencia():
    print("\n Contatos de Apoio Emocional:")
    print("CVV - 188 (24h, gratuito)")        # Centro de Valorização da Vida
    print("Samu - 192")                       # Serviço de Atendimento Móvel de Urgência
    print("Emergência Policial - 190")       # Polícia Militar

# exibe o menu principal do sistema após o login
def menu(usuario, banco):
    # cria instâncias das classes principais do sistema
    diario = Diario(banco, usuario)                    # para gerenciar o diário
    reflexao = Reflexao(banco, usuario)                # para gerenciar reflexões
    emocional = TermometroEmocional(banco, usuario)    # para gerenciar emoções

    # loop principal do menu
    while True:
        # exibe as opções disponíveis para o usuário
        print(f"\n Olá, {usuario.nome}! Escolha uma opção:")
        print("1. Escrever no diário")        # opção para escrever no diário
        print("2. Modo reflexão")             # opção para fazer reflexões
        print("3. Registrar emoção")          # opção para registrar emoções
        print("4. Ver histórico de emoções")  # opção para ver histórico emocional
        print("5. Ver diário")                # nova opção para visualizar o diário
        print("6. Tela de emergência")        # opção para ver contatos de emergência
        print("7. Sair")                      # opção para sair do sistema

        opcao = input(">> ")  # lê a escolha do usuário

        # executa a escolha do usuário
        if opcao == "1":
            diario.escrever()              # para escrever no diário
        elif opcao == "2":
            reflexao.refletir()            # para fazer reflexão
        elif opcao == "3":
            emocional.registrar_emocao()   # para registrar emoção
        elif opcao == "4":
            emocional.ver_historico()      # para ver histórico
        elif opcao == "5":
            diario.ver_diario()            # visualizar o diário
        elif opcao == "6":
            tela_emergencia()              # tela de emergência
        elif opcao == "7":
            print("Até logo!")             # mensagem de despedida
            break                          # sai do loop (encerra o menu)
        else:
            print("Opção inválida!")       # mensagem para opção inválida

# função principal do programa
def main():
    # inicializa o banco de dados 
    banco = BancoDeDados()
    usuario = Usuario(banco)

    print("Bem-vindo ao Sistema Emocional")  # mensagem para iniciar o programa

    # (tela de login)
    while True:
        # exibe as opções iniciais
        print("\n1. Cadastrar\n2. Login\n3. Sair")
        escolha = input(">> ")  # lê a escolha do usuário

        if escolha == "1":
            # coleta dados do novo usuário
            nome = input("Nome: ")
            idade = input("Idade: ")
            email = input("Email: ")
            senha = input("Senha: ")
            # chama o método de cadastro
            usuario.cadastrar(nome, idade, email, senha)

        elif escolha == "2":
            # coleta credenciais do usuário
            email = input("Email: ")
            senha = input("Senha: ")
            # tenta fazer login
            if usuario.login(email, senha):
                # se login bem-sucedido, entra no menu principal
                menu(usuario, banco)
            else:
                # se login falhou, exibe mensagem de erro
                print("Login falhou. Verifique email ou senha.")

        elif escolha == "3":
            # opção para sair do programa
            print("Saindo...")
            break 

        else:
            # opção inválida
            print("Opção inválida.")

    # fecha a conexão com o banco de dados antes de encerrar
    banco.fechar()

if __name__ == "__main__":
    main()
