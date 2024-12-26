import streamlit as st
import pandas as pd
from datetime import date, datetime
from collections import Counter
import plotly.express as px

# Funções para gerenciamento de projetos
def obter_projetos():
    return st.session_state['projetos']

def obter_estatisticas_projetos():
    projetos = st.session_state['projetos']
    status_list = [p['status'] for p in projetos]
    contagem = Counter(status_list)
    estatisticas = list(contagem.items())
    return estatisticas

def calcular_progresso(data_inicio, data_fim):
    hoje = date.today()
    if data_inicio and data_fim:
        total_dias = (data_fim - data_inicio).days
        dias_passados = (hoje - data_inicio).days
        if total_dias > 0:
            progresso = max(0, min(100, int((dias_passados / total_dias) * 100)))
        else:
            progresso = 100
    else:
        progresso = 0
    return progresso

def get_status_badge(status):
    status_dict = {
        'Parado': '🔴 Parado',
        'Em Andamento': '🟢 Em Andamento',
        'Concluído': '✅ Concluído',
        'A definir': '❓ A definir'
    }
    return status_dict.get(status, status)

# Carregar projetos fixos
def carregar_projetos_iniciais():
    return [
        {"nome": "Portal de BI", "descricao": "Criando os usuários e configurando a integração dos BIs para cada usuário", "status": "Em Andamento", "Prioridade": "Alta Prioridade" ,"data_inicio": datetime.strptime("2024-12-19", "%Y-%m-%d").date(), "data_fim": datetime.strptime("2025-01-01", "%Y-%m-%d").date()},
        {"nome": "BI Abastecimento (Base TOTVs)", "descricao": "Em validação com Time de Abastecimento", "status": "Em Andamento", "Prioridade": "Alta Prioridade", "data_inicio": datetime.strptime("2023-10-10", "%Y-%m-%d").date(), "data_fim": datetime.strptime("2025-01-06", "%Y-%m-%d").date()},
        {"nome": "BI de Controladoria", "descricao": "Concluido, a ser integrado no portal por gestor", "status": "Em Andamento", "Prioridade": "Média Prioridade","data_inicio": datetime.strptime("2023-11-01", "%Y-%m-%d").date(), "data_fim": datetime.strptime("2025-01-03", "%Y-%m-%d").date()},
        {"nome": "BI Contas a Pagar", "descricao": "Em desenvolvimento/ajuste de valores", "status": "Em Andamento", "Prioridade": "Média Prioridade" ,"data_inicio": datetime.strptime("2023-12-01", "%Y-%m-%d").date(), "data_fim": datetime.strptime("2025-01-03", "%Y-%m-%d").date()},
        {"nome": "BI de Pátio", "descricao": "Em desenvolvimento com time do Raul da GR", "status": "Em Andamento", "Prioridade": "Média Prioridade", "data_inicio": None, "data_fim": None},
        {"nome": "BI Recursos Humanos", "descricao": "Validado, pronto para fazer a aba por gestor", "status": "A definir", "Prioridade": "Indefinido", "data_inicio": None, "data_fim": None},
        {"nome": "BI Fiscal/Contábil", "descricao": "Chamado aberto, a definir prazos", "status": "A definir", "Prioridade": "Indefinido", "data_inicio": None, "data_fim": None},
        {"nome": "BI de Odômetro", "descricao": "Entregue e funcionando", "status": "Concluído", "Prioridade": None, "data_inicio": None, "data_fim": None},
        {"nome": "BI Suprimentos", "descricao": "Realizando ajustes pendentes e alinhamento", "status": "Concluído", "Prioridade": None, "data_inicio": None, "data_fim": None},
        {"nome": "BI de Faturamento", "descricao": "Corrigido e funcionando", "status": "Concluído", "Prioridade": None, "data_inicio": None, "data_fim": None},
        {"nome": "BI de Abastecimento (Base Excel)", "descricao": "Entregue ao time de Abastecimento", "status": "Concluído", "Prioridade": None, "data_inicio": None, "data_fim": None},
        {"nome": "BI WTMH (Thompson)", "descricao": "Entregue e funcionando", "status": "Concluído", "Prioridade": None, "data_inicio": None, "data_fim": None},
        {"nome": "BI de Manutenção", "descricao": "Ficou combinado do Dante vir para Limeira alinhar com Claudelei as necessidades da equipe de manutenção e sentar com nós para discutirmos sobre quais dados eles precisam", "status": "Parado", "Prioridade": None, "data_inicio": None, "data_fim": None},
        {"nome": "BI Estoque", "descricao": "Parado", "status": "Parado", "Prioridade": None, "data_inicio": None, "data_fim": None},
        {"nome": "BI de Agregado", "descricao": "Parado", "status": "Parado", "Prioridade": None, "data_inicio": None, "data_fim": None},
    ]

# Interface do usuário
def main():
    st.title('Gerenciamento de Projetos de BI')

    if 'projetos' not in st.session_state:
        st.session_state['projetos'] = carregar_projetos_iniciais()

    if 'app_page' not in st.session_state:
        st.session_state['app_page'] = 'visao_geral'

    aplicativo()

def aplicativo():
    st.subheader('Bem-vindo ao Sistema de Gerenciamento de Projetos')

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button('Visão Geral', key='visao_geral_button'):
            st.session_state.app_page = 'visao_geral'
    with col3:
        if st.button('Relatórios', key='relatorios_button'):
            st.session_state.app_page = 'relatorios'

    if st.session_state.app_page == 'visao_geral':
        visao_geral()
    elif st.session_state.app_page == 'relatorios':
        relatorios()

def visao_geral():
    st.subheader('Lista de Projetos')

    projetos_lista = obter_projetos()
    if projetos_lista:
        df = pd.DataFrame(projetos_lista)
        df['Progresso (%)'] = df.apply(lambda row: calcular_progresso(row.get('data_inicio'), row.get('data_fim')), axis=1)
        df['data_inicio_str'] = df['data_inicio'].apply(lambda x: x.strftime('%d/%m/%Y') if x else 'Indefinido')
        df['data_fim_str'] = df['data_fim'].apply(lambda x: x.strftime('%d/%m/%Y') if x else 'Indefinido')
        df['Status'] = df['status'].apply(get_status_badge)

        df_display = df[['nome', 'descricao', 'Status', 'Prioridade', 'data_inicio_str', 'data_fim_str', 'Progresso (%)']].copy()
        df_display.rename(columns={
            'nome': 'Projeto',
            'descricao': 'Descrição',
            'data_inicio_str': 'Data Início',
            'data_fim_str': 'Data Fim',
        }, inplace=True)

        st.table(df_display)

        st.write("### Cronograma dos Projetos")
        fig = px.timeline(
            df,
            x_start="data_inicio",
            x_end="data_fim",
            y="nome",
            color="status",
            title="Cronograma dos Projetos",
            labels={"nome": "Projeto", "status": "Status"}
        )
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info('Nenhum projeto cadastrado.')

def relatorios():
    st.subheader('Relatórios e Análises')
    estatisticas = obter_estatisticas_projetos()
    if estatisticas:
        df_estatisticas = pd.DataFrame(estatisticas, columns=['Status', 'Quantidade'])
        df_estatisticas['Status'] = df_estatisticas['Status'].apply(get_status_badge)

        st.write("### Contagem de Projetos por Status")
        fig_bar = px.bar(
            df_estatisticas,
            x='Status',
            y='Quantidade',
            title='Contagem de Projetos por Status',
            labels={'Quantidade': 'Número de Projetos'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Nenhum projeto cadastrado para gerar relatórios.")

if __name__ == '__main__':
    main()
