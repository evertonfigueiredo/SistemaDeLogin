import tkinter as tk
from tkinter import messagebox
from tinydb import TinyDB, Query
import subprocess
from dashboard import open_dashboard  # Importar a função do arquivo dashboard

# Configurar o banco de dados
db = TinyDB('db.json')
User = Query()

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Verificar se o usuário e a senha estão corretos
    user = db.search((User.username == username) & (User.password == password))
    if user:
        messagebox.showinfo("Login", "Login bem-sucedido!")
        root.destroy()  # Fecha a janela de login
        open_dashboard(username)  # Chama a função do dashboard
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def open_cadastro():
    root.destroy()  # Fecha a janela de login
    subprocess.run(['python3', 'cadastro.py'])  # Abre a tela de cadastro

# Configurar a janela de login
root = tk.Tk()
root.title("Login")
root.geometry("300x200")

# Label e input para usuário
tk.Label(root, text="Usuário:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Label e input para senha
tk.Label(root, text="Senha:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Botão de login
btn_login = tk.Button(root, text="Entrar", command=login)
btn_login.pack(pady=10)

# Botão para ir para a tela de cadastro
btn_cadastro = tk.Button(root, text="Cadastre-se", command=open_cadastro)
btn_cadastro.pack(pady=5)

# Executar a aplicação
root.mainloop()
