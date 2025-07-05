from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from agents.lead_agents import LeadAgents
from tasks.lead_tasks import LeadTasks
from tools.google_maps_tool import GoogleMapsSearchTool
from tools.data_enrichment_tool import DataEnrichmentTool
from config import Config
from utils.database import LeadDatabase
from utils.logger import setup_logger

@CrewBase
class LeadCaptureCrew:
    """Crew para captura de leads do Google Maps"""
    
    def __init__(self, search_term: str, location: str, radius: int, max_results: int, output_file: str):
        self.search_term = search_term
        self.location = location
        self.radius = radius
        self.max_results = max_results
        self.output_file = output_file
        self.database = LeadDatabase()
        self.logger = setup_logger()
        
        # Configurar LLM
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.1,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        # Inicializar ferramentas
        self.google_maps_tool = GoogleMapsSearchTool()
        self.data_enrichment_tool = DataEnrichmentTool()
        
        # Inicializar agentes e tarefas
        self.lead_agents = LeadAgents(self.llm)
        self.lead_tasks = LeadTasks()
    
    @agent
    def pesquisador_leads(self) -> Agent:
        """Agente responsável por pesquisar leads no Google Maps"""
        return self.lead_agents.pesquisador_leads()
    
    @agent
    def enriquecedor_dados(self) -> Agent:
        """Agente responsável por enriquecer os dados dos leads"""
        return self.lead_agents.enriquecedor_dados()
    
    @agent
    def validador_qualidade(self) -> Agent:
        """Agente responsável por validar a qualidade dos leads"""
        return self.lead_agents.validador_qualidade()
    
    @agent
    def organizador_resultados(self) -> Agent:
        """Agente responsável por organizar e formatar os resultados"""
        return self.lead_agents.organizador_resultados()
    
    @task
    def pesquisar_leads_task(self) -> Task:
        """Tarefa para pesquisar leads no Google Maps"""
        return self.lead_tasks.pesquisar_leads_task(
            search_term=self.search_term,
            location=self.location,
            radius=self.radius,
            max_results=self.max_results
        )
    
    @task
    def enriquecer_dados_task(self) -> Task:
        """Tarefa para enriquecer dados dos leads"""
        return self.lead_tasks.enriquecer_dados_task()
    
    @task
    def validar_qualidade_task(self) -> Task:
        """Tarefa para validar qualidade dos leads"""
        return self.lead_tasks.validar_qualidade_task()
    
    @task
    def organizar_resultados_task(self) -> Task:
        """Tarefa para organizar e salvar resultados"""
        return self.lead_tasks.organizar_resultados_task(
            output_file=self.output_file
        )
    
    @crew
    def crew(self) -> Crew:
        """Configuração do crew"""
        return Crew(
            agents=[
                self.pesquisador_leads(),
                self.enriquecedor_dados(),
                self.validador_qualidade(),
                self.organizador_resultados()
            ],
            tasks=[
                self.pesquisar_leads_task(),
                self.enriquecer_dados_task(),
                self.validar_qualidade_task(),
                self.organizar_resultados_task()
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,
            max_rpm=10,
            share_crew=False
        )
    
    def kickoff(self):
        """Executa o crew de captura de leads"""
        self.logger.info("Iniciando execução do crew de captura de leads")
        
        # Executar crew
        result = self.crew().kickoff(inputs={
            'search_term': self.search_term,
            'location': self.location,
            'radius': self.radius,
            'max_results': self.max_results,
            'output_file': self.output_file
        })
        
        self.logger.info("Execução do crew concluída")
        return result 