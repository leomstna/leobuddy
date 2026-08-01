# -*- coding: utf-8 -*-
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try: ctypes.windll.user32.SetProcessDPIAware()
        except: pass

class _EscritorLog:
    def __init__(self, caminho):
        self._arquivo = open(caminho, "a", encoding="utf-8", buffering=1)
    def write(self, msg):
        if msg and msg.strip():
            import datetime
            agora = datetime.datetime.now().strftime("%H:%M:%S")
            self._arquivo.write(f"[{agora}] {msg.strip()}\n")
    def flush(self):
        try: self._arquivo.flush()
        except: pass

_PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
try:
    sys.stdout = _EscritorLog(os.path.join(_PASTA_BASE, "mascote_log.txt"))
    sys.stderr = sys.stdout
except: pass

from core.config_manager import ConfigManager
from core.mascot import Mascote
from core.settings_window import JanelaConfiguracoes
from core.tray_icon import IconeBandeja
from core import detectors

class AplicativoMascote:
    def __init__(self):
        self.config = ConfigManager()
        self.root = tk.Tk()
        self.root.withdraw()

        self.mascote_janela = tk.Toplevel(self.root)
        self.mascote = Mascote(
            self.mascote_janela,
            self.config,
            callback_abrir_config=self.abrir_configuracoes,
            callback_checkup=self.abrir_checkup,
            callback_sair=self.sair,
            callback_diagnostico=self.mostrar_diagnostico,
        )

        self.monitor_tempo = detectors.MonitorTempoUso(minutos_para_resetar=self.config.get("minutos_para_resetar_contador"))
        self._flag_rodando = True

        if self.config.get("detectar_print_screen"):
            self.detector_print = detectors.DetectorPrintScreen(self._on_print_screen)
            self.detector_print.iniciar()

        self.tray = IconeBandeja(
            callback_mostrar_esconder=lambda: self.root.after(0, self.alternar_visibilidade),
            callback_config=lambda: self.root.after(0, self.abrir_configuracoes),
            callback_checkup=lambda: self.root.after(0, self.abrir_checkup),
            callback_sair=lambda: self.root.after(0, self.sair),
            callback_diagnostico=lambda: self.root.after(0, self.mostrar_diagnostico),
        )
        self.tray.iniciar()

        self.thread_deteccao = threading.Thread(target=self._loop_deteccao, daemon=True)
        self.thread_deteccao.start()
        
        if not self.config.get("checkup_concluido"):
            self.root.after(1000, self.abrir_checkup)
        else:
            self.mascote.disparar_evento("boas_vindas")
            self.root.after(6500, lambda: self.mascote.disparar_evento("standart"))

    def abrir_checkup(self):
        from core.checkup_window import JanelaCheckup
        JanelaCheckup(self.root, self.config)

    def _on_print_screen(self):
        if self.config.get("detectar_print_screen"):
            self.root.after(0, lambda: self.mascote.disparar_evento("print_screen"))

    def _loop_deteccao(self):
        import time
        while self._flag_rodando:
            intervalo = float(self.config.get("intervalo_verificacao_segundos"))
            if intervalo < 0.05: intervalo = 0.05
            try:
                evento = self._determinar_evento_atual()
                if evento:
                    self.root.after(0, lambda e=evento: self.mascote.disparar_evento(e))
                elif self.mascote._evento_atual not in (None, "print_screen"):
                    self.root.after(0, self.mascote.voltar_ao_normal)
            except Exception as e:
                print(f"Erro detecao: {e}")
            time.sleep(intervalo)

    def _determinar_evento_atual(self):
        cfg = self.config
        if cfg.get("detectar_tela_cheia") and detectors.tela_cheia_ativa(): return "tela_cheia_jogo_ou_apresentacao"
        if cfg.get("detectar_webcam") and detectors.detectar_webcam_em_uso(): return "webcam_ligada"
        if cfg.get("detectar_uso_prolongado"):
            if self.monitor_tempo.atualizar_e_obter_minutos_ativos() >= cfg.get("tempo_alerta_uso_minutos"):
                self.monitor_tempo.resetar(); return "uso_prolongado"
        if cfg.get("detectar_streaming") and detectors.detectar_streaming(): return "assistindo_streaming"
        if cfg.get("detectar_spotify") and detectors.detectar_spotify(): return "ouvindo_spotify"
        return None

    def abrir_configuracoes(self):
        JanelaConfiguracoes(self.root, self.config, callback_ao_salvar=self._config_atualizada)

    def _config_atualizada(self):
        self.mascote_janela.attributes("-topmost", self.config.get("sempre_no_topo"))
        self.monitor_tempo.minutos_para_resetar = self.config.get("minutos_para_resetar_contador")
        self.mascote.limpar_cache_imagens()
        self.mascote.voltar_ao_normal()

    def mostrar_diagnostico(self):
        relatorio = detectors.diagnostico_completo()
        messagebox.showinfo("Diagnóstico", relatorio)

    def alternar_visibilidade(self):
        if self.mascote_janela.state() == "withdrawn": self.mascote_janela.deiconify()
        else: self.mascote_janela.withdraw()

    def sair(self):
        self._flag_rodando = False
        self.root.quit()
        self.root.destroy()

    def rodar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AplicativoMascote()
    app.rodar()
