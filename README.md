# Sistema de Bem-Estar Emocional

Um sistema para acompanhamento e cuidado da saúde mental, desenvolvido em Python com interface de linha de comando.

#  Sobre o Projeto

O Sistema de Bem-Estar Emocional permite aos usuários registrar e acompanhar seu estado emocional através de diferentes ferramentas:

- Diário Pessoal: Escreva seus pensamentos e experiências diárias
- Reflexões Guiadas: Responda perguntas reflexivas para autoconhecimento
- Termômetro Emocional: Registre suas emoções e acompanhe padrões
- Contatos de Emergência: Acesso rápido a linhas de apoio emocional

# Lista de Funcionalidades Desenvolvidas

Funcionalidades Implementadas

1. Sistema de Autenticação
   - Cadastro de novos usuários
   - Validação de email único
   - Sistema de login seguro
   - Proteção de dados por usuário

2. Gerenciamento de Banco de Dados
   - Criação automática de tabelas SQLite
   - conexão e fechamento seguro do banco

3. Diário Digital
   - Interface para escrita de entradas
   - Registro automático de data/hora
   - Armazenamento persistente de texto
   - Associação com usuário logado
   - Visualização de entradas anteriores
   - Histórico ordenado por data (mais recente primeiro)
   - Exibição de data/hora de cada entrada

4. Sistema de Reflexões
   - Perguntas pré-definidas para reflexão
   - Coleta de respostas do usuário
   - Armazenamento de perguntas e respostas
   - Registro de data das reflexões

5. Termômetro Emocional
   - Registro de estado emocional
   - Escala de intensidade (1-10)
   - Histórico completo de emoções
   - Visualização ordenada por data

6. Tela de Emergência
   - Exibição de contatos de apoio
   - Números de telefone de emergência
   - Acesso rápido em situações críticas

7. Interface de Usuário
   - Menu principal intuitivo
   - Navegação por opções numeradas
   - Mensagens de feedback ao usuário
   - Tratamento de opções inválidas

#Menu Principal do Sistema

Após fazer login, o usuário tem acesso a 7 opções no menu principal:

1. Escrever no diário
- Digite seus pensamentos e experiências do dia
- Registro automático de data/hora
- Texto salvo no banco de dados pessoal

2. Modo reflexão
- Responda 3 perguntas reflexivas pré-definidas:
  - "O que te fez mais alegre hoje?"
  - "Você enfrentou algo difícil hoje? Como lidou?"
  - "Algo que gostaria de lembrar?"
- Respostas salvas para consulta futura

3. Registrar emoção
- Descreva como está se sentindo no momento
- Avalie a intensidade de 1 a 10
- Registro com timestamp automático

4. Ver histórico de emoções
- Visualize todas as emoções registradas
- Lista ordenada por data (mais recente primeiro)
- Acompanhe padrões e evolução emocional

5. Ver diário
- FUNCIONALIDADE: Visualize todas as entradas do diário
- Entradas exibidas em ordem cronológica (mais recente primeiro)
- Mostra data/hora de cada entrada
- Histórico completo preservado

6. Tela de emergência
- Acesso rápido a contatos de apoio emocional:
  - CVV - 188 (24h, gratuito)
  - SAMU - 192
  - Emergência Policial - 190

7. Sair
- Encerra o programa com segurança
- Fecha conexões com banco de dados

Lista de Bibliotecas Utilizadas
 
Bibliotecas e Módulos
1. `sqlite3`
   - Função:Gerenciamento de banco de dados SQLite
   - Uso no projeto:
     - Criação e conexão com banco de dados
     - Execução de comandos SQL (CREATE, INSERT, SELECT)
     - Gerenciamento de transações
     - Fechamento seguro de conexões

2. `datetime`
   - Função: Manipulação de datas e horários
   - Uso no projeto:
     - Registro automático de timestamps
     - Formatação de datas (YYYY-MM-DD HH:MM)
     - Ordenação cronológica de registros


