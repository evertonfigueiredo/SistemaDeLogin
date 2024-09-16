import tkinter as tk
from tinydb import TinyDB, Query

# Conectar ao banco de dados
db = TinyDB('db.json')
Task = Query()

def open_dashboard(username):
    """Função para abrir o dashboard com a lista de tarefas do usuário"""
    dashboard = tk.Tk()
    dashboard.title(f"Dashboard - {username}")
    dashboard.geometry("400x400")

    # Função para atualizar a exibição das tarefas
    def update_tasks():
        for widget in task_frame.winfo_children():
            widget.destroy()

        # Buscar as tarefas do usuário no banco de dados
        tasks = db.search(Task.username == username)

        # Exibir cada tarefa com um botão para excluí-la
        for task in tasks:
            # Verifique se a chave 'task' existe
            if 'task' in task:
                task_frame_single = tk.Frame(task_frame)
                task_frame_single.pack(fill='x', pady=2)

                task_label = tk.Label(task_frame_single, text=task['task'], anchor='w')
                task_label.pack(side='left', padx=5, expand=True)

                delete_button = tk.Button(task_frame_single, text="Excluir", command=lambda t=task: delete_task(t.doc_id))
                delete_button.pack(side='right', padx=5)

    # Função para adicionar uma nova tarefa
    def add_task():
        task_text = task_entry.get()
        if task_text:
            db.insert({'username': username, 'task': task_text})  # Inserir a nova tarefa para o usuário
            task_entry.delete(0, tk.END)
            update_tasks()

    # Função para excluir uma tarefa
    def delete_task(task_id):
        db.remove(doc_ids=[task_id])
        update_tasks()

    # Exibir uma mensagem de boas-vindas
    tk.Label(dashboard, text=f"Bem-vindo, {username}!", font=("Arial", 16)).pack(pady=10)

    # Input para adicionar novas tarefas
    tk.Label(dashboard, text="Adicionar nova tarefa:").pack(pady=5)
    task_entry = tk.Entry(dashboard, width=30)
    task_entry.pack(pady=5)

    add_button = tk.Button(dashboard, text="Adicionar Tarefa", command=add_task)
    add_button.pack(pady=10)

    # Frame para exibir as tarefas
    task_frame = tk.Frame(dashboard)
    task_frame.pack(pady=10, fill='both', expand=True)

    # Atualizar a exibição ao iniciar
    update_tasks()

    dashboard.mainloop()
