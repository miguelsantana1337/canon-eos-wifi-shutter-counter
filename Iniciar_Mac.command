#!/bin/bash
cd "$(dirname "$0")" || exit 1
printf '\n==========================================\n'
printf ' Canon EOS - Contador de disparos\n'
printf '==========================================\n\n'
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 nao encontrado."
  echo "Instale pelo site oficial: https://www.python.org/downloads/"
  echo "Depois, abra este arquivo novamente."
else
  python3 app.py
  if [ $? -ne 0 ]; then
    echo ""
    echo "Nao foi possivel abrir a interface grafica."
    echo "Confira se Python foi instalado pelo site python.org com Tkinter."
    echo "Leia README.pt-BR.md para mais orientacoes."
  fi
fi
echo ""
read -r -p "Pressione Enter para fechar esta janela..." _
