from flask import Flask, render_template, request, jsonify
import crypto_utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.json
        text = data.get('text')
        key = data.get('key')
        algo = data.get('algo')
        
        if not text or not key:
            return jsonify({'error': 'Text and Key are required'}), 400
            
        result = ""
        if algo == "AES":
            result = crypto_utils.aes_encrypt(text, key)
        elif algo == "TripleDES":
            result = crypto_utils.triple_des_encrypt(text, key)
        elif algo == "DES":
            result = crypto_utils.des_encrypt(text, key)
        else:
            return jsonify({'error': 'Unsupported algorithm'}), 400
            
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.json
        ciphertext = data.get('text')
        key = data.get('key')
        algo = data.get('algo')
        
        if not ciphertext or not key:
            return jsonify({'error': 'Ciphertext and Key are required'}), 400
            
        result = ""
        if algo == "AES":
            result = crypto_utils.aes_decrypt(ciphertext, key)
        elif algo == "TripleDES":
            result = crypto_utils.triple_des_decrypt(ciphertext, key)
        elif algo == "DES":
            result = crypto_utils.des_decrypt(ciphertext, key)
        else:
            return jsonify({'error': 'Unsupported algorithm'}), 400
            
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': 'Decryption failed. Check your key and data.'}), 500

if __name__ == '__main__':
    print("Server starting at http://127.0.0.1:5000")
    app.run(debug=True)
