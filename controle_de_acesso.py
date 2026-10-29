# Sistema de Login Simples com Python e TXT





print("executou")


def menu():
    """Exibe o menu principal e retorna a opção escolhida."""
    st.write("\n" + "="*20)
    st.write("   SISTEMA DE ACESSO")
    st.write("="*20)
    st.write("1. Cadastrar novo usuário")
    st.write("2. Fazer Login")
    st.write("3. Sair")
    return input("Escolha uma opção: ")

def cadastrar():
    """Registra um novo usuário no arquivo usuarios.txt."""
    usuario = input("Digite o novo nome de usuário: ").strip()
    senha = input("Digite a nova senha: ").strip()

    if not usuario or not senha:
        st.write("Erro: Usuário e senha não podem estar vazios.")
        return

    # O modo 'a' adiciona ao final do arquivo sem sobrescrever
    with open("usuarios.txt", "a") as arquivo:
        arquivo.write(f"{usuario},{senha}\n")
    
    st.write(f"Usuário '{usuario}' cadastrado com sucesso!")

def login():
    """Valida as credenciais comparando com o arquivo usuarios.txt."""
    usuario_input = input("Usuário: ").strip()
    senha_input = input("Senha: ").strip()
    
    encontrado = False

    try:
        with open("usuarios.txt", "r") as arquivo:
            for linha in arquivo:
                # Divide a linha pela vírgula e remove espaços/quebras de linha
                partes = linha.strip().split(",")
                if len(partes) == 2:
                    usuario_salvo, senha_salva = partes
                    if usuario_input == usuario_salvo and senha_input == senha_salva:
                        encontrado = True
                        break
    except FileNotFoundError:
        st.write("Aviso: Nenhum banco de dados de usuários encontrado. Cadastre um usuário primeiro.")
        return

    if encontrado:
        st.write(f"Sucesso: Bem-vindo ao sistema, {usuario_input}!")
    else:
        st.write("Erro: Usuário ou senha incorretos.")

def iniciar():
    """Controla o fluxo principal do programa."""
    while True:
        opcao = menu()
        
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            login()
        elif opcao == "3":
            st.write("Encerrando o programa. Até logo!")
            break
        else:
            st.write("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    iniciar()
