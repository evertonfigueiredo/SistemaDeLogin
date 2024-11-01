import tkinter as tk
from tkinter import ttk, messagebox
from tinydb import TinyDB, Query

# Configuração do banco de dados
db = TinyDB("estoque.json")
Produto = Query()

# Banco de dados para categorias
db_categorias = TinyDB("categorias.json")

# Lista para armazenar os produtos e categorias (carregando do banco)
estoque = db.all()
categorias = [cat["nome"] for cat in db_categorias.all()]

# Funções para gerenciar categorias
def abrir_tela_categorias():
    def atualizar_tabela_categorias():
        for item in tabela_categorias.get_children():
            tabela_categorias.delete(item)
        for cat in db_categorias.all():
            tabela_categorias.insert("", "end", values=(cat.doc_id, cat["nome"]))

    def adicionar_categoria():
        nome_categoria = entry_nome_categoria.get()
        if nome_categoria:
            db_categorias.insert({"nome": nome_categoria})
            categorias.append(nome_categoria)
            atualizar_combo_categorias()
            atualizar_tabela_categorias()
            entry_nome_categoria.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Categoria adicionada com sucesso!")
        else:
            messagebox.showerror("Erro", "O nome da categoria não pode estar vazio.")

    def preencher_campos_categoria(event):
        item_selecionado = tabela_categorias.selection()
        if item_selecionado:
            indice = tabela_categorias.index(item_selecionado)
            categoria = db_categorias.all()[indice]
            entry_nome_categoria.delete(0, tk.END)
            entry_nome_categoria.insert(0, categoria["nome"])

    def alterar_categoria():
        item_selecionado = tabela_categorias.selection()
        if item_selecionado:
            indice = tabela_categorias.index(item_selecionado)
            doc_id = db_categorias.all()[indice].doc_id
            nome_categoria = entry_nome_categoria.get()
            if nome_categoria:
                db_categorias.update({"nome": nome_categoria}, doc_ids=[doc_id])
                categorias[indice] = nome_categoria
                atualizar_combo_categorias()
                atualizar_tabela_categorias()
                entry_nome_categoria.delete(0, tk.END)
                messagebox.showinfo("Sucesso", "Categoria alterada com sucesso!")
            else:
                messagebox.showerror("Erro", "O nome da categoria não pode estar vazio.")
        else:
            messagebox.showerror("Erro", "Selecione uma categoria para alterar.")

    def excluir_categoria():
        item_selecionado = tabela_categorias.selection()
        if item_selecionado:
            indice = tabela_categorias.index(item_selecionado)
            doc_id = db_categorias.all()[indice].doc_id
            db_categorias.remove(doc_ids=[doc_id])
            categorias.pop(indice)
            atualizar_combo_categorias()
            atualizar_tabela_categorias()
            entry_nome_categoria.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Categoria excluída com sucesso!")
        else:
            messagebox.showerror("Erro", "Selecione uma categoria para excluir.")

    # Janela para cadastro de categorias
    janela_categorias = tk.Toplevel(root)
    janela_categorias.title("Gerenciar Categorias")

    tk.Label(janela_categorias, text="Nome da Categoria:").pack(padx=10, pady=5)
    entry_nome_categoria = tk.Entry(janela_categorias)
    entry_nome_categoria.pack(padx=10, pady=5)

    # Botões de ação para categorias
    tk.Button(janela_categorias, text="Adicionar Categoria", command=adicionar_categoria).pack(pady=5)
    tk.Button(janela_categorias, text="Alterar Categoria", command=alterar_categoria).pack(pady=5)
    tk.Button(janela_categorias, text="Excluir Categoria", command=excluir_categoria).pack(pady=5)

    # Tabela (Treeview) para exibir as categorias
    colunas_categorias = ("ID", "Nome")
    tabela_categorias = ttk.Treeview(janela_categorias, columns=colunas_categorias, show="headings")
    tabela_categorias.heading("ID", text="ID")
    tabela_categorias.heading("Nome", text="Nome")
    tabela_categorias.pack(padx=10, pady=10, fill="both", expand=True)

    # Evento para preencher os campos ao clicar na linha da tabela de categorias
    tabela_categorias.bind("<<TreeviewSelect>>", preencher_campos_categoria)

    # Carregar categorias na tabela ao abrir a janela
    atualizar_tabela_categorias()

