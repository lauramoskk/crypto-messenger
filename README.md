# Crypto Messenger

### Descrição

Crypto Messenger é um chat seguro desenvolvido em Python, formado por duas aplicações Flask que se comunicam utilizando criptografia assimétrica baseada no algoritmo RSA.

Cada aplicação gera suas próprias chaves pública e privada e realiza uma troca inicial de chaves antes do envio das mensagens, garantindo que apenas o destinatário possa ler o conteúdo criptografado.

O sistema permite comunicação bidirecional, possibilitando que App A e App B troquem mensagens simultaneamente de forma segura e confiável.

O projeto foi criado de forma didática, com o algoritmo RSA implementado manualmente, enquanto o Flask simula a comunicação entre as duas aplicações.

As mensagens são enviadas via requisições HTTP, e threads permitem que cada aplicação execute simultaneamente o servidor e a interface de envio de mensagens.

Todo o processo de criptografia e descriptografia ocorre automaticamente, sem depender de bibliotecas externas, tornando o código enxuto, didático e fácil de entender.

https://github.com/user-attachments/assets/902fd720-ba69-4ee4-b9a9-4309a5cd2220

<br>

### Instruções de execução
```bash
# 1. Clone o repositório e acesse a pasta:
git clone https://github.com/seu-usuario/crypto-messenger.git
cd crypto-messenger

# 2. Instale as dependências necessárias:
pip install flask requests

# 3. Inicie o primeiro aplicativo (App A) em um terminal:
python chat_a.py

# 4. Inicie o segundo aplicativo (App B) em outro terminal:
python chat_b.py

# 5. Envie mensagens:
# - Digite sua mensagem em qualquer um dos aplicativos para enviar para o outro.  
# - Para encerrar a execução, digite: sair
```
