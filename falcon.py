#Copyright (c) 2026 Claude Païssé
#Programa experimental de entrada de ronda para Daniel da Falcon
# Passo a passo do projeto
    # Passo 1: Criar a tela do sistema
    # Passo 2: Criar o formulário de cadastro de visitas
    # Passo 3: Salvar a a visita na base de dados
    # Passo 4: Mostrar a base de dados na tela
    # Passo 5: Criar o dashboard com os gráficos
    # Incluir controle de acesso para que apenas supervisores possam cadastrar visitas

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
try:
    locale.setlocale(locale.LC_COLLATE, "pt_BR.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_COLLATE, "C")

from datetime import datetime
from zoneinfo import ZoneInfo

agora = datetime.now(ZoneInfo("America/Sao_Paulo"))


st.write(
    "Teste horário de São Paulo:",
    datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")
)




#Passo 1: montar a tela do sistema
st.write("## Sistema de Visitas de supervisão da Falcon")
st.markdown(
    '<h4 style="margin-left: 40px;">by Claude Païssé  © 2026',
    unsafe_allow_html=True
)
# Passo 2: Criar o formulário de cadastro e, se aruivo não existe, criar um arquivo csv com as colunas
arquivo = "visitas.csv"
colunas = ["Data",
           "Hora",
           "Supervisor",
           "Condominio",
           "Colaborador1",
           "Funcao1",
           "Colaborador2",
           "Funcao2",
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
from zoneinfo import ZoneInfo
agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

valores_iniciais = {
    "Data": agora.date(),   
    "Hora": agora.time().replace(second=0, microsecond=0),
    "supervisor": "Selecione o supervisor",
    "condo": "Selecione o condomínio",
    "colaborador1": "Selecione o colaborador",
    "funcao1": "Selecione a função",
    "colaborador2": "Selecione o colaborador",
    "funcao2": "Selecione a função",
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

#permitir entrada das informações do formulário de cadastro de visitas na barra lateral
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

#selecionar o colaborador, de dentro de uma lista ordenada alfabeticamente, com a primeira opção sendo "Selecione o funcionário"
with open("Colaboradores.txt", "r", encoding="utf-8") as arquivo:
    colaboradores = [linha.strip() for linha in arquivo if linha.strip()]
    colaboradores = sorted(colaboradores, key=str.casefold)
    colaborador1 = st.sidebar.selectbox("Colaborador 1 *", ["Selecione o colaborador"] + colaboradores, key="colaborador1")
with open("Funcoes.txt", "r", encoding="utf-8") as arquivo:
    funcoes = [linha.strip() for linha in arquivo if linha.strip()]
    funcoes = sorted(funcoes, key=str.casefold)
    funcao1 = st.sidebar.selectbox("Função colaborador 1 *", ["Selecione a função"] + funcoes, key="funcao1")

with open("Colaboradores.txt", "r", encoding="utf-8") as arquivo:
    colaboradores = [linha.strip() for linha in arquivo if linha.strip()]
    colaboradores = sorted(colaboradores, key=str.casefold)
    colaborador2 = st.sidebar.selectbox("Colaborador 2 *", ["Selecione o colaborador"] + colaboradores, key="colaborador2")
with open("Funcoes.txt", "r", encoding="utf-8") as arquivo:
    funcoes = [linha.strip() for linha in arquivo if linha.strip()]
    funcoes = sorted(funcoes, key=str.casefold)
    funcao2 = st.sidebar.selectbox("Função colaborador 2 *", ["Selecione a função"] + funcoes, key="funcao2")

obs = st.sidebar.text_area("Observações", key="obs")

limpeza = st.sidebar.radio("Limpeza realizada?", ["Não", "Sim"], horizontal=True, key="limpeza")
limpezaproduto = st.sidebar.radio("Produtos de limpeza verificados?", ["Não", "Sim"], horizontal=True, key="limpezaproduto")
limpezacronograma = st.sidebar.radio("Cronograma de limpeza verificado?", ["Não", "Sim"], horizontal=True, key="limpezacronograma")
limpezacondominio = st.sidebar.radio("Ronda de limpeza do condomínio realizada?", ["Não", "Sim"], horizontal=True, key="limpezacondominio")
limpezaportaria = st.sidebar.radio("Limpeza da portaria realizada?", ["Não", "Sim"], horizontal=True        , key="limpezaportaria")
uniforme = st.sidebar.radio("Uniforme do funcionário em ordem?", ["Não", "Sim"], horizontal=True, key="uniforme")
folhaponto = st.sidebar.radio("Folha de ponto assinada?", ["Não", "Sim"], horizontal=True, key="folhaponto")
cracha = st.sidebar.radio("Crachá do funcionário em ordem?", ["Não", "Sim"], horizontal=True, key="cracha")
pendencias = st.sidebar.radio("Pendências para próxima visita?", ["Não", "Sim"], horizontal=True, key="pendencias")
uniformecondicoes = st.sidebar.radio("Uniforme do funcionário em boas condições?", ["Não", "Sim"], horizontal=True, key="uniformecondicoes")
barbafeita = st.sidebar.radio("Barba do funcionário feita?", ["Não", "Sim"], horizontal=True, key="barbafeita")

# Passo 3: Salvar a visita na base de dados, criando uma função, que será chamada quando o botão for clicado

def cadastrar_visita():

# 1. Verificar os campos obrigatórios
    campos_faltando = []

    if st.session_state.supervisor == "Selecione o supervisor":
        campos_faltando.append("supervisor")

    if st.session_state.condo == "Selecione o condomínio":
        campos_faltando.append("condo")

    if st.session_state.colaborador1 == "Selecione o colaborador":
        campos_faltando.append("colaborador1")

    if st.session_state.funcao1 == "Selecione a função":
        campos_faltando.append("funcao1")

    if st.session_state.colaborador2 == "Selecione o colaborador":
        campos_faltando.append("colaborador2")

    if st.session_state.funcao2 == "Selecione a função":
        campos_faltando.append("funcao2")

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
        st.session_state["Data"],
        st.session_state["Hora"].strftime("%H:%M"),
        st.session_state.supervisor,
        st.session_state.condo,
        st.session_state.colaborador1,
        st.session_state.funcao1,       
        st.session_state.colaborador2,
        st.session_state.funcao2,
        st.session_state.obs,
        st.session_state.limpeza,
        st.session_state.limpezaproduto,
        st.session_state.limpezacronograma,
        st.session_state.limpezacondominio,
        st.session_state.limpezaportaria,
        st.session_state.uniforme,
        st.session_state.folhaponto,
        st.session_state.cracha,
        st.session_state.pendencias,
        st.session_state.uniformecondicoes,
        st.session_state.barbafeita
    ]

# 6. Adicionar a visita e gravar o CSV
    
    #INÍCIO DO DIAGNÓSTICO DO MISMATCH - A APAGAR NA VERSÃO FINAL
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
    #FIM DO DIAGOSTICO DO MISMATCH - A APAGAR NA VERSÃO FINAL

    tabela.loc[len(tabela)] = nova_visita
    tabela.to_csv("visitas.csv", index=False)

    # 7. Confirmar o cadastro
    st.toast("Visita cadastrada!", icon="😇")

    # 8. Limpar os campos para a próxima visita
    st.session_state.supervisor = "Selecione o supervisor"
    st.session_state.condo = "Selecione o condomínio"
    st.session_state.colaborador1 = "Selecione o colaborador"
    st.session_state.funcao1 = "Selecione a função"
    st.session_state.colaborador2 = "Selecione o colaborador"
    st.session_state.funcao2 = "Selecione a função"
    st.session_state.obs = ""
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
grafico4 = px.pie(tabela, 
                  names="Limpeza", 
                  title="Distribuição de limpezas"
                  )
st.plotly_chart(grafico4)
grafico5 = px.pie(tabela, 
                  names="FolhaPonto", 
                  title="Distribuição de folhas de ponto assinadas"
                  )
st.plotly_chart(grafico5)
grafico6 = px.pie(tabela, 
                  names="Cracha", 
                  title="Distribuição de crachás em ordem"
                  )
st.plotly_chart(grafico6)