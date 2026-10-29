# Guia avançado: como registrar a comunicação em um PCAP

[Voltar à página inicial](../README.md) · [Guia completo para iniciantes](../README.pt-BR.md)

**Este procedimento é opcional e técnico.** O leitor tem dois modos:
- **Wi-Fi ao vivo:** experimental, tenta consultar a câmera sem arquivos.
- **PCAP:** lê um arquivo contendo **uma resposta anterior** da câmera com o contador.

**Importante:** fazer a captura, sozinho, **não faz a câmera fornecer o contador**. Durante a gravação, algum programa autorizado deve executar a consulta que produz essa resposta. Capturas comuns, sem o evento necessário, não servem.

## Segurança primeiro

1. Capture apenas a comunicação da **sua câmera** e do seu computador.
2. **Não envie PCAP pessoal ao GitHub ou a outros sites públicos.** Capturas podem conter dados privados, endereços de rede e identificadores de dispositivos.
3. O filtro `tcp port 15740` reduz o que é capturado, mas não garante anonimização.
4. Não capture senhas ou comunicações de outras pessoas.

## Mac: captura com ferramenta nativa

### 1. Conecte-se à câmera

Abra as configurações de Wi-Fi do macOS e conecte-se à rede criada pela Canon. Não é necessário ter internet nesse momento.

### 2. Descubra o nome da interface Wi-Fi

No Terminal, execute:

```bash
networksetup -listallhardwareports
```

Procure a seção **Wi-Fi** e anote o campo **Device**, por exemplo `en0`. Não presuma que será sempre `en0`.

### 3. Inicie a gravação

Substitua `en0` pelo nome correto, caso seja diferente:

```bash
sudo tcpdump -i en0 -s 0 -w ~/Desktop/canon-capture.pcap 'tcp port 15740'
```

Digite a senha do Mac quando solicitada. O Terminal não mostrará os caracteres da senha; isso é normal.

### 4. Gere uma nova consulta à câmera

Com a captura em andamento, use **um programa que efetivamente solicite o contador**. Apenas conectar-se ao Wi-Fi, sem consulta, geralmente não basta.

Quando o programa terminar, volte ao Terminal e pressione **Control + C**.

### 5. Leia a captura

Abra **`Iniciar_Mac.command`** e clique em **Escolher arquivo .pcap**. Selecione `canon-capture.pcap` da Mesa. Você também pode usar o modo de linha de comando:

```bash
python3 canon_t7_wifi.py --pcap ~/Desktop/canon-capture.pcap
```

Se o contador não aparecer, a captura não contém uma resposta reconhecida, a sessão foi diferente ou o formato não é suportado.

## Windows: alternativa

Para capturas no Windows, normalmente é necessário instalar uma ferramenta como **Wireshark** e o respectivo driver de captura (**Npcap**). Escolha a interface Wi-Fi que se conecta à Canon, filtre por `tcp.port == 15740` e exporte como **`.pcap` clássico**, não `.pcapng`. Depois abra o arquivo pelo aplicativo.

Links oficiais: [Wireshark](https://www.wireshark.org/download.html) · [Npcap](https://npcap.com/).

## Limitações do leitor

O parser offline atual espera **PCAP clássico, enlace Ethernet, IPv4/TCP, porta 15740**, com eventos do contador Canon (`0xD1AC`). Nem toda captura gera um valor, e o arquivo pode não ser compatível. Não há suporte a PCAPNG.

**Não anexe suas capturas brutas em issues.** Prefira relatar o modelo da câmera, firmware, sistema operacional e mensagem de erro sem dados pessoais.