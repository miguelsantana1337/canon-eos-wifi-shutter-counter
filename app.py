#!/usr/bin/env python3
"""Optional desktop GUI for Canon EOS Wi-Fi Shutter Counter.

Uses Python's tkinter (included in official python.org installers).
No PCAP is sent to any server.
"""
import queue
import threading
import webbrowser

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError:
    raise SystemExit(
        "Interface grafica indisponivel. Instale Python de python.org com Tkinter. "
        "Use 'python3 canon_t7_wifi.py --help' como alternativa.\n"
        "GUI unavailable. Install Python from python.org with Tkinter."
    )

from canon_t7_wifi import PTPError, read_from_pcap, read_live

REPO_URL = "https://github.com/miguelsantana1337/canon-eos-wifi-shutter-counter"

COPY = {
    "pt": {
        "window": "Canon EOS - Contador de disparos",
        "subtitle": "Gratuito, local e de codigo aberto",
        "intro": "Descubra quantas fotos sua camera registrou.",
        "live_title": "1. Tentar ler pela rede Wi-Fi da camera",
        "live_detail": (
            "Em testes: conecte o computador ao Wi-Fi da Canon e feche outros "
            "programas que usam a camera. Pode nao funcionar ainda."
        ),
        "ip": "Endereco IP da camera:",
        "live_button": "Tentar leitura pelo Wi-Fi (experimental)",
        "pcap_title": "2. Verificar uma captura de rede ja existente",
        "pcap_detail": (
            "Opcao testada com uma captura da Rebel T7. Voce precisa de um "
            "arquivo .pcap registrado durante a leitura da camera."
        ),
        "pcap_button": "Escolher arquivo .pcap",
        "result_title": "Numero de disparos",
        "initial": "Nenhum resultado ainda.",
        "busy": "Consultando... aguarde a resposta.",
        "live_result": "Leitura pelo Wi-Fi concluida. Confira na camera.",
        "pcap_result": "Valor encontrado no arquivo selecionado (nao e leitura ao vivo).",
        "error": "Nao foi possivel obter o numero.",
        "error_title": "Falha na leitura",
        "error_hint": (
            "Confira o Wi-Fi, o endereco IP e feche outros aplicativos Canon. "
            "Para capturas, selecione um arquivo PCAP classico."
        ),
        "help": "Ver instrucoes e resolver problemas",
        "lang": "English",
        "privacy": "Privacidade: o programa nao envia capturas para a internet.",
        "filetypes": "Capturas de rede",
        "allfiles": "Todos os arquivos",
    },
    "en": {
        "window": "Canon EOS - Shutter Counter",
        "subtitle": "Free, local, and open-source",
        "intro": "Find out how many pictures your camera has taken.",
        "live_title": "1. Try reading the camera over Wi-Fi",
        "live_detail": (
            "Experimental: connect your computer to the Canon Wi-Fi network and "
            "close any other camera applications. This may not work yet."
        ),
        "ip": "Camera IP address:",
        "live_button": "Try Wi-Fi reading (experimental)",
        "pcap_title": "2. Check an existing network capture",
        "pcap_detail": (
            "Tested with a Rebel T7 capture. You need a .pcap file recorded "
            "while camera communication was active."
        ),
        "pcap_button": "Choose a .pcap file",
        "result_title": "Shutter count",
        "initial": "No result yet.",
        "busy": "Reading... please wait.",
        "live_result": "Wi-Fi reading complete. Please verify on camera.",
        "pcap_result": "Value found in the selected file (not a live reading).",
        "error": "Could not obtain a shutter count.",
        "error_title": "Reading failed",
        "error_hint": (
            "Check the Wi-Fi connection, IP address and close other Canon apps. "
            "For captures, use a classic PCAP file."
        ),
        "help": "Read instructions and troubleshooting",
        "lang": "Português",
        "privacy": "Privacy: the app never uploads captures to the internet.",
        "filetypes": "Network captures",
        "allfiles": "All files",
    },
}


