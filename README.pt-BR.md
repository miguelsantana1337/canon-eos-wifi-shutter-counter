# Guia completo para iniciantes — Canon EOS Shutter Counter

Este guia explica **desde a instalação**. Não é preciso saber programação.

[Voltar para a página inicial](README.md) · [English](README.en.md)

## Primeiro: o que este aplicativo faz?

O contador de disparos é o número de vezes que o obturador da câmera foi acionado (conforme o dado fornecido pela câmera). O aplicativo tenta ler esse dado, sem pagamento.

Existem **duas formas diferentes**:

- **Wi-Fi (EXPERIMENTAL):** tenta conversar diretamente com a câmera; pode falhar mesmo que ela esteja funcionando corretamente.
- **Arquivo PCAP (VALIDADO EM UMA CAPTURA):** examina uma gravação de rede que contenha a resposta da câmera. **Não basta selecionar qualquer PCAP; ele precisa conter o evento do contador.**

O teste com arquivo foi realizado com uma **Canon Rebel T7 / EOS 2000D**. Outros modelos e o Wi-Fi ao vivo precisam de testes adicionais.

## Passo 1 — Instalar o Python

Python é a tecnologia que abre o aplicativo.

1. Acesse [python.org/downloads](https://www.python.org/downloads/).
2. Baixe a versão estável para seu sistema.
3. Instale normalmente.
4. No **Windows**, se aparecer a opção **Add python.exe to PATH**, marque-a antes de instalar.
5. No **Mac**, prefira o instalador oficial da página para incluir suporte gráfico (Tkinter).

Você não precisa criar conta, configurar servidor nem instalar bibliotecas pelo `pip`.

## Passo 2 — Baixar os arquivos

1. [Clique aqui para baixar o ZIP do projeto](https://github.com/miguelsantana1337/canon-eos-wifi-shutter-counter/archive/refs/heads/main.zip).
2. Abra **Downloads**.
3. Extraia o ZIP (no Mac, clique duas vezes; no Windows, clique com o botão direito e escolha **Extrair tudo**).
4. Entre na pasta **canon-eos-wifi-shutter-counter-main**.

**Não é preciso instalar Git nem usar comandos `git clone`.**

## Passo 3 — Abrir

### Windows

1. Abra a pasta extraída.
2. Clique duas vezes em **`Iniciar_Windows.bat`**.
3. Se aparecer uma janela preta, mantenha-a aberta: ela inicia a interface gráfica.
4. Se aparecer **Python não encontrado**, volte ao passo 1. Feche e reabra a janela após a instalação.

> O Windows pode pedir confirmação antes de executar um script obtido da internet. Execute apenas arquivos que você baixou deste repositório e conseguiu revisar. Não desative as proteções de segurança do sistema.

### Mac

1. Abra a pasta extraída.
2. Clique duas vezes em **`Iniciar_Mac.command`**.
3. O Terminal abrirá a interface gráfica. **Não feche o Terminal enquanto usar o aplicativo.**
4. Se não funcionar, consulte a seção a seguir.

### Mac: o arquivo .command não abre

O macOS pode bloquear scripts novos ou dizer que você não tem permissão.

**Opção 1:** tente clicar com o botão direito no arquivo e selecionar **Abrir**. Analise o aviso antes de continuar.

**Opção 2:** abra o Terminal, digite `chmod +x ` (com um espaço no final), arraste **Iniciar_Mac.command** para a janela do Terminal e pressione Enter. Depois abra o arquivo novamente.

**Opção 3 (alternativa):** no Terminal, digite `python3 ` (com espaço no final), arraste o arquivo **app.py** para a janela e pressione Enter. Esse caminho não exige mudar permissões.

Se aparecer **No module named tkinter** ou **Tkinter não disponível**, reinstale o Python com o instalador de [python.org](https://www.python.org/downloads/) que inclua o suporte Tcl/Tk.

## Passo 4 — Escolher como deseja ler

### A) Pela rede Wi-Fi da câmera — em testes

1. Ligue a Canon e certifique-se de que a bateria esteja carregada.
2. Ative a conexão Wi-Fi nas configurações da câmera.
3. Coloque-a no modo de conexão com computador/controle remoto, se disponível.
4. **No computador, conecte-se à rede Wi-Fi da Canon**. Essa rede pode não oferecer internet, e isso é normal.
5. Feche aplicativos que já estejam usando a câmera (por exemplo, Canon Camera Connect ou outro programa de leitura).
6. Abra nosso aplicativo e confira o campo **Endereço IP da câmera**. O IP padrão sugerido é `192.168.1.2`, **mas pode ser diferente no seu caso**.
7. Clique em **Tentar leitura pelo Wi-Fi (experimental)**.

**Se aparecer um número:** é o dado que o programa conseguiu ler. Se possível, compare com uma leitura independente e repita após tirar uma foto.

**Se aparecer erro:** ainda pode ser uma limitação da implementação; não é prova de defeito da câmera. Confira o endereço IP, a conexão e o modo remoto.

> Aviso: **não garantimos que a leitura direta funcione na Rebel T7 sem ajustes adicionais.** Estamos convidando colaboradores a testar e corrigir essa parte.

### B) Com um arquivo PCAP — validado em uma captura

Você só precisa desta opção **se já tiver uma captura de comunicação com a Canon**.

1. Clique em **Escolher arquivo .pcap**.
2. Escolha o arquivo salvo no computador.
3. O aplicativo procura a propriedade Canon do contador (identificador técnico `0xD1AC`).
4. Se ela estiver presente, mostrará o número na tela.

**Atenção:** não tente abrir JPG, CR2, vídeos ou arquivos ZIP por essa opção. Ela lê **somente capturas clássicas do Wi-Fi/da rede que contenham a resposta do contador**.

Precisa capturar a comunicação? É uma tarefa mais técnica. Leia [o guia avançado de captura](docs/CAPTURA_PCAP.md).

## Erros e soluções

| Mensagem ou situação | O que significa / como resolver |
| --- | --- |
| **Python não encontrado** | Instale pelo site oficial e tente novamente. |
| **No module named tkinter** | Instale a distribuição do Python com suporte ao Tkinter. |
| **Permission denied** no Mac | Veja a seção **Mac: o arquivo .command não abre**. |
| **Camera disconnected** | A câmera encerrou a sessão. Confira a conexão e feche outros aplicativos. |
| **Connection refused / timed out** | Verifique se o computador está no Wi-Fi da Canon, o IP está correto e a câmera está aceitando conexão. |
| **ShutterCounter event not returned** | O contador não foi fornecido nessa sessão; o modo Wi-Fi ainda é experimental. |
| **ShutterCounter property not found** | O PCAP selecionado não contém uma leitura reconhecível do contador. |
| **Unsupported format** | Arquivo não é PCAP clássico ou usa outro tipo de captura. PCAPNG não é suportado por enquanto. |
| **Não aparece a interface** | Abra o programa pelo Terminal para ler o erro; pode faltar Python ou Tkinter. |

## Privacidade e segurança

- O aplicativo funciona **localmente**.
- Ele não faz login, não cobra e não envia seus arquivos para serviços online.
- A conexão Wi-Fi é feita diretamente com o IP da câmera indicado por você.
- **Não coloque arquivos PCAP pessoais em issues, pull requests ou repositórios públicos**: eles podem conter informações privadas da rede.
- Use somente em câmeras e redes que você está autorizado a acessar.

## Como pedir ajuda ou contribuir

Acesse [Issues](https://github.com/miguelsantana1337/canon-eos-wifi-shutter-counter/issues) e informe:
- Qual é o modelo da câmera e a versão do firmware?
- Está no Windows ou Mac? Qual versão?
- Você usou **Wi-Fi** ou **arquivo PCAP**?
- Qual erro apareceu (sem enviar senhas, números de série ou capturas de rede)?

Código aberto sob [licença MIT](LICENSE). Projeto **não oficial**, sem vínculo com a Canon.