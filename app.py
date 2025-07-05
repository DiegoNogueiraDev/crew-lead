import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
from config import Config
from utils.database import LeadDatabase
from utils.logger import setup_logger

# Configurar página
st.set_page_config(
    page_title="Captura de Leads - Google Maps",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar logger
logger = setup_logger()

# Inicializar banco de dados
@st.cache_resource
def init_db():
    return LeadDatabase()

db = init_db()

def main():
    st.title("🎯 Sistema de Captura de Leads do Google Maps")
    st.markdown("### Powered by CrewAI")
    
    # Sidebar para configurações
    st.sidebar.header("⚙️ Configurações")
    
    # Verificar configurações
    with st.sidebar.expander("🔑 Status das APIs", expanded=True):
        openai_status = "✅ Configurada" if Config.OPENAI_API_KEY else "❌ Não configurada"
        gmaps_status = "✅ Configurada" if Config.GOOGLE_MAPS_API_KEY else "❌ Não configurada"
        
        st.write(f"**OpenAI API:** {openai_status}")
        st.write(f"**Google Maps API:** {gmaps_status}")
        
        if not Config.OPENAI_API_KEY or not Config.GOOGLE_MAPS_API_KEY:
            st.warning("⚠️ Configure as APIs nas variáveis de ambiente")
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Capturar Leads", "📊 Dashboard", "📋 Gerenciar Leads", "📈 Relatórios"])
    
    with tab1:
        capture_leads_tab()
    
    with tab2:
        dashboard_tab()
    
    with tab3:
        manage_leads_tab()
    
    with tab4:
        reports_tab()

def capture_leads_tab():
    st.header("🔍 Capturar Novos Leads")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parâmetros de Busca")
        
        search_term = st.text_input(
            "Termo de Busca",
            placeholder="Ex: restaurante, dentista, advogado",
            help="Digite o tipo de estabelecimento que você quer encontrar"
        )
        
        location = st.text_input(
            "Localização",
            value=Config.DEFAULT_LOCATION,
            placeholder="Ex: São Paulo, SP",
            help="Digite a cidade ou região para buscar"
        )
        
        col_radius, col_results = st.columns(2)
        
        with col_radius:
            radius = st.slider(
                "Raio (km)",
                min_value=1,
                max_value=50,
                value=10,
                help="Distância em quilômetros do ponto central"
            )
        
        with col_results:
            max_results = st.slider(
                "Máx. Resultados",
                min_value=10,
                max_value=200,
                value=50,
                help="Número máximo de leads para capturar"
            )
    
    with col2:
        st.subheader("Configurações Avançadas")
        
        export_format = st.selectbox(
            "Formato de Exportação",
            ["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"]
        )
        
        quality_filter = st.selectbox(
            "Filtro de Qualidade",
            ["Todos", "Apenas Alta Qualidade", "Alta e Média Qualidade"]
        )
        
        include_photos = st.checkbox("Incluir URLs de Fotos", value=False)
        include_reviews = st.checkbox("Incluir Avaliações Detalhadas", value=False)
        
        st.markdown("---")
        
        # Botão para iniciar captura
        if st.button("🚀 Iniciar Captura de Leads", type="primary", use_container_width=True):
            if not search_term:
                st.error("❌ Por favor, informe o termo de busca")
                return
            
            if not Config.OPENAI_API_KEY or not Config.GOOGLE_MAPS_API_KEY:
                st.error("❌ Configure as APIs antes de iniciar")
                return
            
            # Executar captura
            execute_lead_capture(search_term, location, radius * 1000, max_results, export_format)

def execute_lead_capture(search_term, location, radius, max_results, export_format):
    """Executa a captura de leads com feedback em tempo real"""
    
    # Criar containers para feedback
    status_container = st.container()
    progress_container = st.container()
    
    with status_container:
        st.info(f"🔍 Iniciando captura de leads para: **{search_term}** em **{location}**")
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
    try:
        # Simular processo de captura (substituir pela implementação real)
        import time
        
        # Etapa 1: Pesquisar no Google Maps
        status_text.text("🔍 Pesquisando estabelecimentos no Google Maps...")
        progress_bar.progress(25)
        time.sleep(2)
        
        # Etapa 2: Enriquecer dados
        status_text.text("🔍 Enriquecendo dados dos leads...")
        progress_bar.progress(50)
        time.sleep(2)
        
        # Etapa 3: Validar qualidade
        status_text.text("✅ Validando qualidade dos leads...")
        progress_bar.progress(75)
        time.sleep(2)
        
        # Etapa 4: Organizar e salvar
        status_text.text("💾 Organizando e salvando resultados...")
        progress_bar.progress(100)
        time.sleep(1)
        
        # Simular dados de resultado
        leads_encontrados = 45
        leads_qualificados = 32
        
        # Mostrar resultados
        st.success(f"✅ Captura concluída com sucesso!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Leads Encontrados", leads_encontrados)
        with col2:
            st.metric("⭐ Leads Qualificados", leads_qualificados)
        with col3:
            st.metric("📈 Taxa de Qualificação", f"{(leads_qualificados/leads_encontrados)*100:.1f}%")
        
        # Botão para download
        filename = f"leads_{search_term}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        st.download_button(
            label="📥 Baixar Arquivo de Leads",
            data=b"dados_simulados",  # Substituir pelos dados reais
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"❌ Erro durante a captura: {str(e)}")
        logger.error(f"Erro na captura de leads: {e}")

