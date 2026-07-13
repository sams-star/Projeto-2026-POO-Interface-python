import json
import os
import sys
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

WIDTH = 360
HEIGHT = 500
ARQUIVO_USUARIOS = "usuarios.json"
IMAGEM_LOGO = "logo.jpg"


COR_BG_PRINCIPAL = "#121212"
COR_BG_INPUT = "#1e1e1e"
COR_TEXTO = "white"
COR_MUTED = "#aaaaaa"
COR_BOTAO = "#740707"
COR_BOTAO_HOVER = "#ce0606"


class GerenciadorPerfil:
    """Responsável por carregar os dados específicos do usuário ativo do JSON."""
    
    @staticmethod
    def buscar_senha_usuario(usuario):

        if not os.path.exists(ARQUIVO_USUARIOS):
            return "Não encontrado"
        try:
            with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
                dados_usuarios = json.load(arquivo)

                if usuario in dados_usuarios:
                    return dados_usuarios[usuario].get("senha", "Sem senha")
                
                return "Usuário não cadastrado"
            
        except (json.JSONDecodeError, Exception):
            return "Erro ao ler dados"


class InterfacePerfil:
    def __init__(self, root, usuario_logado):

        self.root = root
        self.usuario = usuario_logado
        self.senha = GerenciadorPerfil.buscar_senha_usuario(self.usuario)
        
        self.configurar_janela()
        self.criar_widgets()

    def configurar_janela(self):
        
        self.root.title("SpotTI - Perfil")
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

       
        self.avatar_image = self.carregar_imagem_circular(IMAGEM_LOGO, tamanho=120)

        label_avatar = tk.Label(
            self.root, 
            image=self.avatar_image, 
            bg=COR_BG_PRINCIPAL, bd=0)
        label_avatar.pack(pady=(40, 10))

       
        tk.Label(
            self.root, 
            text="Seu Perfil",
            font=("Arial", 18, "bold"), 
            bg=COR_BG_PRINCIPAL, 
            fg=COR_TEXTO
        ).pack(pady=(0, 25))

        
        frame_dados = tk.Frame(self.root, bg=COR_BG_PRINCIPAL)
        frame_dados.pack(fill="x", padx=45)

        
        tk.Label(
            frame_dados, 
            text="Nome de Usuário", 
            font=("Arial", 10), 
            bg=COR_BG_PRINCIPAL, 
            fg=COR_MUTED).pack(anchor="w")
        
        label_user_box = tk.Label(
            frame_dados, text=self.usuario, font=("Arial", 12, "bold"), 
            bg=COR_BG_INPUT, fg=COR_TEXTO, anchor="w", padx=10
        )
        label_user_box.pack(fill="x", ipady=8, pady=(4, 15))

        
        tk.Label(
            frame_dados, text="Senha da Conta", 
            font=("Arial", 10), 
            bg=COR_BG_PRINCIPAL, 
            fg=COR_MUTED).pack(anchor="w")
        
        self.label_senha_box = tk.Label(
            frame_dados, text=self.senha, font=("Arial", 12), 
            bg=COR_BG_INPUT, fg=COR_TEXTO, anchor="w", padx=10
        )
        self.label_senha_box.pack(fill="x", ipady=8, pady=(4, 30))

       
        btn_voltar = tk.Button(
            self.root, text="Fechar aba do Perfil",
            command=self.root.destroy,
            bg=COR_BOTAO, fg=COR_TEXTO, 
            font=("Arial", 12, "bold"), 
            bd=0, activebackground=COR_BOTAO_HOVER, 
            activeforeground=COR_TEXTO,
            cursor="hand2"
        )
        btn_voltar.pack(fill="x", padx=45, ipady=10)


if __name__ == "__main__":
    usuario_ativo = sys.argv[1] if len(sys.argv) > 1 else "eu tentei"
    
    janela_perfil = tk.Tk()
    app = InterfacePerfil(janela_perfil, usuario_ativo)
    janela_perfil.mainloop()
