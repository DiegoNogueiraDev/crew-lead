#!/usr/bin/env python3
"""
Teste básico do sistema de captura de leads
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Testa se todas as importações estão funcionando"""
    print("🧪 Testando importações...")
    
    try:
        from crew.lead_capture_crew import LeadCaptureCrew
        print("✅ LeadCaptureCrew importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar LeadCaptureCrew: {e}")
        return False
    
    try:
        from tools.google_maps_tool import GoogleMapsSearchTool
        print("✅ GoogleMapsSearchTool importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar GoogleMapsSearchTool: {e}")
        return False
    
    try:
        from utils.database import LeadDatabase
        print("✅ LeadDatabase importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar LeadDatabase: {e}")
        return False
    
    try:
        from config import Config
        print("✅ Config importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar Config: {e}")
        return False
    
    return True

def test_database():
    """Testa a criação do banco de dados"""
    print("\n🧪 Testando banco de dados...")
    
    try:
        from utils.database import LeadDatabase
        
        # Usar banco de teste
        db = LeadDatabase("test_leads.db")
        
        # Testar inserção de lead de exemplo
        lead_exemplo = {
            'nome': 'Empresa Teste',
            'endereco': 'Rua Teste, 123',
            'telefone': '(11) 99999-9999',
            'email': 'teste@empresa.com',
            'categoria': 'Restaurante',
            'avaliacao': 4.5,
            'numero_avaliacoes': 100
        }
        
        lead_id = db.save_lead(lead_exemplo)
        print(f"✅ Lead de teste salvo com ID: {lead_id}")
        
        # Testar recuperação
        leads = db.get_leads(limit=1)
        if leads:
            print(f"✅ Lead recuperado: {leads[0]['nome']}")
        
        # Limpar banco de teste
        os.remove("test_leads.db")
        print("✅ Banco de dados testado com sucesso")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do banco: {e}")
        return False

def test_config():
    """Testa a configuração"""
    print("\n🧪 Testando configuração...")
    
    try:
        from config import Config
        
        print(f"📊 Modo headless: {Config.HEADLESS_MODE}")
        print(f"⏱️ Delay de busca: {Config.SEARCH_DELAY}s")
        print(f"📈 Máximo de resultados: {Config.MAX_RESULTS_PER_SEARCH}")
        
        # Verificar se as chaves estão configuradas
        if Config.OPENAI_API_KEY:
            print("✅ OpenAI API Key configurada")
        else:
            print("⚠️ OpenAI API Key não configurada (necessária para agentes)")
        
        if Config.GOOGLE_MAPS_API_KEY:
            print("✅ Google Maps API Key configurada")
        else:
            print("⚠️ Google Maps API Key não configurada (usará web scraping)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de configuração: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes do sistema...")
    print("=" * 50)
    
    testes_passaram = []
    
    testes_passaram.append(test_imports())
    testes_passaram.append(test_database())
    testes_passaram.append(test_config())
    
    print("\n" + "=" * 50)
    if all(testes_passaram):
        print("🎉 Todos os testes passaram! Sistema pronto para uso.")
        print("\n📋 Próximos passos:")
        print("1. Configure as chaves de API no arquivo .env")
        print("2. Execute: python main.py --termo 'restaurante' --localizacao 'São Paulo, SP'")
        print("3. Ou use: streamlit run app.py")
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main() 