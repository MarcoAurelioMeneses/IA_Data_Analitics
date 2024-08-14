from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_analysis_response(query, df):
    prompt = f"""
    Você é um assistente que ajuda a analisar dados de uma planilha. 
    Os dados da planilha são:
    {df.head().to_string()}
    
    Baseado nesses dados, {query}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ou "gpt-4"
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda a analisar dados de uma planilha."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )

    analysis_text = response.choices[0].message.content
    
    # Simule a criação de um DataFrame com base na análise
    # (Este é um exemplo; substitua com dados reais conforme necessário)
    analysis_df = pd.DataFrame({
        "Análise": [analysis_text]
    })
    
    # Salve o DataFrame na sessão
    return analysis_text, analysis_df