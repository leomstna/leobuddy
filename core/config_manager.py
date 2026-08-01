import json
import os

class ConfigManager:
    def __init__(self):
        self.file = "config.json"
        self.default = {
            "tempo_alerta_uso_minutos": 120,
            "minutos_para_resetar_contador": 5,
            "sempre_no_topo": True,
            "detectar_print_screen": True,
            "detectar_webcam": True,
            "detectar_streaming": True,
            "detectar_spotify": True,
            "detectar_tela_cheia": False,
            "intervalo_verificacao_segundos": 2.0,
            "escala_imagem": 200,
            "checkup_concluido": False,
            "poses_aleatorias": True,
            "dance_speed_ms": 450,
            "opacidade": 1.0,
            "image_mapping": {
                "standart": "STANDART",
                "boas_vindas": "OLA",
                "ouvindo_spotify": "DANÇANDO",
                "assistindo_streaming": "PIPOCA",
                "webcam_ligada": "CAMERA 2",
                "print_screen": "MÃO NA TELA",
                "uso_prolongado": "RELOGIO GIGANTE",
                "tela_cheia_jogo_ou_apresentacao": "DE COSTAS",
                "trabalhando_documento": "PAPELADA",
                "lendo_livro": "LENDO LIVRO",
                "cafe": "CAFE ENORME",
                "ausente": "OLHANDO PRA BAIXO",
                "confuso": "CONFUSO",
                "pensando": "PENSANDO",
                "joia": "JOIA"
            },
            "image_offsets": {}
        }
        self.data = self.default.copy()
        self.load()

    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r", encoding="utf-8") as f:
                    carregado = json.load(f)
                    self.data.update(carregado)
            except:
                pass
        # Atualiza mapping caso falte algo
        for k, v in self.default["image_mapping"].items():
            if k not in self.data["image_mapping"]:
                self.data["image_mapping"][k] = v
        self.save()

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key):
        return self.data.get(key, self.default.get(key))

    def set(self, key, val):
        self.data[key] = val
        self.save()
