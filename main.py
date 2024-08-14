from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_file, session, redirect, url_for
from analyze import generate_dashboard, create_analysis_response
import io
import os
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessário para armazenar dados na sessão

# Configuração da chave da API da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
   

# Rota para a página inicial com o formulário de upload
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.csv'):
            unique_filename = str(uuid.uuid4()) + '.csv'
            file.save(unique_filename)
            session['file_path'] = unique_filename
            return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'file_path' not in session:
        return redirect(url_for('index'))

    file_path = session['file_path']
    df = pd.read_csv(file_path)

    if request.method == 'POST':
        query = request.form.get('query')
        if not query:
            return "Por favor, insira uma consulta."

        # Gera o dashboard baseado na consulta
        dashboard_html = create_analysis_response(query, df)
        return render_template('dashboard.html', dashboard_html=dashboard_html)

    return render_template('dashboard.html')

# Rota para baixar o arquivo Excel processado
@app.route('/download', methods=['GET'])
def download_file():
    if 'dataframe' not in session or 'filename' not in session:
        return redirect(url_for('index'))

    df = pd.DataFrame(session['dataframe'])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name=session['filename'])

if __name__ == '__main__':
    app.run(debug=True)