class App:
    def __init__(self, root):
        self.root = root
        self.lang = "pt"
        self.events = queue.Queue()
        self.busy = False
        self.labels = {}

        root.title(COPY["pt"]["window"])
        root.geometry("700x650")
        root.minsize(540, 560)

        style = ttk.Style(root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("Arial", 22, "bold"))
        style.configure("Section.TLabel", font=("Arial", 13, "bold"))
        style.configure("Result.TLabel", font=("Arial", 35, "bold"))
        style.configure("Normal.TLabel", font=("Arial", 11))
        style.configure("Primary.TButton", font=("Arial", 11, "bold"), padding=11)
        style.configure("Normal.TButton", font=("Arial", 10), padding=7)

        frame = ttk.Frame(root, padding=24)
        frame.pack(fill="both", expand=True)
        self.add_label(frame, "title", "Title.TLabel")
        self.add_label(frame, "subtitle", "Normal.TLabel")
        self.add_label(frame, "intro", "Normal.TLabel")
        ttk.Separator(frame).pack(fill="x", pady=12)

        self.add_label(frame, "live_title", "Section.TLabel")
        self.add_label(frame, "live_detail", "Normal.TLabel", wraplength=625)
        ip_row = ttk.Frame(frame)
        ip_row.pack(fill="x", pady=(9, 5))
        self.ip_label = ttk.Label(ip_row, style="Normal.TLabel")
        self.ip_label.pack(side="left")
        self.ip = ttk.Entry(ip_row, width=20, font=("Arial", 11))
        self.ip.insert(0, "192.168.1.2")
        self.ip.pack(side="left", padx=(10, 0))
        self.btn_wifi = ttk.Button(
            frame, style="Primary.TButton", command=self.try_wifi
        )
        self.btn_wifi.pack(fill="x", pady=(4, 14))

        self.add_label(frame, "pcap_title", "Section.TLabel")
        self.add_label(frame, "pcap_detail", "Normal.TLabel", wraplength=625)
        self.btn_pcap = ttk.Button(
            frame, style="Primary.TButton", command=self.pick_pcap
        )
        self.btn_pcap.pack(fill="x", pady=(9, 15))
        ttk.Separator(frame).pack(fill="x", pady=(0, 12))

        self.add_label(frame, "result_title", "Section.TLabel")
        self.count = ttk.Label(frame, text="—", style="Result.TLabel")
        self.count.pack(anchor="w", pady=(5, 0))
        self.status = ttk.Label(
            frame, style="Normal.TLabel", wraplength=625, justify="left"
        )
        self.status.pack(anchor="w", fill="x", pady=(2, 9))

        bottom = ttk.Frame(frame)
        bottom.pack(fill="x", side="bottom")
        self.btn_help = ttk.Button(
            bottom, command=lambda: webbrowser.open(REPO_URL + "#readme"),
            style="Normal.TButton"
        )
        self.btn_help.pack(side="left")
        self.btn_lang = ttk.Button(
            bottom, command=self.toggle_language, style="Normal.TButton"
        )
        self.btn_lang.pack(side="right")
        self.add_label(frame, "privacy", "Normal.TLabel")

        self.translate()
        self.root.after(100, self.poll)

    def add_label(self, parent, key, style, wraplength=0):
        label = ttk.Label(parent, style=style, wraplength=wraplength, justify="left")
        label.pack(anchor="w", fill="x", pady=(0, 5))
        self.labels[key] = label

    def t(self, key):
        return COPY[self.lang][key]

    def translate(self):
        self.root.title(self.t("window"))
        # Keep the most recent result when switching languages.
        for key, label in self.labels.items():
            label.configure(text=self.t("window") if key == "title" else self.t(key))
        self.ip_label.configure(text=self.t("ip"))
        self.btn_wifi.configure(text=self.t("live_button"))
        self.btn_pcap.configure(text=self.t("pcap_button"))
        self.btn_help.configure(text=self.t("help"))
        self.btn_lang.configure(text=self.t("lang"))
        if not self.busy and self.count.cget("text") == "—":
            self.status.configure(text=self.t("initial"))

    def toggle_language(self):
        self.lang = "en" if self.lang == "pt" else "pt"
        self.translate()

    def start(self, operation, arg):
        if self.busy:
            return
        self.busy = True
        self.btn_wifi.configure(state="disabled")
        self.btn_pcap.configure(state="disabled")
        self.status.configure(text=self.t("busy"))
        self.count.configure(text="…")
        def worker():
            try:
                value = read_live(arg) if operation == "wifi" else read_from_pcap(arg)
                self.events.put(("ok", operation, value))
            except (OSError, PTPError, ValueError) as exc:
                self.events.put(("error", operation, str(exc)))
        threading.Thread(target=worker, daemon=True).start()

    def try_wifi(self):
        address = self.ip.get().strip()
        if not address:
            messagebox.showerror(self.t("error_title"), self.t("error_hint"))
            return
        self.start("wifi", address)

    def pick_pcap(self):
        path = filedialog.askopenfilename(
            title=self.t("pcap_button"),
            filetypes=[
                (self.t("filetypes"), "*.pcap"),
                (self.t("allfiles"), "*.*")
            ]
        )
        if path:
            self.start("pcap", path)

    def poll(self):
        try:
            while True:
                result, operation, value = self.events.get_nowait()
                self.busy = False
                self.btn_wifi.configure(state="normal")
                self.btn_pcap.configure(state="normal")
                if result == "ok":
                    self.count.configure(text=f"{value:,}".replace(",", "."))
                    self.status.configure(
                        text=self.t("live_result" if operation == "wifi" else "pcap_result")
                    )
                else:
                    self.count.configure(text="—")
                    self.status.configure(text=self.t("error"))
                    messagebox.showerror(
                        self.t("error_title"),
                        f"{value}\n\n{self.t('error_hint')}"
                    )
        except queue.Empty:
            pass
        self.root.after(100, self.poll)


def main():
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        raise SystemExit(
            f"Could not start the graphical interface: {exc}. "
            "Try the command-line reader or install Python with Tkinter."
        )
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
