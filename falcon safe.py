#Copyright (c) 2026 Claude Païssé
#Programa experimental de entrada de ronda para Daniel da Falcon
# Passo a passo do projeto
    # Passo 1: Criar a tela do sistema
    # Passo 2: Criar o formulário de cadastro de visitas
    # Passo 3: Salvar a a visita na base de dados
    # Passo 4: Mostrar a base de dados na tela
    # Passo 5: Criar o dpipashboard com os gráficos

#requerimentos
# carregar comandos do MAC
import os
# carregar comandos do Streamlit para deploy
import streamlit as st
# carregar comandos do Pandas para manipulação de dados
import pandas as pd
# carregar comandos do Plotly para gráficos
import plotly.express as px
# carregar a localidade brasileira para ordenação correta de strings
import locale
# configurar o jogo de caracteres para português do Brasil
locale.setlocale(locale.LC_COLLATE, "pt_BR.UTF-8")

#Passo 1: montar a tela do sistema
st.write("## Sistema de Visitas de supervisão da Falcon")
st.markdown(
    '<h4 style="margin-left: 40px;">by Claude Païssé</p>',
    unsafe_allow_html=True
)
# Passo 2: Criar o formulário de cadastro e, se aruivo não existir, criar um arquivo csv com as colunas
arquivo = "visitas.csv"
colunas = ["Data",
           "Hora",
           "Supervisor",
           "Condominio",
           "Funcionario",
           "Observacoes",
           "Limpeza",
           "LimpezaProduto",
           "LimpezaCronograma",
           "LimpezaCondominio",
           "LimpezaPortaria",
           "Uniforme",
           "FolhaPonto",
           "Cracha",
           "Pendencias",
           "UniformeCondicoes",
           "BarbaFeita"
]
if os.path.exists(arquivo):
    tabela = pd.read_csv(arquivo)
    print("Arquivo existente carregado.")
else:
    tabela = pd.DataFrame(columns=colunas)
    tabela.to_csv(arquivo, index=False)
    print("Arquivo criado com uma tabela vazia.")
print(tabela)

# incialzar atributos e carregar banco de dados
from datetime import datetime
agora = datetime.now()

valores_iniciais = {
    "data": agora.date(),   
    "hora": agora.time().replace(second=0, microsecond=0),
    "supervisor": "Selecione o supervisor",
    "condo": "Selecione o condomínio",
    "funcionario": "Selecione o funcionário",
    "obs": None,
    "limpeza": False,
    "limpezaproduto": False,
    "limpezacronograma": False,
    "limpezacondominio": False,
    "limpezaportaria": False,
    "uniforme": False,
    "folhaponto": False,
    "cracha": False,
    "pendencias": False,
    "uniformecondicoes": False,
    "barbafeita": False,
}

for chave, valor in valores_iniciais.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor
tabela = pd.read_csv("visitas.csv")

#perimitir entrada das informações do formulário de cadastro de visitas na barra lateral
#colunas: Data,Hora,Supervisor,Condomninio,Funcionario,Observacoes,LimpezaProduto,LimpezaCronograma,LimpezaCondominio(ronda),LimpezaPortaria,Uniforme,FolhaPonto,Cracha,Pendencias,UniformeCondicoes,BarbaFeita

st.sidebar.write("## Cadastrar visita")
data = st.sidebar.date_input("Data", key="Data")
hora = st.sidebar.time_input("Hora", key="Hora")

    #selecionar o supervisor, de dentro de uma lista orednada alfabeticamente, com a primeira opção sendo "Selecione o supervisor"
with open("Supervisores.txt", "r", encoding="utf-8") as arquivo:    
    supervisores = [linha.strip() for linha in arquivo if linha.strip()]
    supervisores = sorted(supervisores, key=str.casefold)
    supervisor = st.sidebar.selectbox("Supervisor *", ["Selecione o supervisor"] + supervisores, key="supervisor")

    #selecionar o condomínio, de dentro de uma lista ordenada alfabeticamente, com a primeira opção sendo "Selecione o condomínio"
with open("Condominios.txt", "r", encoding="utf-8") as arquivo:
    condominios = [linha.strip() for linha in arquivo if linha.strip()]
    condominios = sorted(condominios, key=str.casefold)
    condo = st.sidebar.selectbox("Condomínio *", ["Selecione o condomínio"] + condominios, key="condo")
    #selecionar o funcionário, de dentro de uma lista ordenada alfabeticamente, com a primeira opção sendo "Selecione o funcionário"

with open("Funcionarios.txt", "r", encoding="utf-8") as arquivo:
    funcionarios = [linha.strip() for linha in arquivo if linha.strip()]
    funcionarios = sorted(funcionarios, key=str.casefold)
    funcionario = st.sidebar.selectbox("Funcionário *", ["Selecione o funcionário"] + funcionarios, key="funcionario")

obs = st.sidebar.text_area("Observações", key="Observações")

