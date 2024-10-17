import streamlit as st
import requests

# URL base do seu backend (substitua pela URL do seu serviço em produção)
base_url = "https://aps-3-flask-rest-mongo-0tomz-1.onrender.com"

# Funções para interação com o backend

# Funções de Usuários
def get_usuarios():
    response = requests.get(f"{base_url}/usuarios")
    return response.json()

def get_usuario_by_id(id_usuario):
    response = requests.get(f"{base_url}/usuarios/{id_usuario}")
    return response.json()

def create_usuario(cpf, nome, data_de_aniversario):
    usuario = {"cpf": cpf, "nome": nome, "data_de_aniversario": data_de_aniversario}
    response = requests.post(f"{base_url}/usuarios", json=usuario)
    return response.json()

def update_usuario(id_usuario, cpf, nome, data_de_aniversario):
    usuario = {"cpf": cpf, "nome": nome, "data_de_aniversario": data_de_aniversario}
    response = requests.put(f"{base_url}/usuarios/{id_usuario}", json=usuario)
    return response.json()

def delete_usuario(id_usuario):
    response = requests.delete(f"{base_url}/usuarios/{id_usuario}")
    return response.json()

# Funções de Bicicletas
def get_bikes():
    response = requests.get(f"{base_url}/bikes")
    return response.json()

def create_bike(marca, modelo, cidade, status):
    bike = {"marca": marca, "modelo": modelo, "cidade": cidade, "status": status}
    response = requests.post(f"{base_url}/bikes", json=bike)
    return response.json()

def update_bike(id_bike, marca, modelo, cidade, status):
    bike = {"marca": marca, "modelo": modelo, "cidade": cidade, "status": status}
    response = requests.put(f"{base_url}/bikes/{id_bike}", json=bike)
    return response.json()

def delete_bike(id_bike):
    response = requests.delete(f"{base_url}/bikes/{id_bike}")
    return response.json()

# Funções de Empréstimos
def get_emprestimos():
    response = requests.get(f"{base_url}/emprestimos")
    return response.json()

def create_emprestimo(id_usuario, id_bike, data):
    emprestimo = {"id_usuario": id_usuario, "id_bike": id_bike, "data": data}
    response = requests.post(f"{base_url}/emprestimos", json=emprestimo)
    return response.json()

def delete_emprestimo(id_emprestimo):
    response = requests.delete(f"{base_url}/emprestimos/{id_emprestimo}")
    return response.json()


# Interface de Usuários
def usuarios_page():
    st.title("Gerenciamento de Usuários")
    
    opcoes = ["Visualizar Usuários", "Adicionar Usuário", "Atualizar Usuário", "Deletar Usuário"]
    escolha = st.selectbox("Escolha uma opção", opcoes)
    
    if escolha == "Visualizar Usuários":
        usuarios = get_usuarios()
        st.write(usuarios)

    elif escolha == "Adicionar Usuário":
        cpf = st.text_input("CPF")
        nome = st.text_input("Nome")
        data_de_aniversario = st.text_input("Data de Nascimento")
        if st.button("Adicionar"):
            resultado = create_usuario(cpf, nome, data_de_aniversario)
            st.write(resultado)

    elif escolha == "Atualizar Usuário":
        id_usuario = st.text_input("ID do Usuário")
        cpf = st.text_input("Novo CPF")
        nome = st.text_input("Novo Nome")
        data_de_aniversario = st.text_input("Nova Data de Nascimento")
        if st.button("Atualizar"):
            resultado = update_usuario(id_usuario, cpf, nome, data_de_aniversario)
            st.write(resultado)

    elif escolha == "Deletar Usuário":
        id_usuario = st.text_input("ID do Usuário")
        if st.button("Deletar"):
            resultado = delete_usuario(id_usuario)
            st.write(resultado)


# Interface de Bicicletas
def bikes_page():
    st.title("Gerenciamento de Bicicletas")
    
    opcoes = ["Visualizar Bicicletas", "Adicionar Bicicleta", "Atualizar Bicicleta", "Deletar Bicicleta"]
    escolha = st.selectbox("Escolha uma opção", opcoes)
    
    if escolha == "Visualizar Bicicletas":
        bikes = get_bikes()
        st.write(bikes)

    elif escolha == "Adicionar Bicicleta":
        marca = st.text_input("Marca")
        modelo = st.text_input("Modelo")
        cidade = st.text_input("Cidade")
        status = st.selectbox("Status", ["disponivel", "em uso"])
        if st.button("Adicionar"):
            resultado = create_bike(marca, modelo, cidade, status)
            st.write(resultado)

    elif escolha == "Atualizar Bicicleta":
        id_bike = st.text_input("ID da Bicicleta")
        marca = st.text_input("Nova Marca")
        modelo = st.text_input("Novo Modelo")
        cidade = st.text_input("Nova Cidade")
        status = st.selectbox("Novo Status", ["disponivel", "em uso"])
        if st.button("Atualizar"):
            resultado = update_bike(id_bike, marca, modelo, cidade, status)
            st.write(resultado)

    elif escolha == "Deletar Bicicleta":
        id_bike = st.text_input("ID da Bicicleta")
        if st.button("Deletar"):
            resultado = delete_bike(id_bike)
            st.write(resultado)


# Interface de Empréstimos
def emprestimos_page():
    st.title("Gerenciamento de Empréstimos")
    
    opcoes = ["Visualizar Empréstimos", "Criar Empréstimo", "Deletar Empréstimo"]
    escolha = st.selectbox("Escolha uma opção", opcoes)
    
    if escolha == "Visualizar Empréstimos":
        emprestimos = get_emprestimos()
        st.write(emprestimos)

    elif escolha == "Criar Empréstimo":
        id_usuario = st.text_input("ID do Usuário")
        id_bike = st.text_input("ID da Bicicleta")
        data = st.text_input("Data do Empréstimo")
        if st.button("Criar"):
            resultado = create_emprestimo(id_usuario, id_bike, data)
            st.write(resultado)

    elif escolha == "Deletar Empréstimo":
        id_emprestimo = st.text_input("ID do Empréstimo")
        if st.button("Deletar"):
            resultado = delete_emprestimo(id_emprestimo)
            st.write(resultado)


# Menu Principal
def main():
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Ir para", ["Usuários", "Bicicletas", "Empréstimos"])
    
    if page == "Usuários":
        usuarios_page()
    elif page == "Bicicletas":
        bikes_page()
    elif page == "Empréstimos":
        emprestimos_page()


if __name__ == "__main__":
    main()
