import threading
try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_PYSTRAY = True
except ImportError:
    HAS_PYSTRAY = False

class IconeBandeja:
    def __init__(self, callback_mostrar_esconder, callback_config, callback_checkup, callback_sair, callback_diagnostico):
        self.callback_mostrar_esconder = callback_mostrar_esconder
        self.callback_config = callback_config
        self.callback_checkup = callback_checkup
        self.callback_sair = callback_sair
        self.callback_diagnostico = callback_diagnostico

    def criar_imagem_padrao(self):
        img = Image.new('RGB', (64, 64), color=(30, 30, 30))
        d = ImageDraw.Draw(img)
        d.rectangle([16, 16, 48, 48], fill=(77, 166, 255))
        return img

    def iniciar(self):
        if not HAS_PYSTRAY: return
        menu = pystray.Menu(
            pystray.MenuItem("Mostrar/Esconder", lambda: self.callback_mostrar_esconder()),
            pystray.MenuItem("Configurações", lambda: self.callback_config()),
            pystray.MenuItem("Refazer Check-up", lambda: self.callback_checkup()),
            pystray.MenuItem("Diagnóstico", lambda: self.callback_diagnostico()),
            pystray.MenuItem("Sair", lambda: self.callback_sair())
        )
        self.icon = pystray.Icon("mascote_hyo", self.criar_imagem_padrao(), "Mascote Hyo", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()
