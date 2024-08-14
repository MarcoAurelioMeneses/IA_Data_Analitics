from openai import OpenAI
import pandas as pd
import seaborn as sns
import io
import base64
import os
from dotenv import load_dotenv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that helps analyze data from a spreadsheet."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message

def generate_dashboard(df, analysis_type):
    plt.figure(figsize=(10, 6))
    
    if analysis_type == "school_distribution":
        sns.countplot(x="Vinculação da Escola", data=df)
        plt.title("Distribuição das Escolas por CREDE")
    
    # Salva o gráfico como imagem em base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return f'<img src="data:image/png;base64,{plot_url}" />'

def create_analysis_response(query, df):
    analysis_prompt = f"O usuário pediu o seguinte: {query}. Baseado na planilha fornecida, que tipo de análise você sugeriria?"
    analysis_type = ask_openai(analysis_prompt)
    
    dashboard_html = generate_dashboard(df, analysis_type)
    return dashboard_html