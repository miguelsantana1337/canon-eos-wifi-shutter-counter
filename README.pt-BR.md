# Contador de disparos Canon EOS via Wi-Fi

Leitor **gratuito, experimental e de código aberto** para consultar disparos de câmeras Canon EOS por PTP/IP (Wi-Fi) ou analisar capturas PCAP localmente.

- **Validado em captura:** Canon Rebel T7 / EOS 2000D, propriedade Canon `0xD1AC`, operação EOS GetEvent `0x9116`.
- **Wi-Fi ao vivo:** ainda não validado de ponta a ponta em hardware real.
- **Sem pagamento, cadastro, bibliotecas adicionais ou envio de dados.** Python 3.9+.
- **Licença MIT.**

## Como utilizar

Conecte o computador ao Wi-Fi da câmera e feche outros aplicativos que utilizem a câmera.

```bash
python3 canon_t7_wifi.py
python3 canon_t7_wifi.py --ip 192.168.1.2 --json
```

A câmera precisa estar pareada e aceitar controle remoto. O IP pode ser diferente.

Para verificar um arquivo de captura PCAP **localmente**:

```bash
python3 canon_t7_wifi.py --pcap /caminho/para/captura.pcap
```

O leitor PCAP suporta o formato clássico com enlace Ethernet, tráfego IPv4/TCP e porta 15740. Não suporta PCAPNG diretamente.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## Privacidade

Nenhum arquivo é enviado pela internet. Capturas de rede podem conter dados pessoais. **Não publique capturas integrais em issues públicas.**

## Limitações

- A leitura direta por Wi-Fi precisa de validação prática.
- Outros modelos e firmwares não foram confirmados.
- A câmera pode não retornar a propriedade em todas as sessões.
- Não é uma ferramenta oficial da Canon.

Ajude a melhorar em [CONTRIBUTING.md](CONTRIBUTING.md).