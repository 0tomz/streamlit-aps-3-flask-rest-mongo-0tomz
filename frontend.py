import streamlit as st
import pandas as pd
import requests

# Base URL da API do backend (Flask)
BASE_URL = "http://127.0.0.1:5000"

# Função genérica para fazer requisições ao backend
def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    url = f"{BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url, params=params)
        else:
            st.error("Método HTTP não suportado.")
            return None

        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        elif response.status_code == 404:
            st.warning("⚠ Recurso não encontrado.")
        elif response.status_code == 500:
            st.error("⚠ Erro interno do servidor.")
        else:
            st.error(f"⚠ Erro: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"⚠ Erro de conexão: {e}")
        return None

# Título da aplicação
st.title("Sistema de Gerenciamento de Aluguel de Bicicletas")

# Escolha entre gerenciar usuários ou bicicletas
categoria = st.sidebar.selectbox(
    "Escolha uma categoria",
    ["Usuários", "Bicicletas"]
)

# Escolha da ação
acao = st.sidebar.selectbox(
    "Selecione a ação",
    ["Listar", "Criar", "Atualizar", "Deletar"]
)

# Função para listar todos os itens de uma categoria
def listar_itens(endpoint, chave):
    st.subheader(f"Listar {chave}")
    itens = fazer_requisicao(endpoint)
    if itens:
        df_itens = pd.DataFrame(itens[chave])
        st.dataframe(df_itens)

# Função para deletar um item pelo ID
def deletar_item(endpoint, id):
    st.subheader(f"Deletar {endpoint[:-1].capitalize()} por ID")
    if st.button("Deletar"):
        resposta = fazer_requisicao(f"{endpoint}/{id}", method="DELETE")
        if resposta:
            st.success(f"{endpoint[:-1].capitalize()} deletado com sucesso!")

# Função para atualizar um item
def atualizar_item(endpoint, id, campos):
    st.subheader(f"Atualizar {endpoint[:-1].capitalize()} por ID")
    with st.form(key=f"atualizar_{endpoint[:-1]}"):
        data = {}
        for campo in campos:
            data[campo] = st.text_input(f"{campo.capitalize()}", key=f"{campo}_update")
        submit = st.form_submit_button("Atualizar")
        if submit:
            resposta = fazer_requisicao(f"{endpoint}/{id}", method="PUT", data=data)
            if resposta:
                st.success(f"{endpoint[:-1].capitalize()} atualizado com sucesso!")

# Seção de usuários
if categoria == "Usuários":
    st.header("Gestão de Usuários")

    # Ação de listar usuários
    if acao == "Listar":
        listar_itens("usuarios", "usuarios")

    # Ação de criar novo usuário
    elif acao == "Criar":
        with st.form(key="cadastrar_usuario"):
            st.subheader("Cadastrar Novo Usuário")
            nome = st.text_input("Nome")
            cpf = st.text_input("CPF")
            data_nasc = st.text_input("Data de Nascimento (dd/mm/yyyy)")
            submit = st.form_submit_button("Cadastrar Usuário")

            if submit:
                if nome and cpf and data_nasc:
                    usuario_data = {
                        "nome": nome,
                        "cpf": cpf,
                        "data_de_aniversario": data_nasc
                    }
                    resposta = fazer_requisicao("usuarios", method="POST", data=usuario_data)
                    if resposta:
                        st.success("Usuário cadastrado com sucesso!")
                else:
                    st.error("Por favor, preencha todos os campos.")

    # Ação de atualizar usuário
    elif acao == "Atualizar":
        usuario_id_update = st.text_input("ID do Usuário para atualizar")
        if usuario_id_update:
            atualizar_item("usuarios", usuario_id_update, ["cpf", "nome", "data_de_aniversario"])

    # Ação de deletar usuário
    elif acao == "Deletar":
        usuario_id_del = st.text_input("ID do Usuário para deletar")
        if usuario_id_del:
            deletar_item("usuarios", usuario_id_del)

# Seção de bicicletas
elif categoria == "Bicicletas":
    st.header("Gestão de Bicicletas")

    # Ação de listar bicicletas
    if acao == "Listar":
        listar_itens("bikes", "bikes")

    # Ação de criar nova bicicleta
    elif acao == "Criar":
        with st.form(key="cadastrar_bike"):
            st.subheader("Cadastrar Nova Bicicleta")
            marca = st.text_input("Marca")
            modelo = st.text_input("Modelo")
            cidade = st.text_input("Cidade")
            status = st.selectbox("Status", ["disponivel", "em uso"])
            submit_bike = st.form_submit_button("Cadastrar Bicicleta")

            if submit_bike:
                if marca and modelo and cidade and status:
                    bike_data = {
                        "marca": marca,
                        "modelo": modelo,
                        "cidade": cidade,
                        "status": status
                    }
                    resposta = fazer_requisicao("bikes", method="POST", data=bike_data)
                    if resposta:
                        st.success("Bicicleta cadastrada com sucesso!")
                else:
                    st.error("Por favor, preencha todos os campos.")

    # Ação de atualizar bicicleta
    elif acao == "Atualizar":
        bike_id_update = st.text_input("ID da Bicicleta para atualizar")
        if bike_id_update:
            atualizar_item("bikes", bike_id_update, ["marca", "modelo", "cidade", "status"])

    # Ação de deletar bicicleta
    elif acao == "Deletar":
        bike_id_del = st.text_input("ID da Bicicleta para deletar")
        if bike_id_del:
            deletar_item("bikes", bike_id_del)

# Rodapé
st.sidebar.info("Sistema de Gerenciamento de Aluguel de Bicicletas - Desenvolvido em Flask e MongoDB")