# Funções para atualizar a lista de categorias no Combobox
def atualizar_combo_categorias():
    combo_categoria['values'] = categorias

# Funções CRUD para produtos
def adicionar_produto():
    nome = entry_nome.get()
    categoria = combo_categoria.get()
    try:
        qtd = int(entry_qtd.get())
        preco = float(entry_preco.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e preço devem ser números válidos.")
        return

    if nome and categoria:
        produto = {"nome": nome, "categoria": categoria, "qtd": qtd, "preco": preco}
        estoque.append(produto)
        db.insert(produto)
        atualizar_tabela()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
    else:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

def atualizar_tabela():
    for item in tabela.get_children():
        tabela.delete(item)
    for produto in estoque:
        tabela.insert("", "end", values=(produto['nome'], produto['categoria'], produto['qtd'], f"R${produto['preco']:.2f}"))

def limpar_campos():
    entry_nome.delete(0, tk.END)
    combo_categoria.set("")
    entry_qtd.delete(0, tk.END)
    entry_preco.delete(0, tk.END)

def preencher_campos(event):
    item_selecionado = tabela.selection()
    if item_selecionado:
        indice = tabela.index(item_selecionado)
        produto = estoque[indice]
        entry_nome.delete(0, tk.END)
        combo_categoria.set(produto["categoria"])
        entry_qtd.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_nome.insert(0, produto["nome"])
        entry_qtd.insert(0, produto["qtd"])
        entry_preco.insert(0, produto["preco"])

def alterar_produto():
    item_selecionado = tabela.selection()
    if item_selecionado:
        indice = tabela.index(item_selecionado)
        try:
            nome = entry_nome.get()
            categoria = combo_categoria.get()
            qtd = int(entry_qtd.get())
            preco = float(entry_preco.get())
            if nome and categoria:
                estoque[indice] = {"nome": nome, "categoria": categoria, "qtd": qtd, "preco": preco}
                db.update(estoque[indice], doc_ids=[indice + 1])
                atualizar_tabela()
                limpar_campos()
                messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e preço devem ser números válidos.")
    else:
        messagebox.showerror("Erro", "Selecione um produto para alterar.")

def excluir_produto():
    item_selecionado = tabela.selection()
    if item_selecionado:
        indice = tabela.index(item_selecionado)
        db.remove(doc_ids=[indice + 1])
        del estoque[indice]
        atualizar_tabela()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
    else:
        messagebox.showerror("Erro", "Selecione um produto para excluir.")

# Interface gráfica
root = tk.Tk()
root.title("Gerenciamento de Estoque")

# Labels e campos de entrada
tk.Label(root, text="Nome do Produto:").grid(row=0, column=0, padx=10, pady=5)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Categoria:").grid(row=1, column=0, padx=10, pady=5)
combo_categoria = ttk.Combobox(root, values=categorias, state='readonly')
combo_categoria.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Quantidade:").grid(row=2, column=0, padx=10, pady=5)
entry_qtd = tk.Entry(root)
entry_qtd.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Preço:").grid(row=3, column=0, padx=10, pady=5)
entry_preco = tk.Entry(root)
entry_preco.grid(row=3, column=1, padx=10, pady=5)

# Botões para produtos
tk.Button(root, text="Adicionar", command=adicionar_produto).grid(row=4, column=0, padx=10, pady=5)
tk.Button(root, text="Alterar", command=alterar_produto).grid(row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Excluir", command=excluir_produto).grid(row=4, column=2, padx=10, pady=5)
tk.Button(root, text="Limpar Campos", command=limpar_campos).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Gerenciar Categorias", command=abrir_tela_categorias).grid(row=5, column=2, pady=10)

# Tabela (Treeview) para exibir os produtos
colunas = ("Nome", "Categoria", "Qtd", "Preço")
tabela = ttk.Treeview(root, columns=colunas, show="headings")
tabela.heading("Nome", text="Nome")
tabela.heading("Categoria", text="Categoria")
tabela.heading("Qtd", text="Qtd")
tabela.heading("Preço", text="Preço")
tabela.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Configurar a seleção de itens na tabela
tabela.bind("<<TreeviewSelect>>", preencher_campos)

# Ajustar a proporção da tabela
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)

# Inicializar a tabela de produtos
atualizar_tabela()

# Iniciar o loop da interface gráfica
root.mainloop()