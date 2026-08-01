import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

class JanelaConfiguracoes:
    def __init__(self, root, config, callback_ao_salvar):
        self.top = tk.Toplevel(root)
        self.top.title("Configurações do Mascote")
        self.top.geometry("450x550")
        self.top.configure(bg="#1e1e1e")
        self.top.attributes("-topmost", True)
        self.config = config
        self.callback = callback_ao_salvar
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("TCheckbutton", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("TButton", background="#3a3a3a", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#505050")])
        style.configure("TEntry", fieldbackground="#2b2b2b", foreground="#ffffff", borderwidth=1)
        style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2b2b2b", foreground="#ffffff", font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", "#4da6ff")])

        tk.Label(self.top, text="⚙️ Painel de Controle", font=("Segoe UI", 14, "bold"), bg="#1e1e1e", fg="#4da6ff").pack(anchor="w", padx=20, pady=(15, 5))

        notebook = ttk.Notebook(self.top)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # ABA BÁSICO
        tab_basico = tk.Frame(notebook, bg="#1e1e1e")
        notebook.add(tab_basico, text="  Básico  ")
        
        f_tempo = tk.Frame(tab_basico, bg="#1e1e1e")
        f_tempo.pack(fill=tk.X, pady=5, padx=5)
        ttk.Label(f_tempo, text="Alerta de tempo de uso (min):").pack(side=tk.LEFT)
        self.var_tempo = tk.IntVar(value=self.config.get("tempo_alerta_uso_minutos"))
        ttk.Entry(f_tempo, textvariable=self.var_tempo, width=8, justify="center").pack(side=tk.RIGHT)

        f_escala = tk.Frame(tab_basico, bg="#1e1e1e")
        f_escala.pack(fill=tk.X, pady=5, padx=5)
        ttk.Label(f_escala, text="Tamanho do Mascote (px):").pack(side=tk.LEFT)
        self.var_escala = tk.IntVar(value=self.config.get("escala_imagem"))
        ttk.Entry(f_escala, textvariable=self.var_escala, width=8, justify="center").pack(side=tk.RIGHT)
        
        f_reacao = tk.Frame(tab_basico, bg="#1e1e1e")
        f_reacao.pack(fill=tk.X, pady=5, padx=5)
        ttk.Label(f_reacao, text="Tempo de reação (segundos):").pack(side=tk.LEFT)
        self.var_reacao = tk.DoubleVar(value=self.config.get("intervalo_verificacao_segundos"))
        ttk.Entry(f_reacao, textvariable=self.var_reacao, width=8, justify="center").pack(side=tk.RIGHT)

        ttk.Separator(tab_basico, orient='horizontal').pack(fill=tk.X, pady=10)

        self.var_poses = tk.BooleanVar(value=self.config.get("poses_aleatorias"))
        ttk.Checkbutton(tab_basico, text="🎭 Fazer poses aleatórias parado", variable=self.var_poses).pack(anchor="w", pady=2, padx=5)

        self.var_topo = tk.BooleanVar(value=self.config.get("sempre_no_topo"))
        ttk.Checkbutton(tab_basico, text="📌 Manter sempre no topo", variable=self.var_topo).pack(anchor="w", pady=2, padx=5)
        
        self.var_spotify = tk.BooleanVar(value=self.config.get("detectar_spotify"))
        ttk.Checkbutton(tab_basico, text="🎵 Animar com Spotify", variable=self.var_spotify).pack(anchor="w", pady=2, padx=5)
        
        self.var_stream = tk.BooleanVar(value=self.config.get("detectar_streaming"))
        ttk.Checkbutton(tab_basico, text="🍿 Detectar Netflix/YouTube", variable=self.var_stream).pack(anchor="w", pady=2, padx=5)
        
        self.var_cam = tk.BooleanVar(value=self.config.get("detectar_webcam"))
        ttk.Checkbutton(tab_basico, text="📷 Detectar Webcam ligada", variable=self.var_cam).pack(anchor="w", pady=2, padx=5)
        
        self.var_print = tk.BooleanVar(value=self.config.get("detectar_print_screen"))
        ttk.Checkbutton(tab_basico, text="📸 Reagir a Print Screen", variable=self.var_print).pack(anchor="w", pady=2, padx=5)

        # ABA AVANÇADO
        tab_avancado = tk.Frame(notebook, bg="#1e1e1e")
        notebook.add(tab_avancado, text="  Avançado  ")
        
        f_dance = tk.Frame(tab_avancado, bg="#1e1e1e")
        f_dance.pack(fill=tk.X, pady=5, padx=5)
        ttk.Label(f_dance, text="Velocidade da dança (ms):").pack(side=tk.LEFT)
        self.var_dance = tk.IntVar(value=self.config.get("dance_speed_ms"))
        ttk.Entry(f_dance, textvariable=self.var_dance, width=8, justify="center").pack(side=tk.RIGHT)
        
        f_opa = tk.Frame(tab_avancado, bg="#1e1e1e")
        f_opa.pack(fill=tk.X, pady=5, padx=5)
        ttk.Label(f_opa, text="Opacidade (0.1 a 1.0):").pack(side=tk.LEFT)
        self.var_opa = tk.DoubleVar(value=self.config.get("opacidade"))
        ttk.Entry(f_opa, textvariable=self.var_opa, width=8, justify="center").pack(side=tk.RIGHT)

        ttk.Separator(tab_avancado, orient='horizontal').pack(fill=tk.X, pady=15)
        
        ttk.Button(tab_avancado, text="🔗 Alterar Imagens das Reações", command=self.abrir_mapeamento).pack(fill=tk.X, pady=5, padx=5)
        ttk.Label(tab_avancado, text="Escolha qual .png carregar para cada ação.", font=("Segoe UI", 8), foreground="#aaaaaa").pack(pady=(0, 10))
        
        ttk.Button(tab_avancado, text="🎯 Ajustar Centro/Âncora Visual", command=self.abrir_ancoragem).pack(fill=tk.X, pady=5, padx=5)
        ttk.Label(tab_avancado, text="Ajuste visualmente onde a imagem fica ancorada.", font=("Segoe UI", 8), foreground="#aaaaaa").pack(pady=(0, 10))

        # BOTAO SALVAR
        btn_frame = tk.Frame(self.top, bg="#1e1e1e")
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        ttk.Button(btn_frame, text="SALVAR TUDO", command=self.salvar).pack(side=tk.RIGHT, ipadx=10, ipady=3)

    def abrir_mapeamento(self):
        win = tk.Toplevel(self.top)
        win.title("Mapeamento de Reações")
        win.geometry("350x500")
        win.configure(bg="#1e1e1e")
        win.attributes("-topmost", True)
        
        canvas = tk.Canvas(win, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        mapping = self.config.get("image_mapping")
        self.map_vars = {}
        for chave, valor in mapping.items():
            f = tk.Frame(scrollable_frame, bg="#1e1e1e")
            f.pack(fill=tk.X, pady=2, padx=10)
            ttk.Label(f, text=f"{chave}:").pack(side=tk.LEFT)
            var = tk.StringVar(value=valor)
            ttk.Entry(f, textvariable=var, width=15).pack(side=tk.RIGHT)
            self.map_vars[chave] = var
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def salvar_map():
            novo_map = {k: v.get() for k, v in self.map_vars.items()}
            self.config.set("image_mapping", novo_map)
            win.destroy()
            messagebox.showinfo("Mapeamento", "Salvo! Não esqueça de clicar no 'Salvar Tudo' principal depois.", parent=self.top)
            
        ttk.Button(win, text="Confirmar", command=salvar_map).pack(pady=10)

    def abrir_ancoragem(self):
        win = tk.Toplevel(self.top)
        win.title("Ajuste Visual de Âncora")
        win.geometry("500x650")
        win.configure(bg="#1e1e1e")
        win.attributes("-topmost", True)
        
        ttk.Label(win, text="Selecione a Imagem:").pack(pady=(15, 5))
        mapping = self.config.get("image_mapping")
        todas_imagens = list(set(mapping.values()))
        
        arquivos_ociosos = ["MÃO NO BOLSO", "MÃO NO BOLSO 2", "BRAÇOS CRUZADO", "SENTADO", "SENTADO NO SOFA"]
        for o in arquivos_ociosos:
            if o not in todas_imagens: todas_imagens.append(o)
            
        combo = ttk.Combobox(win, values=todas_imagens, state="readonly", width=30)
        if todas_imagens: combo.current(0)
        combo.pack(pady=5)
        
        ttk.Label(win, text="🖱️ Arraste a imagem no quadrado para centralizar", font=("Segoe UI", 9, "italic"), foreground="#aaaaaa").pack(pady=5)
        
        escala = self.config.get("escala_imagem")
        
        # Canvas preview
        frame_canvas = tk.Frame(win, bg="#333333", bd=2, relief="sunken")
        frame_canvas.pack(pady=10)
        
        preview_canvas = tk.Canvas(frame_canvas, width=escala, height=escala, bg="#0a0a0a", highlightthickness=0)
        preview_canvas.pack()
        
        cx, cy = escala // 2, escala // 2
        
        # Desenha grid e cruz
        preview_canvas.create_line(cx, 0, cx, escala, fill="#4da6ff", dash=(4, 4))
        preview_canvas.create_line(0, cy, escala, cy, fill="#4da6ff", dash=(4, 4))
        preview_canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill="red", outline="white")
        
        f_coords = tk.Frame(win, bg="#1e1e1e")
        f_coords.pack(pady=5)
        
        f_x = tk.Frame(f_coords, bg="#1e1e1e")
        f_x.pack(side=tk.LEFT, padx=10)
        ttk.Label(f_x, text="Eixo X:").pack(side=tk.LEFT)
        var_x = tk.IntVar(value=0)
        tk.Spinbox(f_x, from_=-200, to=200, textvariable=var_x, width=5, bg="#2b2b2b", fg="white").pack(side=tk.RIGHT)
        
        f_y = tk.Frame(f_coords, bg="#1e1e1e")
        f_y.pack(side=tk.LEFT, padx=10)
        ttk.Label(f_y, text="Eixo Y:").pack(side=tk.LEFT)
        var_y = tk.IntVar(value=0)
        tk.Spinbox(f_y, from_=-200, to=200, textvariable=var_y, width=5, bg="#2b2b2b", fg="white").pack(side=tk.RIGHT)
        
        offsets = self.config.get("image_offsets")
        self._img_preview = None
        
        def atualizar_canvas(*args):
            img_sel = combo.get()
            preview_canvas.delete("img_oc")
            
            dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho = os.path.join(dir_base, "imagens", f"{img_sel}.png")
            
            if os.path.exists(caminho):
                try:
                    img = Image.open(caminho).convert("RGBA")
                    img.thumbnail((escala, escala), Image.Resampling.LANCZOS)
                    self._img_preview = ImageTk.PhotoImage(img)
                    
                    pos_x = cx + var_x.get()
                    pos_y = cy + var_y.get()
                    
                    preview_canvas.create_image(pos_x, pos_y, image=self._img_preview, anchor=tk.CENTER, tags="img_oc")
                    preview_canvas.tag_lower("img_oc") # Abaixo da mira
                except: pass
                
        def carregar_offset(event):
            img_sel = combo.get()
            off = offsets.get(img_sel, {"x": 0, "y": 0})
            var_x.set(off.get("x", 0))
            var_y.set(off.get("y", 0))
            atualizar_canvas()
            
        combo.bind("<<ComboboxSelected>>", carregar_offset)
        
        def on_var_change(*args):
            try:
                # valida se é numero
                var_x.get(); var_y.get()
                atualizar_canvas()
            except: pass
            
        var_x.trace_add("write", on_var_change)
        var_y.trace_add("write", on_var_change)
        
        # Logica de drag
        def on_press(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y
            self._start_var_x = var_x.get()
            self._start_var_y = var_y.get()
            
        def on_drag(event):
            dx = event.x - self._drag_start_x
            dy = event.y - self._drag_start_y
            var_x.set(self._start_var_x + dx)
            var_y.set(self._start_var_y + dy)
            
        preview_canvas.bind("<Button-1>", on_press)
        preview_canvas.bind("<B1-Motion>", on_drag)
        
        carregar_offset(None)
        
        def salvar_ancora():
            img_sel = combo.get()
            offsets[img_sel] = {"x": var_x.get(), "y": var_y.get()}
            self.config.set("image_offsets", offsets)
            messagebox.showinfo("Âncora", f"Offsets de '{img_sel}' salvos!", parent=win)
            
        ttk.Button(win, text="Salvar Atual", command=salvar_ancora).pack(pady=15)

    def salvar(self):
        self.config.set("tempo_alerta_uso_minutos", self.var_tempo.get())
        self.config.set("escala_imagem", self.var_escala.get())
        self.config.set("intervalo_verificacao_segundos", self.var_reacao.get())
        self.config.set("poses_aleatorias", self.var_poses.get())
        self.config.set("sempre_no_topo", self.var_topo.get())
        self.config.set("detectar_spotify", self.var_spotify.get())
        self.config.set("detectar_streaming", self.var_stream.get())
        self.config.set("detectar_webcam", self.var_cam.get())
        self.config.set("detectar_print_screen", self.var_print.get())
        self.config.set("dance_speed_ms", self.var_dance.get())
        self.config.set("opacidade", self.var_opa.get())
        self.callback()
        messagebox.showinfo("Sucesso", "Configurações aplicadas com sucesso!", parent=self.top)
        self.top.destroy()
