from flask import Flask, request, jsonify
import requests, time , threading, sys
from rsa import generate_keys, encrypt, decrypt

app = Flask(__name__)

# geração das chaves para o app B
my_public_key, my_private_key = generate_keys()
their_public_key = None  # será preenchida com a chave pública do app A

@app.route('/receive', methods=['POST'])
def receive_message(): # endpoint que recebe dados do app A (chave pública ou mensagem)
    global their_public_key
    data = request.get_json()
    
    if data.get('public_key'):
        their_public_key = tuple(data['public_key'])
        print('[App B] 🔑 Chave pública recebida do App A:', their_public_key)
        return jsonify({'message': 'Chave recebida!'})

    ciphertext = data['message']
    message = decrypt(ciphertext, my_private_key)
    
    print(f'\n[App B] 📥 Mensagem recebida e descriptografada: {message}\n[App B] 💬 Digite a mensagem para enviar (ou "sair" para encerrar): ', end='', flush=True)
    
    sys.stdout.flush()

    return jsonify({'message': 'Recebido com sucesso!'})

# envia uma mensagem criptografada para o app A
def send_message(text):
    global their_public_key

    if their_public_key is None:
        print('[App B] ❌ Erro: chave pública do App A ainda não recebida.')
        return

    encrypted = encrypt(text, their_public_key)
    payload = {'message': encrypted}

    try:
        requests.post('http://localhost:5000/receive', json=payload)
        print(f'[App B] 📤 Mensagem enviada: {text}')
    except requests.exceptions.ConnectionError:
        print('[App B] ⚠️ Erro ao enviar mensagem: App A não disponível.')

# inicia o servidor flask do app B na porta 5001
# o app A já usa a porta 5000, então o App B precisa rodar em outra porta para evitar conflito
def run_flask():
    import logging

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # silencia os logs de requisição

    app.run(port=5001)

# realiza a troca inicial de chaves públicas entre app B e app A
def try_exchange_keys():
    global their_public_key
    payload = {'public_key': list(my_public_key)}

    # envia a chave uma única vez
    while True:
        try:
            requests.post('http://localhost:5000/receive', json=payload)
            print('[App B] 🔐 Chave pública enviada para App A. Aguardando chave pública do App A...')
            break
        except requests.exceptions.ConnectionError:
            print('[App B] App A ainda não disponível, tentando novamente...')
            time.sleep(1)

    # espera pela chave do outro app
    while their_public_key is None:
        time.sleep(0.5)

if __name__ == '__main__':
    print('[App B] 🟣 Iniciado.')
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    try_exchange_keys()

    while True:
        try:
            text = input('[App B] 💬 Digite a mensagem para enviar (ou "sair" para encerrar): ')
            if text.lower() == 'sair':
                print('[App B] 👋 Encerrando.')
                break
            send_message(text)
        except KeyboardInterrupt:
            print('\n[App B] 👋 Encerrando pelo teclado.')
            break
