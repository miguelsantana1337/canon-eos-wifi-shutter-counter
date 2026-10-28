# Canon EOS Wi-Fi Shutter Counter

Open-source, free **experimental** shutter-count reader for Canon EOS cameras over PTP/IP (Wi-Fi), with a supported offline PCAP reader.

- **Tested offline:** Canon EOS Rebel T7 / EOS 2000D, Canon property `0xD1AC` from EOS GetEvent `0x9116`.
- **Live Wi-Fi:** experimental; not yet validated end-to-end with real camera hardware.
- **No payment, registration, dependencies or online upload required.** Python 3.9+.
- **License:** MIT.

[Português (Brasil)](README.pt-BR.md)

## Usage

Connect your Mac or PC to your camera's Wi-Fi network, close other camera applications, then:

```bash
python3 canon_t7_wifi.py
python3 canon_t7_wifi.py --ip 192.168.1.2 --json
```

The camera must already be paired and in a compatible remote-control mode. The IP may vary.

Read an **existing local capture** without connecting to a camera:

```bash
python3 canon_t7_wifi.py --pcap /path/to/capture.pcap
```

Classic Ethernet PCAP with IPv4 TCP traffic on port 15740 is currently supported; PCAPNG isn't supported.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

## Privacy

The reader does not upload captures, communicate with third-party services, or use an API key. PCAP files can include sensitive network data; **never upload your personal captures to public issues**.

## Known limitations

- Live connection and compatibility with other models or firmware versions have not been verified.
- The event containing the shutter counter may not be emitted every time.
- Offline parsing is intentionally limited to Ethernet classic-PCAP IPv4/TCP PTP/IP.
- The shutter counter value is a camera-reported value and not a warranty of camera condition.

This is an unofficial community project, not associated with or endorsed by Canon.

Contributions and reproducible, privacy-redacted test reports are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).