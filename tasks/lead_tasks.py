from crewai import Task
from agents.lead_agents import LeadAgents
from tools.google_maps_tool import GoogleMapsSearchTool
from tools.data_enrichment_tool import DataEnrichmentTool

class LeadTasks:
    """Classe que define as tarefas para captura de leads"""
    
    def pesquisar_leads_task(self, search_term: str, location: str, radius: int, max_results: int) -> Task:
        """Tarefa para pesquisar leads no Google Maps"""
        return Task(
            description=f"""
            Pesquise leads no Google Maps usando os seguintes critérios:
            - Termo de busca: {search_term}
            - Localização: {location}
            - Raio: {radius} metros
            - Máximo de resultados: {max_results}
            
            Para cada lead encontrado, colete as seguintes informações:
            1. Nome do estabelecimento/empresa
            2. Endereço completo
            3. Telefone (se disponível)
            4. Website (se disponível)
            5. Categoria/tipo de negócio
            6. Avaliação e número de avaliações
            7. Horário de funcionamento
            8. Coordenadas (latitude e longitude)
            9. Fotos (URLs se disponíveis)
            
            Organize os resultados em uma lista estruturada com todos os dados coletados.
            """,
            agent=None,  # Será definido pelo crew
            expected_output="Lista de leads encontrados com todas as informações coletadas em formato JSON",
            tools=[GoogleMapsSearchTool()],
            output_file="leads_encontrados.json"
        )
    
    def enriquecer_dados_task(self) -> Task:
        """Tarefa para enriquecer dados dos leads"""
        return Task(
            description="""
            Enriqueça os dados dos leads encontrados na tarefa anterior com informações adicionais:
            
            1. Procure por informações de contato adicionais:
               - Email corporativo
               - Redes sociais (LinkedIn, Facebook, Instagram)
               - Outras formas de contato
            
            2. Colete informações adicionais sobre a empresa:
               - Descrição do negócio
               - Número de funcionários (estimativa)
               - Ano de fundação (se disponível)
               - Especialidades ou serviços oferecidos
            
            3. Verifique a qualidade e atualização das informações:
               - Confirme se o telefone está ativo
               - Verifique se o website está funcionando
               - Valide o endereço
            
            Para cada lead, adicione as informações encontradas mantendo a estrutura original.
            """,
            agent=None,  # Será definido pelo crew
            expected_output="Lista de leads enriquecidos com informações adicionais em formato JSON",
            tools=[DataEnrichmentTool()],
            output_file="leads_enriquecidos.json"
        )
    
    def validar_qualidade_task(self) -> Task:
        """Tarefa para validar a qualidade dos leads"""
        return Task(
            description="""
            Valide e classifique a qualidade dos leads enriquecidos:
            
            1. Critérios de qualidade:
               - Informações de contato completas (telefone, email, website)
               - Endereço completo e válido
               - Negócio ativo (avaliações recentes, website funcionando)
               - Relevância para o termo de busca
            
            2. Classificação de qualidade:
               - ALTA: Todas as informações disponíveis e verificadas
               - MÉDIA: Maioria das informações disponíveis
               - BAIXA: Poucas informações ou dados desatualizados
            
            3. Filtros de qualidade:
               - Remova leads duplicados
               - Exclua leads com informações incompletas demais
               - Marque leads suspeitos ou inativos
            
            4. Adicione score de qualidade (1-10) para cada lead
            
            Retorne apenas leads com qualidade MÉDIA ou ALTA.
            """,
            agent=None,  # Será definido pelo crew
            expected_output="Lista de leads validados e classificados por qualidade em formato JSON",
            output_file="leads_validados.json"
        )
    
    def organizar_resultados_task(self, output_file: str) -> Task:
        """Tarefa para organizar e exportar resultados"""
        return Task(
            description=f"""
            Organize e exporte os leads validados no formato final:
            
            1. Estruture os dados em formato tabular com as colunas:
               - Nome
               - Endereço
               - Telefone
               - Email
               - Website
               - Categoria
               - Avaliação
               - Número de Avaliações
               - Horário de Funcionamento
               - Latitude
               - Longitude
               - Score de Qualidade
               - Classificação de Qualidade
               - Observações
               - Data de Captura
            
            2. Ordene os leads por score de qualidade (maior para menor)
            
            3. Adicione estatísticas do resultado:
               - Total de leads encontrados
               - Leads por classificação de qualidade
               - Leads por categoria
               - Cobertura geográfica
            
            4. Exporte os dados em formato Excel ({output_file})
            
            5. Crie um resumo executivo com os principais insights
            """,
            agent=None,  # Será definido pelo crew
            expected_output=f"Arquivo Excel com leads organizados e resumo executivo salvo como {output_file}",
            output_file=output_file
        ) 