def dashboard_tab():
    st.header("📊 Dashboard de Leads")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    # Dados simulados (substituir por dados reais do banco)
    total_leads = 1234
    leads_mes = 156
    taxa_conversao = 12.5
    campanhas_ativas = 8
    
    with col1:
        st.metric("📊 Total de Leads", total_leads, delta="+23")
    
    with col2:
        st.metric("📈 Leads este Mês", leads_mes, delta="+15")
    
    with col3:
        st.metric("💰 Taxa de Conversão", f"{taxa_conversao}%", delta="+2.3%")
    
    with col4:
        st.metric("🎯 Campanhas Ativas", campanhas_ativas, delta="+2")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Leads por Mês")
        
        # Dados simulados
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        leads_count = [45, 78, 92, 134, 156, 98]
        
        fig_line = px.line(
            x=months, 
            y=leads_count, 
            title="Evolução Mensal de Leads",
            labels={'x': 'Mês', 'y': 'Número de Leads'}
        )
        fig_line.update_traces(line_color='#ff6b6b')
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Leads por Categoria")
        
        # Dados simulados
        categories = ['Restaurantes', 'Clínicas', 'Advogados', 'Lojas', 'Serviços']
        counts = [234, 187, 156, 143, 98]
        
        fig_pie = px.pie(
            values=counts,
            names=categories,
            title="Distribuição por Categoria"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Mapa de calor (simulado)
    st.subheader("🗺️ Distribuição Geográfica")
    
    # Dados simulados de localização
    import numpy as np
    
    # Simular coordenadas em São Paulo
    lat = np.random.normal(-23.5505, 0.1, 100)
    lon = np.random.normal(-46.6333, 0.1, 100)
    
    df_map = pd.DataFrame({
        'lat': lat,
        'lon': lon,
        'leads': np.random.randint(1, 10, 100)
    })
    
    st.map(df_map)

def manage_leads_tab():
    st.header("📋 Gerenciar Leads")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_category = st.selectbox(
            "Filtrar por Categoria",
            ["Todos", "Restaurantes", "Clínicas", "Advogados", "Lojas", "Serviços"]
        )
    
    with col2:
        filter_quality = st.selectbox(
            "Filtrar por Qualidade",
            ["Todos", "Alta", "Média", "Baixa"]
        )
    
    with col3:
        filter_status = st.selectbox(
            "Status do Lead",
            ["Todos", "Novo", "Contatado", "Qualificado", "Convertido"]
        )
    
    # Dados simulados de leads
    leads_data = {
        'Nome': ['Restaurante Silva', 'Clínica Dr. João', 'Advocacia Lima', 'Loja da Maria', 'Serviços Tech'],
        'Categoria': ['Restaurantes', 'Clínicas', 'Advogados', 'Lojas', 'Serviços'],
        'Telefone': ['(11) 99999-1111', '(11) 99999-2222', '(11) 99999-3333', '(11) 99999-4444', '(11) 99999-5555'],
        'Email': ['contato@silva.com', 'clinica@drjoao.com', 'adv@lima.com', 'loja@maria.com', 'tech@services.com'],
        'Avaliação': [4.5, 4.8, 4.2, 4.0, 4.7],
        'Qualidade': ['Alta', 'Alta', 'Média', 'Média', 'Alta'],
        'Status': ['Novo', 'Contatado', 'Qualificado', 'Novo', 'Convertido']
    }
    
    df_leads = pd.DataFrame(leads_data)
    
    # Aplicar filtros
    if filter_category != "Todos":
        df_leads = df_leads[df_leads['Categoria'] == filter_category]
    
    if filter_quality != "Todos":
        df_leads = df_leads[df_leads['Qualidade'] == filter_quality]
    
    if filter_status != "Todos":
        df_leads = df_leads[df_leads['Status'] == filter_status]
    
    # Mostrar tabela
    st.subheader(f"📊 {len(df_leads)} leads encontrados")
    
    # Configurar editor de dados
    edited_df = st.data_editor(
        df_leads,
        column_config={
            "Avaliação": st.column_config.NumberColumn(
                "Avaliação",
                help="Avaliação no Google Maps",
                min_value=0,
                max_value=5,
                step=0.1,
                format="%.1f ⭐"
            ),
            "Status": st.column_config.SelectboxColumn(
                "Status",
                help="Status do lead",
                options=["Novo", "Contatado", "Qualificado", "Convertido"],
                required=True
            ),
            "Qualidade": st.column_config.SelectboxColumn(
                "Qualidade",
                help="Qualidade do lead",
                options=["Alta", "Média", "Baixa"],
                required=True
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Salvar Alterações", type="primary"):
            st.success("✅ Alterações salvas com sucesso!")
    
    with col2:
        if st.button("📤 Exportar Selecionados"):
            csv = edited_df.to_csv(index=False)
            st.download_button(
                label="📥 Baixar CSV",
                data=csv,
                file_name=f"leads_exportados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🗑️ Remover Selecionados"):
            st.warning("⚠️ Funcionalidade em desenvolvimento")

def reports_tab():
    st.header("📈 Relatórios e Análises")
    
    # Seletor de período
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Data Inicial", value=datetime.now().replace(day=1))
    
    with col2:
        end_date = st.date_input("Data Final", value=datetime.now())
    
    # Relatório de performance
    st.subheader("📊 Relatório de Performance")
    
    # Dados simulados
    performance_data = {
        'Métrica': ['Leads Capturados', 'Leads Qualificados', 'Taxa de Conversão', 'Custo por Lead'],
        'Valor': [1234, 892, '12.5%', 'R$ 3.45'],
        'Meta': [1000, 800, '15%', 'R$ 5.00'],
        'Status': ['✅ Superou', '✅ Superou', '❌ Abaixo', '✅ Superou']
    }
    
    df_performance = pd.DataFrame(performance_data)
    st.dataframe(df_performance, use_container_width=True)
    
    # Gráfico de comparação
    st.subheader("📈 Comparação de Campanhas")
    
    campanhas = ['Restaurantes SP', 'Clínicas RJ', 'Advogados BH', 'Lojas POA', 'Serviços BSB']
    leads_gerados = [234, 187, 156, 143, 98]
    conversoes = [29, 23, 19, 18, 12]
    
    fig_compare = go.Figure()
    
    fig_compare.add_trace(go.Bar(
        name='Leads Gerados',
        x=campanhas,
        y=leads_gerados,
        marker_color='lightblue'
    ))
    
    fig_compare.add_trace(go.Bar(
        name='Conversões',
        x=campanhas,
        y=conversoes,
        marker_color='orange'
    ))
    
    fig_compare.update_layout(
        title='Comparação de Performance por Campanha',
        xaxis_title='Campanhas',
        yaxis_title='Quantidade',
        barmode='group'
    )
    
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # Relatório detalhado
    st.subheader("📋 Relatório Detalhado")
    
    if st.button("📄 Gerar Relatório Completo", type="primary"):
        # Simular geração de relatório
        with st.spinner("Gerando relatório..."):
            import time
            time.sleep(2)
        
        st.success("✅ Relatório gerado com sucesso!")
        
        # Botão para download
        st.download_button(
            label="📥 Baixar Relatório PDF",
            data=b"relatorio_simulado",
            file_name=f"relatorio_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main() 