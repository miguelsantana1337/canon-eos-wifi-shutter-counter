# Contador de disparos Canon EOS — gratuito

### Descubra quantas fotos sua câmera Canon já tirou

Leitor **gratuito e de código aberto**, com interface gráfica em português e inglês. Criado inicialmente para a **Canon EOS Rebel T7 / EOS 2000D**.

> **Importante:** a leitura direta pelo Wi-Fi **ainda é experimental**. A leitura de uma captura de rede (arquivo `.pcap`) foi comprovada com um registro real da Rebel T7. Não garantimos que o Wi-Fi funcione com todas as câmeras.

**[Guia completo em português](README.pt-BR.md) · [English instructions](README.en.md)**

## Como começar (sem saber programar)

### 1. Instale o Python, caso não tenha

Baixe gratuitamente em **[python.org/downloads](https://www.python.org/downloads/)**.

- **Windows:** durante a instalação, marque **Add python.exe to PATH**, se essa opção aparecer.
- **Mac:** use o instalador para macOS do site oficial. A interface gráfica precisa do **Tkinter**, incluído nos instaladores oficiais usuais.

O Python é o programa usado para abrir o nosso aplicativo. Você **não precisa aprender Python**.

### 2. Baixe o projeto

Clique em **[Download ZIP](https://github.com/miguelsantana1337/canon-eos-wifi-shutter-counter/archive/refs/heads/main.zip)**, extraia o arquivo ZIP e abra a pasta extraída.

### 3. Abra o aplicativo

| Seu computador | O que fazer |
| --- | --- |
| **Windows** | Clique duas vezes em **`Iniciar_Windows.bat`**. |
| **Mac** | Clique duas vezes em **`Iniciar_Mac.command`**. Se o macOS impedir a execução, veja o [guia do Mac](README.pt-BR.md#mac-o-arquivo-command-não-abre). |

Quando abrir, aparecerão dois caminhos:

**Opção A — Ler a câmera por Wi-Fi (experimental)**

1. Na Canon, ative o Wi-Fi e coloque a câmera no modo de conexão/controle remoto.
2. Conecte o computador **ao Wi-Fi da Canon** (não ao da sua casa).
3. Feche outros aplicativos que estejam usando a câmera.
4. No programa, confirme o IP (o exemplo é `192.168.1.2`) e clique em **Tentar leitura pelo Wi-Fi**.
5. Se funcionar, o contador aparecerá na tela. **Se não funcionar, isso não significa que a câmera tenha zero disparos.**

**Opção B — Abrir um PCAP já existente (testada)**

1. Clique em **Escolher arquivo .pcap**.
2. Selecione uma captura de rede **que contenha a leitura da câmera**.
3. O programa procura o contador no arquivo e mostra o resultado.

`PCAP` é uma gravação da comunicação de rede, **não é uma foto**. Fotos JPG/RAW não substituem um PCAP.

## O que já funciona?

| Recurso | Situação |
| --- | --- |
| Interface com botões, em português e inglês | Disponível |
| Leitura de contador em arquivo PCAP da Rebel T7 | Validada em uma captura |
| Comunicação com a câmera pelo Wi-Fi | Experimental, ainda precisa de testes reais |
| Windows e macOS | Scripts de abertura disponíveis; validação em diferentes versões pendente |
| Outras câmeras Canon | Não validadas |

## Dúvidas mais comuns

- **É grátis?** Sim. Código sob licença MIT; nenhuma conta ou pagamento é necessário.
- **Preciso de cabo USB?** O modo Wi-Fi não usa cabo. Para usar um PCAP, é preciso ter a gravação da comunicação.
- **Preciso pagar pelo Camera Shutter Count?** Não para usar este projeto. Não prometemos, porém, que nossa leitura Wi-Fi funcione em todos os modelos.
- **O computador ficará sem internet ao entrar no Wi-Fi da câmera?** Pode acontecer. É normal e a leitura é local.
- **O Mac não abriu?** Veja o [guia de instalação e erros](README.pt-BR.md).
- **O programa envia meus dados?** Não. Ele não envia arquivos a serviços externos. **Nunca publique capturas de rede pessoais no GitHub.**

## Para quem programa

Use sem interface gráfica:

```bash
python3 canon_t7_wifi.py --pcap "/caminho/arquivo.pcap"
python3 canon_t7_wifi.py --ip 192.168.1.2
python3 -m unittest discover -s tests -v
```

[Como contribuir](CONTRIBUTING.md) · [Segurança e privacidade](SECURITY.md)

**Projeto comunitário, não oficial e sem vínculo com a Canon.**