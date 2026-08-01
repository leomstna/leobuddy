import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import os
import random

class Mascote:
    def __init__(self, root, config, callback_abrir_config, callback_checkup, callback_sair, callback_diagnostico):
        self.root = root
        self.config = config
        self.callback_abrir_config = callback_abrir_config
        self.callback_checkup = callback_checkup
        self.callback_sair = callback_sair
        self.callback_diagnostico = callback_diagnostico
        
        self.dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dir_img = os.path.join(self.dir_base, "imagens")
        
        self.imagens = {}
        self.carregar_imagens()
        
        self.root.overrideredirect(True)
        self.chroma_key = "#0a0a0a"
        self.root.wm_attributes("-transparentcolor", self.chroma_key)
        self.root.attributes("-topmost", self.config.get("sempre_no_topo"))
        self.root.attributes("-alpha", float(self.config.get("opacidade")))
        self.root.configure(bg=self.chroma_key)
        
        # Mudanca para Canvas para permitir ancoragem manual
        escala = self.config.get("escala_imagem")
        self.root.geometry(f"{escala}x{escala}")
        
        self.canvas = tk.Canvas(root, bg=self.chroma_key, highlightthickness=0, width=escala, height=escala)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self._evento_atual = None
        self.flip_dance = False
        self._timer_print = None
        self.idle_timer = 0
        
        self.canvas.bind("<Button-1>", self.clique_esquerdo)
        self.canvas.bind("<B1-Motion>", self.arrastar)
        self.canvas.bind("<Button-3>", self.abrir_menu)
        
        self.set_imagem_por_evento("standart")
        self.animar()

    def carregar_imagens(self):
        tamanho = self.config.get("escala_imagem")
        mapping = self.config.get("image_mapping")
        arquivos_ociosos = ["MÃO NO BOLSO", "MÃO NO BOLSO 2", "BRAÇOS CRUZADO", "SENTADO", "SENTADO NO SOFA"]
        arquivos_pra_carregar = list(mapping.values()) + arquivos_ociosos
        
        for nome_arq in set(arquivos_pra_carregar):
            caminho = os.path.join(self.dir_img, f"{nome_arq}.png")
            if os.path.exists(caminho):
                try:
                    img = Image.open(caminho).convert("RGBA")
                    img.thumbnail((tamanho, tamanho), Image.Resampling.LANCZOS)
                    self.imagens[nome_arq] = ImageTk.PhotoImage(img)
                    
                    if nome_arq == mapping.get("ouvindo_spotify", "DANÇANDO"):
                        self.imagens[f"{nome_arq}_FLIP"] = ImageTk.PhotoImage(ImageOps.mirror(img))
                except Exception as e:
                    print(f"Erro carregando {nome_arq}: {e}")

    def limpar_cache_imagens(self):
        self.imagens.clear()
        escala = self.config.get("escala_imagem")
        self.root.geometry(f"{escala}x{escala}")
        self.canvas.configure(width=escala, height=escala)
        self.root.attributes("-alpha", float(self.config.get("opacidade")))
        
        self.carregar_imagens()
        if self._evento_atual:
            evento_temp = self._evento_atual
            self._evento_atual = None
            self.disparar_evento(evento_temp)
        else:
            self.set_imagem_por_evento("standart")

    def set_imagem_por_evento(self, evento, flip=False):
        mapping = self.config.get("image_mapping")
        nome_arq = mapping.get(evento, mapping.get("standart", "STANDART"))
        
        chave = f"{nome_arq}_FLIP" if flip and f"{nome_arq}_FLIP" in self.imagens else nome_arq
        
        img_para_mostrar = None
        if chave in self.imagens:
            img_para_mostrar = self.imagens[chave]
        elif mapping.get("standart", "STANDART") in self.imagens:
            img_para_mostrar = self.imagens[mapping.get("standart", "STANDART")]
            nome_arq = mapping.get("standart", "STANDART")
            
        if img_para_mostrar:
            escala = self.config.get("escala_imagem")
            offsets = self.config.get("image_offsets").get(nome_arq, {"x": 0, "y": 0})
            cx = (escala // 2) + int(offsets.get("x", 0))
            cy = (escala // 2) + int(offsets.get("y", 0))
            
            self.canvas.delete("mascote")
            self.canvas.create_image(cx, cy, image=img_para_mostrar, anchor=tk.CENTER, tags="mascote")

    def disparar_evento(self, evento):
        self.idle_timer = 0
        if self._evento_atual == evento:
            return
            
        if self._evento_atual == "print_screen" and evento != "print_screen":
            return

        if evento == "print_screen":
            self.set_imagem_por_evento("print_screen")
            self._evento_atual = "print_screen"
            if self._timer_print:
                try: self.root.after_cancel(self._timer_print)
                except: pass
            
            tempo_reacao_ms = int(float(self.config.get("intervalo_verificacao_segundos")) * 1000)
            if tempo_reacao_ms < 500: tempo_reacao_ms = 500 # Minimo pro print
            self._timer_print = self.root.after(tempo_reacao_ms, self.resetar_print_screen)
            return

        self._evento_atual = evento
        self.set_imagem_por_evento(evento)

    def resetar_print_screen(self):
        self._evento_atual = None
        self._timer_print = None
        self.set_imagem_por_evento("standart")
            
    def voltar_ao_normal(self):
        if self._evento_atual == "print_screen": return
        if self._evento_atual is None: return 
        self._evento_atual = None
        self.set_imagem_por_evento("standart")

    def animar(self):
        if self._evento_atual == "ouvindo_spotify":
            self.flip_dance = not self.flip_dance
            self.set_imagem_por_evento("ouvindo_spotify", self.flip_dance)
            velocidade = int(self.config.get("dance_speed_ms"))
            self.root.after(velocidade, self.animar)
        else:
            if self._evento_atual is None and self.config.get("poses_aleatorias"):
                self.idle_timer += 1
                if self.idle_timer > 8:
                    self.idle_timer = 0
                    if random.random() > 0.4:
                        poses = ["MÃO NO BOLSO", "MÃO NO BOLSO 2", "BRAÇOS CRUZADO", self.config.get("image_mapping").get("standart", "STANDART")]
                        pose = random.choice(poses)
                        if pose in self.imagens:
                            escala = self.config.get("escala_imagem")
                            offsets = self.config.get("image_offsets").get(pose, {"x": 0, "y": 0})
                            cx = (escala // 2) + int(offsets.get("x", 0))
                            cy = (escala // 2) + int(offsets.get("y", 0))
                            self.canvas.delete("mascote")
                            self.canvas.create_image(cx, cy, image=self.imagens[pose], anchor=tk.CENTER, tags="mascote")
            elif not self.config.get("poses_aleatorias") and self._evento_atual is None:
                pass
            self.root.after(1000, self.animar)

    def clique_esquerdo(self, event):
        self.x = event.x; self.y = event.y

    def arrastar(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def abrir_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0, bg="#2b2b2b", fg="white", activebackground="#404040")
        menu.add_command(label="🔧 Configurações", command=self.callback_abrir_config)
        menu.add_command(label="🛠️ Refazer Check-up", command=self.callback_checkup)
        menu.add_command(label="📊 Diagnóstico", command=self.callback_diagnostico)
        menu.add_separator()
        menu.add_command(label="❌ Sair", command=self.callback_sair)
        menu.post(event.x_root, event.y_root)
