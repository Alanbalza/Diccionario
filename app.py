from flask import Flask, request, render_template, redirect, url_for, jsonify
import re

app = Flask(__name__)

synonyms = {
    'rápido': ['veloz'],
    'feliz': ['contento'],
    'triste': ['melancólico'],
    'enojado': ['molesto'],
    'hermoso': ['bello'],
    'inteligente': ['listo'],
    'fuerte': ['robusto'],
    'débil': ['frágil'],
    'grande': ['enorme'],
    'pequeño': ['chico'],
    'rico': ['millonario'],
    'pobre': ['necesitado'],
    'caliente': ['ardiente'],
    'frío': ['helado'],
    'viejo': ['anciano'],
    'joven': ['adolescente'],
    'difícil': ['complicado'],
    'fácil': ['sencillo'],
    'limpio': ['higiénico'],
    'sucio': ['mugriento']
}

def analyze_code(code):
    tokens = []
    lines = code.split('\n')
    
    for line_number, line in enumerate(lines, start=1):
        words = re.findall(r'\w+|[^\s\w]', line) 
        for word in words:
            token = {
                'value': word,
                'sinónimo': '',
                'símbolo': '',
                'dígito': '',
                'línea': line_number,
                'ERROR': ''
            }

            found = False

            
            for key, synonyms_list in synonyms.items():
                if word == key or word in synonyms_list:
                    token['sinónimo'] = key
                    found = True
                    break

            if re.search(r'[\[\]{}()=+\-*/%,;.]', word):
                token['símbolo'] = 'X'
                found = True

            if re.search(r'\d', word):
                token['dígito'] = 'X'
                found = True

            if not found:
                token['ERROR'] = 'X'
            
            tokens.append(token)
    
    return tokens

@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code')
    
    if not code:
        return jsonify({"error": "Por favor, ingrese texto para analizar"}), 400
    
    results = analyze_code(code)
    return render_template('index.html', results=results, code=code)

@app.route('/clear_results', methods=['POST'])
def clear_results():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
