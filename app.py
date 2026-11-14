from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados simulado em memória (ou para plugar no seu arquivo de persistência)
leads = [
    {
        "id": 1,
        "nome": "Farmácia Iguaçu",
        "segmento": "Tributário / Fiscal",
        "contato": "Responsável / Gestor",
        "telefone": "5541999999999", # Substituir pelo número real capturado
        "status": "Diagnóstico Gratuito Oferecido"
    },
    {
        "id": 2,
        "nome": "Supermercado Filial 1",
        "segmento": "Tributário / Varejo",
        "contato": "Gerente",
        "telefone": "5541988888888",
        "status": "Pipeline Aberto"
    },
    {
        "id": 3,
        "nome": "Associação do Pastor",
        "segmento": "Terceiro Setor",
        "contato": "Pastor",
        "telefone": "5541977777777",
        "status": "Contatos de Gestão Mapeados"
    }
]

@app.route('/')
def index():
    return render_template('index.html', leads=leads)

# Rota para gerar o link direto do WhatsApp com mensagem personalizada baseada no pilar
@app.route('/whatsapp/<int:lead_id>')
def abrir_whatsapp(lead_id):
    lead = next((l for l in leads if l['id'] == lead_id), None)
    if not lead:
        return "Lead não encontrado", 404
    
    # Mensagem customizada dependendo do pilar
    if "Tributário" in lead['segmento']:
        texto = f"Olá, {lead['contato']}, tudo bem? Aqui é o Marcelo da KRONUS. Passando para alinharmos aquele diagnóstico fiscal gratuito para otimização de PIS/COFINS na {lead['nome']}."
    else:
        texto = f"Olá, pastor, tudo bem? Aqui é o Marcelo da KRONUS. Retomando nosso papo sobre a estruturação e gestão da associação."
    
    url_wa = f"https://wa.me/{lead['telefone']}?text={texto.replace(' ', '%20')}"
    return redirect(url_wa)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
