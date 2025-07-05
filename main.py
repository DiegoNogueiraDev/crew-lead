#!/usr/bin/env python3
"""
Sistema de Captura de Leads do Google Maps com CrewAI
Autor: Assistente IA
Data: 2024
"""

import sys
import argparse
from datetime import datetime
from config import Config
from crew.lead_capture_crew import LeadCaptureCrew
from utils.logger import setup_logger
from utils.database import init_database

def main():
    """Função principal do sistema de captura de leads"""
    
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description="Sistema de Captura de Leads do Google Maps")
    parser.add_argument("--termo", "-t", type=str, required=True, 
                       help="Termo de busca (ex: 'restaurante', 'dentista', 'oficina')")
    parser.add_argument("--localizacao", "-l", type=str, 
                       default=Config.DEFAULT_LOCATION,
                       help="Localização para busca (ex: 'São Paulo, SP')")
    parser.add_argument("--raio", "-r", type=int, 
                       default=Config.DEFAULT_SEARCH_RADIUS,
                       help="Raio de busca em metros")
    parser.add_argument("--max-resultados", "-m", type=int, 
                       default=Config.MAX_RESULTS_PER_SEARCH,
                       help="Número máximo de resultados")
    parser.add_argument("--arquivo-saida", "-o", type=str, 
                       default=f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                       help="Arquivo de saída para os leads")
    
    args = parser.parse_args()
    
    # Configurar logging
    logger = setup_logger()
    
    try:
        # Validar configurações
        Config.validate()
        logger.info("Configurações validadas com sucesso")
        
        # Inicializar banco de dados
        init_database()
        logger.info("Banco de dados inicializado")
        
        # Criar e executar crew
        crew = LeadCaptureCrew(
            search_term=args.termo,
            location=args.localizacao,
            radius=args.raio,
            max_results=args.max_resultados,
            output_file=args.arquivo_saida
        )
        
        logger.info(f"Iniciando captura de leads para: {args.termo}")
        logger.info(f"Localização: {args.localizacao}")
        logger.info(f"Raio: {args.raio}m")
        logger.info(f"Máximo de resultados: {args.max_resultados}")
        
        # Executar captura
        result = crew.kickoff()
        
        logger.info(f"Captura concluída! Resultados salvos em: {args.arquivo_saida}")
        print(f"\n✅ Captura de leads concluída com sucesso!")
        print(f"📊 Resultados salvos em: {args.arquivo_saida}")
        
    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
        print(f"❌ Erro de configuração: {e}")
        print("💡 Certifique-se de definir as variáveis de ambiente necessárias")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 