from flask import Flask, request, jsonify
import requests, time, threading, sys
from rsa import generate_keys, encrypt, decrypt

app = Flask(__name__)

# geração das chaves para o app A
my_public_key, my_private_key = generate_keys()
their_public_key = None  # será preenchida com a chave pública do app B

@app.route('/receive', methods=['POST'])
def receive_message(): # endpoint que recebe dados do app B (chave pública ou mensagem)
    global their_public_key
    data = request.get_json()

    # apenas quem possui a chave privada correspondente consegue recuperar a mensagem original, isso garante a confidencialidade

    # caso seja o envio da chave pública
    if data.get('public_key'):
        their_public_key = tuple(data['public_key'])
        print('[App A] 🔑 Chave pública recebida do App B:', their_public_key)
        return jsonify({'message': 'Chave recebida!'})

    # caso seja uma mensagem
    ciphertext = data['message']
    message = decrypt(ciphertext, my_private_key)

    print(f'\n[App A] 📥 Mensagem recebida e descriptografada: {message}\n[App A] 💬 Digite a mensagem para enviar (ou "sair" para encerrar): ', end='', flush=True)
    
    sys.stdout.flush()

    return jsonify({'message': 'Recebido com sucesso!'})

# envia uma mensagem criptografada para o app B
def send_message(text):
    global their_public_key

    if their_public_key is None:
        print('[App A] ❌ Erro: chave pública do App B ainda não recebida.')
        return

    # criptografa a mensagem com a chave pública do destinatário
    encrypted = encrypt(text, their_public_key)
    payload = {'message': encrypted}

    try:
        requests.post('http://localhost:5001/receive', json=payload)
        print(f'[App A] 📤 Mensagem enviada: {text}')
    except requests.exceptions.ConnectionError:
        print('[App A] ⚠️ Erro ao enviar mensagem: App B não disponível.')

# inicia o servidor flask do app A na porta 5000
def run_flask():
    import logging

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # silencia os logs de requisição

    app.run(port=5000)

# realiza a troca inicial de chaves públicas entre app A e app B
# a troca de chaves deve acontecer ANTES de qualquer mensagem ser enviada, porque o rsa depende da chave pública do destinatário para criptografar
def try_exchange_keys():
    global their_public_key
    payload = {'public_key': list(my_public_key)}

    # envia a chave uma única vez
    while True:
        try:
            requests.post('http://localhost:5001/receive', json=payload)
            print('[App A] 🔐 Chave pública enviada para App B. Aguardando chave pública do App B...')
            break
        except requests.exceptions.ConnectionError:
            print('[App A] App B ainda não disponível, tentando novamente...')
            time.sleep(1)

    # aguarda até receber a chave pública do app B
    while their_public_key is None:
        time.sleep(0.5)

if __name__ == '__main__':
    print('[App A] 🟢 Iniciado.')
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    try_exchange_keys()

    # loop principal para envio de mensagens
    while True:
        try:
            text = input('[App A] 💬 Digite a mensagem para enviar (ou "sair" para encerrar): ')
            if text.lower() == 'sair':
                print('[App A] 👋 Encerrando.')
                break
            send_message(text)
        except KeyboardInterrupt:
            print('\n[App A] 👋 Encerrando pelo teclado.')
            break
