import tkinter as tk
from tkinter import ttk, messagebox

class JanelaCheckup:
    def __init__(self, root, config):
        self.top = tk.Toplevel(root)
        self.top.title("Check-up e Calibragem Oficial - Mascote Hyo")
        self.top.geometry("500x650")
        self.top.configure(bg="#1e1e1e")
        self.top.attributes("-topmost", True)
        self.config = config

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("TButton", background="#3a3a3a", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#505050")])

        main_frame = tk.Frame(self.top, bg="#1e1e1e", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="🛠️ Check-up Completo de Reações", font=("Segoe UI", 15, "bold"), bg="#1e1e1e", fg="#4da6ff").pack(pady=(0, 5))
        
        instrucoes = (
            "Teste as interações abaixo para validar se o mascote está respondendo perfeitamente.\n"
            "Assim que o mascote mudar para a imagem correspondente, marque o item."
        )
        ttk.Label(main_frame, text=instrucoes, wraplength=460, justify="center").pack(pady=(0, 10))

        canvas = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        testes = [
            ("🎵 Dê play em uma música no Spotify", "DANÇANDO.png"),
            ("⏸️ Pause a música no Spotify", "STANDART.png"),
            ("📸 Tire um Print (PrintScreen / LightShot / Win+Shift+S)", "MÃO NA TELA.png"),
            ("🍿 Abra Netflix, YouTube ou Twitch no navegador", "PIPOCA.png"),
            ("📷 Abra o app Câmera ou ligue a Webcam", "CAMERA 2.png"),
            ("💬 Mensagem de Boas-vindas (Ao abrir)", "OLA.png / CONFUSO.png"),
            ("☕ Simule pausa para café / descanse", "CAFE ENORME.png"),
            ("💻 Deixe o computador ocioso por instantes", "OLHANDO PRA BAIXO.png")
        ]

        self.vars = []
        for texto, reacao in testes:
            f = tk.Frame(scrollable_frame, bg="#2b2b2b", padx=10, pady=6)
            f.pack(fill=tk.X, pady=4, ipadx=5)
            
            var = tk.BooleanVar(value=False)
            self.vars.append(var)
            
            chk = tk.Checkbutton(f, text=f" {texto}", variable=var, bg="#2b2b2b", fg="white", 
                                 selectcolor="#1e1e1e", activebackground="#2b2b2b", activeforeground="white",
                                 font=("Segoe UI", 10, "bold"))
            chk.pack(anchor="w")
            
            tk.Label(f, text=f"   ↳ Imagem esperada: {reacao}", bg="#2b2b2b", fg="#aaaaaa", font=("Segoe UI", 9)).pack(anchor="w")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(main_frame, bg="#1e1e1e")
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        ttk.Button(btn_frame, text="✅ Concluir Calibragem e Iniciar", command=self.concluir).pack(ipadx=15, ipady=6)

    def concluir(self):
        self.config.set("checkup_concluido", True)
        messagebox.showinfo("Sucesso", "Calibragem concluída com sucesso! Divirta-se com seu mascote.", parent=self.top)
        self.top.destroy()
