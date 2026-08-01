import win32gui
import win32process
import psutil
import winreg
import time
import ctypes
import keyboard

def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        exe = process.name().lower()
        return title, exe
    except:
        return "", ""

_spotify_pids_cache = set()
_last_spotify_scan = 0

def detectar_spotify():
    global _spotify_pids_cache, _last_spotify_scan
    agora = time.time()
    
    # Remove os PIDs que não existem mais (o usuário fechou o spotify)
    _spotify_pids_cache = {pid for pid in _spotify_pids_cache if psutil.pid_exists(pid)}
    
    # Varredura pesada só roda se não achou PIDs ainda, e a cada 5 segundos no máximo
    if not _spotify_pids_cache and (agora - _last_spotify_scan > 5):
        _last_spotify_scan = agora
        for p in psutil.process_iter(['name', 'pid']):
            try:
                if p.info['name'] and p.info['name'].lower() == 'spotify.exe':
                    _spotify_pids_cache.add(p.info['pid'])
            except: pass
            
    if not _spotify_pids_cache:
        return False
        
    tocando = False
    def winEnumHandler(hwnd, ctx):
        nonlocal tocando
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid in _spotify_pids_cache:
                title = win32gui.GetWindowText(hwnd).lower()
                if title and title not in ["spotify", "spotify premium", "spotify free", ""]:
                    if "angle" not in title and "default" not in title:
                        tocando = True
                        
    try: win32gui.EnumWindows(winEnumHandler, None)
    except: pass
    
    return tocando

def detectar_streaming():
    title, exe = get_active_window_info()
    title_lower = title.lower()
    browsers = ["brave.exe", "chrome.exe", "firefox.exe", "msedge.exe", "opera.exe"]
    if exe in browsers:
        targets = ["netflix", "prime video", "youtube", "hbo", "disney+", "twitch", "vlc", "player"]
        if any(t in title_lower for t in targets):
            return True
    return False

def detectar_webcam_em_uso():
    caminhos_registro = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
    ]
    for base_path in caminhos_registro:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_path)
            for i in range(1024):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    if subkey_name == "NonPackaged":
                        for j in range(1024):
                            try:
                                np_name = winreg.EnumKey(subkey, j)
                                np_key = winreg.OpenKey(subkey, np_name)
                                last_used_stop, _ = winreg.QueryValueEx(np_key, "LastUsedTimeStop")
                                if last_used_stop == 0: 
                                    winreg.CloseKey(np_key)
                                    return True
                                winreg.CloseKey(np_key)
                            except: 
                                break
                    else:
                        try:
                            last_used_stop, _ = winreg.QueryValueEx(subkey, "LastUsedTimeStop")
                            if last_used_stop == 0: 
                                winreg.CloseKey(subkey)
                                return True
                        except:
                            pass
                    winreg.CloseKey(subkey)
                except: 
                    break
            winreg.CloseKey(key)
        except:
            pass
    return False

def tela_cheia_ativa():
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd: return False
        rect = win32gui.GetWindowRect(hwnd)
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        user32 = ctypes.windll.user32
        sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return w >= sw and h >= sh
    except:
        return False

class MonitorTempoUso:
    def __init__(self, minutos_para_resetar=5):
        self.inicio = time.time()
        self.minutos_para_resetar = minutos_para_resetar
        
    def get_idle_time(self):
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0

    def atualizar_e_obter_minutos_ativos(self):
        idle = self.get_idle_time()
        if idle > (self.minutos_para_resetar * 60):
            self.resetar()
        return (time.time() - self.inicio) / 60.0

    def resetar(self):
        self.inicio = time.time()

class DetectorPrintScreen:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        
    def iniciar(self):
        if not self.running:
            self.running = True
            try:
                keyboard.on_press_key("print screen", lambda e: self.callback())
                keyboard.add_hotkey("win+shift+s", lambda: self.callback())
                keyboard.add_hotkey("ctrl+shift+9", lambda: self.callback())
            except Exception as e:
                print(f"Erro ao registrar hook de print: {e}")

def diagnostico_completo():
    t, e = get_active_window_info()
    return f"Janela Ativa: {t}\nProcesso: {e}\nWebcam: {detectar_webcam_em_uso()}\nSpotify: {detectar_spotify()}\nStreaming: {detectar_streaming()}\nTela Cheia: {tela_cheia_ativa()}"
