from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.google_maps_tool import GoogleMapsSearchTool
from tools.data_enrichment_tool import DataEnrichmentTool

class LeadAgents:
    """Classe que define os agentes para captura de leads"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.google_maps_tool = GoogleMapsSearchTool()
        self.data_enrichment_tool = DataEnrichmentTool()
    
    def pesquisador_leads(self) -> Agent:
        """Agente especializado em pesquisar leads no Google Maps"""
        return Agent(
            role='Pesquisador de Leads',
            goal='Encontrar leads qualificados no Google Maps usando os critérios especificados',
            backstory="""Você é um especialista em pesquisa de leads com experiência em encontrar 
                        empresas e profissionais relevantes no Google Maps. Você sabe como usar 
                        diferentes termos de busca e filtros para encontrar os melhores prospects 
                        para campanhas de marketing.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.google_maps_tool.search_businesses],
            max_iter=5,
            max_execution_time=300
        )
    
    def enriquecedor_dados(self) -> Agent:
        """Agente especializado em enriquecer dados dos leads"""
        return Agent(
            role='Enriquecedor de Dados',
            goal='Enriquecer os dados dos leads com informações adicionais e de contato',
            backstory="""Você é um especialista em enriquecimento de dados que sabe como encontrar 
                        informações adicionais sobre empresas, incluindo emails, telefones, 
                        redes sociais e outros dados de contato relevantes. Você é meticuloso 
                        e sempre verifica a qualidade das informações.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.data_enrichment_tool.enrich_contact_info],
            max_iter=3,
            max_execution_time=180
        )
    
    def validador_qualidade(self) -> Agent:
        """Agente especializado em validar a qualidade dos leads"""
        return Agent(
            role='Validador de Qualidade',
            goal='Validar e filtrar leads com base em critérios de qualidade e relevância',
            backstory="""Você é um especialista em qualificação de leads com experiência em 
                        identificar prospects de alta qualidade. Você sabe avaliar a relevância 
                        de um lead, a qualidade das informações de contato e o potencial de 
                        conversão baseado em diversos critérios.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            max_iter=2,
            max_execution_time=120
        )
    
    def organizador_resultados(self) -> Agent:
        """Agente especializado em organizar e formatar resultados"""
        return Agent(
            role='Organizador de Resultados',
            goal='Organizar, formatar e exportar os leads capturados em formato adequado',
            backstory="""Você é um especialista em organização de dados que sabe como estruturar 
                        informações de leads de forma clara e útil. Você é responsável por 
                        formatar os dados, criar relatórios e exportar os resultados em 
                        diferentes formatos conforme necessário.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            max_iter=2,
            max_execution_time=90
        ) 