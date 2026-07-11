import tkinter as tk
from tkinter import messagebox
import subprocess
import json
import os

WIDTH = 360
HEIGHT = 600

def realizar_cadastro():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()

    if not usuario or not senha:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos!")
        return

    nome_arquivo = "usuarios.json"
    dados_usuarios = {}

    if os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
                dados_usuarios = json.load(arquivo)
        except json.JSONDecodeError:
            dados_usuarios = {}

    # Lógica de decisão adaptada para a nova estrutura
    if usuario in dados_usuarios:
        # A senha agora fica dentro do campo ["senha"]
        if dados_usuarios[usuario]["senha"] == senha:
            messagebox.showinfo("Sucesso", f"Bem-vindo de volta, {usuario}!")
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
            return
    else:
        # Cria o novo usuário com a estrutura: senha + lista de músicas vazia
        dados_usuarios[usuario] = {
            "senha": senha,
            "musicas": []
        }
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados_usuarios, arquivo, indent=4, ensure_ascii=False)
        
        messagebox.showinfo("Sucesso", f"Conta criada!\nBem-vindo, {usuario}!")

    # IMPORTANTE: Passa o nome do usuário logado como argumento para a biblioteca principal
    subprocess.Popen(["python", "main.py", usuario])
    root.destroy()


root = tk.Tk()
root.title("SpotTI - Cadastro")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)


tk.Label(
    root, 
    text="Criar Conta",  
    font=("Arial", 20, "bold")
).pack(pady=40)


tk.Label(root, text="Nome de Usuário", font=("Arial", 11)).pack(anchor="w", padx=45, pady=(10, 2))

entry_usuario = tk.Entry(root, bg="#1e1e1e", fg="white", bd=0, font=("Arial", 12), insertbackground="white")
entry_usuario.pack(fill="x", padx=45, ipady=8)


tk.Label(root, text="Senha", font=("Arial", 11)).pack(anchor="w", padx=45, pady=(20, 2))

entry_senha = tk.Entry(root, bg="#1e1e1e", fg="white", bd=0, font=("Arial", 12), show="*", insertbackground="white")
entry_senha.pack(fill="x", padx=45, ipady=8)


btn_cadastrar = tk.Button(
    root,
    text="Cadastrar",
    command=realizar_cadastro,
    bg="#1db954", 
    fg="white",
    font=("Arial", 12, "bold"),
    bd=0,
    activebackground="#1aa34a",
    activeforeground="white"
)
btn_cadastrar.pack(fill="x", padx=45, pady=40, ipady=10)

root.mainloop()