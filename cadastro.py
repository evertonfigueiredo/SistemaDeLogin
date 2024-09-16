import tkinter as tk
from tkinter import messagebox  # Importando messagebox explicitamente
from tinydb import TinyDB
import subprocess

# Configurar o banco de dados
db = TinyDB('db.json')

def cadastrar():
    username = entry_username.get()
    password = entry_password.get()
    
    if username and password:
        # Inserir o novo usuário no banco de dados
        db.insert({'username': username, 'password': password})
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        root.destroy()  # Fecha a janela de cadastro
        subprocess.run(['python3', 'login.py'])  # Abre a tela de login
    else:
        messagebox.showerror("Erro", "Preencha todos os campos.")

# Configurar a janela de cadastro
root = tk.Tk()
root.title("Cadastro")
root.geometry("300x200")

# Label e input para usuário
tk.Label(root, text="Usuário:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Label e input para senha
tk.Label(root, text="Senha:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Botão para realizar o cadastro
btn_cadastrar = tk.Button(root, text="Cadastrar", command=cadastrar)
btn_cadastrar.pack(pady=10)

# Executar a aplicação
root.mainloop()
