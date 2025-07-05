#!/usr/bin/env python3
"""
Teste de configuração do OpenRouter
"""

import os
import sys
from dotenv import load_dotenv
from config import Config

def test_openrouter_config():
    """Testa a configuração do OpenRouter"""
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    print("🔍 Testando configuração do OpenRouter...")
    
    # Verificar se as variáveis estão configuradas
    if not Config.OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY não está configurada")
        return False
    
    if not Config.OPENROUTER_API_KEY.startswith('sk-or-'):
        print("❌ OPENROUTER_API_KEY deve começar com 'sk-or-'")
        return False
    
    if not Config.OPENROUTER_BASE_URL:
        print("❌ OPENROUTER_BASE_URL não está configurada")
        return False
    
    if not Config.OPENROUTER_MODEL:
        print("❌ OPENROUTER_MODEL não está configurada")
        return False
    
    print("✅ Configuração básica do OpenRouter OK")
    return True

def test_openrouter_connection():
    """Testa conexão com OpenRouter"""
    
    try:
        from langchain_openai import ChatOpenAI
        from pydantic import SecretStr
        
        # Configurar LLM
        llm = ChatOpenAI(
            model=Config.OPENROUTER_MODEL,
            temperature=0.1,
            api_key=SecretStr(Config.OPENROUTER_API_KEY),
            base_url=Config.OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": Config.OPENROUTER_SITE_URL,
                "X-Title": Config.OPENROUTER_SITE_NAME,
            }
        )
        
        print("✅ Inicialização do LLM OpenRouter OK")
        
        # Teste básico de conectividade
        response = llm.invoke("Diga apenas 'OK' se você pode me ouvir")
        print(f"✅ Resposta do OpenRouter: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com OpenRouter: {e}")
        return False

def test_crew_integration():
    """Testa integração com CrewAI"""
    
    try:
        from crew.lead_capture_crew import LeadCaptureCrew
        
        # Criar uma instância do crew para testar
        crew = LeadCaptureCrew(
            search_term="teste",
            location="São Paulo, SP",
            radius=1000,
            max_results=5,
            output_file="teste.xlsx"
        )
        
        print("✅ Integração com CrewAI OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração com CrewAI: {e}")
        return False

def main():
    """Função principal do teste"""
    
    print("🧪 Iniciando testes de configuração do OpenRouter\n")
    
    tests = [
        ("Configuração básica", test_openrouter_config),
        ("Conexão com OpenRouter", test_openrouter_connection),
        ("Integração com CrewAI", test_crew_integration),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Executando: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSOU")
            else:
                failed += 1
                print(f"❌ {test_name}: FALHOU")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: ERRO - {e}")
    
    print(f"\n📊 Resultados:")
    print(f"✅ Testes aprovados: {passed}")
    print(f"❌ Testes falharam: {failed}")
    
    if failed > 0:
        print("\n💡 Dicas para resolver problemas:")
        print("1. Verifique se o arquivo .env está configurado corretamente")
        print("2. Certifique-se de que OPENROUTER_API_KEY está definida")
        print("3. Confirme que a chave do OpenRouter é válida")
        print("4. Verifique se todas as dependências estão instaladas")
        sys.exit(1)
    else:
        print("\n🎉 Todos os testes passaram! O OpenRouter está configurado corretamente.")

if __name__ == "__main__":
    main() 