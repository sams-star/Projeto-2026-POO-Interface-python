import json
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

# --- CONFIGURAÇÕES GLOBAIS ---
WIDTH = 360
HEIGHT = 600
ARQUIVO_USUARIOS = "usuarios.json"
IMAGEM_LOGO = "maisninquem.jpg"

# --- PALETA DE CORES ---
COR_BG_PRINCIPAL = "#121212"
COR_BG_INPUT = "#1e1e1e"
COR_TEXTO = "white"
COR_BOTAO = "#740707"
COR_BOTAO_HOVER = "#ce0606"


class GerenciadorAutenticacao:
    """Responsável por carregar, validar e registrar usuários no JSON."""
    
    @staticmethod
    def carregar_dados():
        if not os.path.exists(ARQUIVO_USUARIOS):
            return {}
        try:
            with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def salvar_dados(dados):
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    @classmethod
    def validar_ou_cadastrar(cls, usuario, senha):
        dados_usuarios = cls.carregar_dados()

        if usuario in dados_usuarios:
            if dados_usuarios[usuario]["senha"] == senha:
                return "login_sucesso"
            return "senha_incorreta"
        
        # Cria novo usuário se não existir
        dados_usuarios[usuario] = {"senha": senha, "musicas": []}
        cls.salvar_dados(dados_usuarios)
        return "cadastro_sucesso"


class InterfaceLogin:
    """Responsável por construir e gerenciar a janela de Login do SpotTI."""
    
    def __init__(self, root):
        self.root = root
        self.configurar_janela()
        self.criar_widgets()

    def configurar_janela(self):
        self.root.title("SpotTI - Login")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=COR_BG_PRINCIPAL)

    def carregar_imagem_circular(self, caminho_imagem, tamanho):
        try:
            img = Image.open(caminho_imagem).convert("RGBA")
            img = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
            
            mascara = Image.new('L', (tamanho, tamanho), 0)
            desenho = ImageDraw.Draw(mascara)
            desenho.ellipse((0, 0, tamanho, tamanho), fill=255)
            
            imagem_circular = Image.new('RGBA', (tamanho, tamanho))
            imagem_circular.paste(img, (0, 0), mask=mascara)
            
            return ImageTk.PhotoImage(imagem_circular)
        
        except Exception as e:

            print(f"Erro ao carregar a imagem {caminho_imagem}: {e}")
            return ImageTk.PhotoImage(Image.new('RGBA', (tamanho, tamanho)))

    def criar_widgets(self):

        # Logo Circular
        self.logo_image = self.carregar_imagem_circular(IMAGEM_LOGO, tamanho=150)
        label_logo = tk.Label(self.root, image=self.logo_image, bg=COR_BG_PRINCIPAL, bd=0)
        label_logo.pack(pady=(50, 10))

        # Título
        tk.Label(
            self.root, 
            text="Login",
            font=("Arial", 20, "bold"), 
            bg=COR_BG_PRINCIPAL, 
            fg=COR_TEXTO
        ).pack(pady=(0, 20))

        # Campo Usuário
        tk.Label(
            self.root, 
            text="Nome de Usuário", 
            font=("Arial", 11), 
            bg=COR_BG_PRINCIPAL, 
            fg=COR_TEXTO).pack(anchor="w", padx=45, pady=(10, 2))
        
        self.entry_usuario = tk.Entry(
            self.root, 
            bg=COR_BG_INPUT, 
            fg=COR_TEXTO, 
            bd=0, 
            font=("Arial", 12), 
            insertbackground=COR_TEXTO)
        
        self.entry_usuario.pack(fill="x", padx=45, ipady=8)

        # Campo Senha
        tk.Label(
            self.root, 
            text="Senha", 
            font=("Arial", 11), 
            bg=COR_BG_PRINCIPAL, fg=COR_TEXTO).pack(anchor="w", padx=45, pady=(20, 2))
        
        self.entry_senha = tk.Entry(
            self.root, 
            
            bg=COR_BG_INPUT, 
            fg=COR_TEXTO, 
            bd=0, 
            font=("Arial", 12), 
            show="*", 
            insertbackground=COR_TEXTO)
        self.entry_senha.pack(fill="x", padx=45, ipady=8)

        # Botão Conectar
        btn_entrar = tk.Button(
            self.root, text="Conectar",
            command=self.executar_login,
            bg=COR_BOTAO, fg=COR_TEXTO, 
            font=("Arial", 12, "bold"), 
            bd=0, activebackground=COR_BOTAO_HOVER, 
            activeforeground=COR_TEXTO
        )
        btn_entrar.pack(fill="x", padx=45, pady=40, ipady=10)

    def executar_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not usuario or not senha:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos!")
            return

        resultado = GerenciadorAutenticacao.validar_ou_cadastrar(usuario, senha)

        if resultado == "senha_incorreta":
            messagebox.showerror("Erro", "Senha incorreta!")
            return
            
        if resultado == "login_sucesso":
            messagebox.showinfo("Sucesso", f"Bem-vindo de volta, {usuario}!")
        elif resultado == "cadastro_sucesso":
            messagebox.showinfo("Sucesso", f"Conta criada!\nBem-vindo, {usuario}!")

        # Inicializa o próximo script e fecha a tela atual
        subprocess.Popen(["python", "main.py", usuario])
        self.root.destroy()


# --- EXECUÇÃO DO PROGRAMA ---
if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = InterfaceLogin(janela_principal)
    janela_principal.mainloop()
