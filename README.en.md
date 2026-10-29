# Canon EOS Wi-Fi Shutter Counter — Beginner's Guide

**Free and open source.** This app helps you look for the shutter count of a Canon EOS camera. Originally developed for the **EOS Rebel T7 / EOS 2000D**.

[Home / Português](README.md) · [Full guide in Portuguese](README.pt-BR.md)

> **Important:** Reading a camera directly over Wi-Fi is **experimental and not yet verified end-to-end**. Reading a previously captured `.pcap` network recording has been verified using one Rebel T7 capture. Compatibility with other camera models is unknown.

## Install in 3 steps — No programming experience needed

### 1. Install Python

Go to [python.org/downloads](https://www.python.org/downloads/) and install Python 3.9 or later.

- **Windows:** enable **Add python.exe to PATH** if the installer offers it.
- **macOS:** use the official macOS installer with Tkinter graphics support.

Python is just what runs the app. You don't need to write code or install extra Python libraries.

### 2. Download the project

**[Download the ZIP here](https://github.com/miguelsantana1337/canon-eos-wifi-shutter-counter/archive/refs/heads/main.zip)**, extract it, and open the extracted folder. No Git account is necessary.

### 3. Open the program

| Operating system | How to open |
| --- | --- |
| **Windows** | Double-click **`Iniciar_Windows.bat`**. |
| **macOS** | Double-click **`Iniciar_Mac.command`**. If you get a permissions error, see below. |

**Mac cannot open the `.command` file?** Open Terminal, type `python3 ` followed by a space, drag **app.py** from Finder into Terminal, then press Return. If the interface reports missing `tkinter`, install an official Python build with GUI support.

## In the program, choose one of two modes

### Option A — Try reading from your camera over Wi-Fi (experimental)

1. Turn on the camera's Wi-Fi connection and select a compatible remote-control mode.
2. Connect your **computer to the camera's Wi-Fi** (not your home Wi-Fi). Losing internet is normal.
3. Close other applications currently connected to the camera.
4. Check the camera's IP address. The provided example is `192.168.1.2`; yours may be different.
5. Click **Try Wi-Fi reading (experimental)**.

**If you see an error, your camera might still be working correctly.** Our live implementation is not yet confirmed on hardware.

### Option B — Read an existing network capture (verified on one T7 capture)

1. Click **Choose a .pcap file**.
2. Select a **classic PCAP file containing the camera's shutter-counter response**.
3. If that response is present, the app will show the shutter count.

PCAP files are **network recordings**, not your pictures. JPEG, RAW, and MP4 files will not work. You can read the [advanced capture instructions](docs/CAPTURA_PCAP.md) if needed (Portuguese).

## FAQs

**Is it free?** Yes. MIT-licensed code; no payment, sign-up, or API key.

**Does it work on my Canon model?** We have only validated the offline PCAP mode using a Rebel T7 capture. Please contribute a reproducible report for other models.

**Does this modify my camera?** The app attempts a connection and read operations; it does not intentionally change camera settings, but live mode is experimental.

**Can I run without internet?** Yes. The program does not require internet after download and installation.

**Does it send my network captures anywhere?** No. Captures are processed locally. **Never publish personal PCAP files to public GitHub issues.**

**Troubleshooting:** see the [Portuguese guide](README.pt-BR.md#erros-e-soluções) or [open an issue](https://github.com/miguelsantana1337/canon-eos-wifi-shutter-counter/issues) with the model, firmware, operating system and error message. Do not include passwords, serial numbers or raw captures.

## Command-line usage (advanced)

```bash
python3 canon_t7_wifi.py --pcap "/path/to/network-capture.pcap"
python3 canon_t7_wifi.py --ip 192.168.1.2
python3 -m unittest discover -s tests -v
```

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [License](LICENSE)

Unofficial community project, not affiliated with or endorsed by Canon.