limpeza = st.sidebar.checkbox("Limpeza realizada?", key="Limpeza")
limpezaproduto = st.sidebar.checkbox("Produtos de limpeza verificados?", key="LimpezaProdutos")
limpezacronograma = st.sidebar.checkbox("Cronograma de limpeza verificado?", key="LimpezaCronograma")
limpezacondominio = st.sidebar.checkbox("Ronda de limpeza do condomínio realizada?", key="LimpezaCondomínio")
limpezaportaria = st.sidebar.checkbox("Limpeza da portaria realizada?", key="LimpezaPortaria")
uniforme = st.sidebar.checkbox("Uniforme do funcionário em ordem?", key="Uniforme")
folhaponto = st.sidebar.checkbox("Folha de ponto assinada?", key="FolhaPonto")
cracha = st.sidebar.checkbox("Crachá do funcionário em ordem?", key="Cracha")
pendencias = st.sidebar.checkbox("Pendências para próxima visita?", key="Pendencias")
uniformecondicoes = st.sidebar.checkbox("Uniforme do funcionário em boas condições?", key="UniformeCondições")
barbafeita = st.sidebar.checkbox("Barba do funcionário feita?", key="BarbaFeita")

# Passo 3: Salvar a visita na base de dados, criando uma função, que será chamada quando o botão for clicado

def cadastrar_visita():

    # 1. Verificar os campos obrigatórios
    campos_faltando = []

    if st.session_state.supervisor == "Selecione o supervisor":
        campos_faltando.append("supervisor")

    if st.session_state.condo == "Selecione o condomínio":
        campos_faltando.append("condo")

    if st.session_state.funcionario == "Selecione o funcionário":
        campos_faltando.append("funcionario")

    # 2. Se faltar algum campo, não cadastrar
    if campos_faltando:
        st.session_state.erro_cadastro = (
            "Preencha os campos obrigatórios: "
            + ", ".join(campos_faltando)
            + "."
        )
        return

    # 3. Se tudo estiver preenchido, limpar a mensagem de erro
    st.session_state.erro_cadastro = ""

    # 4. Carregar a tabela atual
    tabela = pd.read_csv("visitas.csv")

    # 5. Preparar os dados da nova visita
    nova_visita = [
        st.session_state.data,
        st.session_state.hora,
        st.session_state.supervisor,
        st.session_state.condo,
        st.session_state.funcionario,
        st.session_state.obs,
        "Sim" if st.session_state.limpeza else "Não",
        "Sim" if st.session_state.limpezaproduto else "Não",
        "Sim" if st.session_state.limpezacronograma else "Não",
        "Sim" if st.session_state.limpezacondominio else "Não",
        "Sim" if st.session_state.limpezaportaria else "Não",
        "Sim" if st.session_state.uniforme else "Não",
        "Sim" if st.session_state.folhaponto else "Não",
        "Sim" if st.session_state.cracha else "Não",
        "Sim" if st.session_state.pendencias else "Não",
        "Sim" if st.session_state.uniformecondicoes else "Não",
        "Sim" if st.session_state.barbafeita else "Não"
    ]

#colunas: Data,Hora,Supervisor,Condomninio,Funcionario,Observacoes,LimpezaProduto,LimpezaCronograma,LimpezaCondominio(ronda),LimpezaPortaria,Uniforme,FolhaPonto,Cracha,Pendencias,UniformeCondicoes,BarbaFeita
    # 6. Adicionar a visita e gravar o CSV
    
    #DIAGOSTICO DO MISMATCH
    print("Colunas da tabela:", list(tabela.columns))
    print("Quantidade de colunas:", len(tabela.columns))

    print("Nova visita:", nova_visita)
    print("Quantidade de valores:", len(nova_visita))
    
    print("\n--- DIAGNÓSTICO DO MISMATCH ---")

    print("Colunas da tabela:", tabela.columns.tolist())
    print("Número de colunas:", len(tabela.columns))

    print("Nova visita:", nova_visita)
    print("Tipo de nova_visita:", type(nova_visita))
    print("Número de valores:", len(nova_visita))

    print("--- FIM DO DIAGNÓSTICO ---")

    
    
    tabela.loc[len(tabela)] = nova_visita
    tabela.to_csv("visitas.csv", index=False)

    # 7. Confirmar o cadastro
    st.toast("Visita cadastrada!", icon="✅")

    # 8. Limpar os campos para a próxima visita
    st.session_state.supervisor = "Selecione o supervisor"
    st.session_state.condo = "Selecione o condomínio"
    st.session_state.funcionario = "Selecione o funcionário"
    st.session_state.observacoes = ""
    st.session_state.limpeza = False
    st.session_state.limpezaproduto = False
    st.session_state.limpezacronograma = False
    st.session_state.limpezacondominio = False
    st.session_state.limpezaportaria = False
    st.session_state.uniforme = False
    st.session_state.folhaponto = False
    st.session_state.cracha = False
    st.session_state.pendencias = False
    st.session_state.uniformecondicoes = False
    st.session_state.barbafeita = False

botao = st.sidebar.button(
    "Cadastrar visita",
    on_click=cadastrar_visita
)

if st.session_state.get("erro_cadastro"):
    st.sidebar.error(st.session_state.erro_cadastro)
# Passo 4: Mostrar a base de dados na tela
st.write("## Visitas cadastradas")
st.dataframe(tabela)

# Passo 5: Criar o dashboard publicando os gráficos de pizza
st.write("## Dashboard")

grafico2 = px.pie(tabela, 
                  names="Supervisor",
                  title="Distribuição de visitas por supervisor"
                  )
st.plotly_chart(grafico2)
grafico3 = px.pie(tabela, 
                  names="Condominio", 
                  title="Distribuição de visitas por condomínio"
                  )
st.plotly_chart(grafico3)