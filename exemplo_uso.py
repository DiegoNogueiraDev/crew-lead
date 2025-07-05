#!/usr/bin/env python3
"""
Exemplo prático de uso do Sistema de Captura de Leads
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def exemplo_basico():
    """Exemplo básico de captura de leads"""
    print("🎯 Exemplo Básico - Captura de Leads")
    print("=" * 50)
    
    # Simular configuração (em produção, use variáveis de ambiente)
    print("📋 Configurações:")
    print("- Termo de busca: 'restaurante'")
    print("- Localização: 'São Paulo, SP'")
    print("- Raio: 10 km")
    print("- Máximo de resultados: 25")
    print()
    
    # Dados simulados de exemplo
    exemplo_leads = [
        {
            'nome': 'Restaurante Bella Vista',
            'endereco': 'Rua das Flores, 123 - Vila Madalena, São Paulo - SP',
            'telefone': '(11) 99999-1234',
            'email': 'contato@bellavista.com.br',
            'website': 'https://bellavista.com.br',
            'categoria': 'Restaurante',
            'avaliacao': 4.5,
            'numero_avaliacoes': 127,
            'latitude': -23.5505,
            'longitude': -46.6333,
            'qualidade': 'ALTA',
            'score_qualidade': 9.2
        },
        {
            'nome': 'Pizzaria do Zé',
            'endereco': 'Av. Paulista, 456 - Bela Vista, São Paulo - SP',
            'telefone': '(11) 88888-5678',
            'email': 'pizza@ze.com',
            'website': 'https://pizzariadoze.com',
            'categoria': 'Pizzaria',
            'avaliacao': 4.2,
            'numero_avaliacoes': 89,
            'latitude': -23.5618,
            'longitude': -46.6565,
            'qualidade': 'MÉDIA',
            'score_qualidade': 7.8
        },
        {
            'nome': 'Café Central',
            'endereco': 'Rua Augusta, 789 - Consolação, São Paulo - SP',
            'telefone': '(11) 77777-9012',
            'email': 'cafe@central.com',
            'website': 'https://cafecentral.com.br',
            'categoria': 'Café',
            'avaliacao': 4.7,
            'numero_avaliacoes': 203,
            'latitude': -23.5489,
            'longitude': -46.6388,
            'qualidade': 'ALTA',
            'score_qualidade': 9.5
        }
    ]
    
    print("🔍 Resultados da Captura:")
    print("=" * 50)
    
    for i, lead in enumerate(exemplo_leads, 1):
        print(f"\n📍 Lead {i}:")
        print(f"   Nome: {lead['nome']}")
        print(f"   Endereço: {lead['endereco']}")
        print(f"   Telefone: {lead['telefone']}")
        print(f"   Email: {lead['email']}")
        print(f"   Website: {lead['website']}")
        print(f"   Categoria: {lead['categoria']}")
        print(f"   Avaliação: {lead['avaliacao']} ⭐ ({lead['numero_avaliacoes']} avaliações)")
        print(f"   Qualidade: {lead['qualidade']} (Score: {lead['score_qualidade']})")
        print(f"   Coordenadas: {lead['latitude']}, {lead['longitude']}")
    
    print("\n📊 Estatísticas:")
    print("=" * 50)
    total_leads = len(exemplo_leads)
    leads_alta = sum(1 for lead in exemplo_leads if lead['qualidade'] == 'ALTA')
    leads_media = sum(1 for lead in exemplo_leads if lead['qualidade'] == 'MÉDIA')
    taxa_qualificacao = ((leads_alta + leads_media) / total_leads) * 100
    
    print(f"✅ Total de leads capturados: {total_leads}")
    print(f"🌟 Leads de alta qualidade: {leads_alta}")
    print(f"⭐ Leads de média qualidade: {leads_media}")
    print(f"📈 Taxa de qualificação: {taxa_qualificacao:.1f}%")
    
    # Simular exportação
    filename = f"leads_exemplo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    print(f"\n💾 Dados exportados para: {filename}")
    print("✅ Processo concluído com sucesso!")

def exemplo_avancado():
    """Exemplo avançado com múltiplas configurações"""
    print("\n🚀 Exemplo Avançado - Múltiplas Buscas")
    print("=" * 50)
    
    # Configurações para diferentes tipos de negócio
    configuracoes = [
        {
            'termo': 'clínica médica',
            'localizacao': 'Rio de Janeiro, RJ',
            'raio': 15000,
            'max_resultados': 30,
            'foco': 'Profissionais de saúde'
        },
        {
            'termo': 'escritório de advocacia',
            'localizacao': 'Belo Horizonte, MG',
            'raio': 20000,
            'max_resultados': 20,
            'foco': 'Serviços jurídicos'
        },
        {
            'termo': 'oficina mecânica',
            'localizacao': 'Porto Alegre, RS',
            'raio': 12000,
            'max_resultados': 40,
            'foco': 'Serviços automotivos'
        }
    ]
    
    print("📋 Configurações de Busca:")
    for i, config in enumerate(configuracoes, 1):
        print(f"\n🎯 Busca {i} - {config['foco']}:")
        print(f"   Termo: {config['termo']}")
        print(f"   Localização: {config['localizacao']}")
        print(f"   Raio: {config['raio']/1000} km")
        print(f"   Máximo: {config['max_resultados']} resultados")
    
    # Simular resultados
    print("\n📊 Resultados Consolidados:")
    print("=" * 50)
    
    resultados = {
        'Clínicas (RJ)': {'total': 28, 'qualificados': 22, 'taxa': 78.6},
        'Advogados (BH)': {'total': 19, 'qualificados': 16, 'taxa': 84.2},
        'Oficinas (POA)': {'total': 35, 'qualificados': 27, 'taxa': 77.1}
    }
    
    total_geral = 0
    qualificados_geral = 0
    
    for categoria, stats in resultados.items():
        print(f"\n📍 {categoria}:")
        print(f"   Total encontrados: {stats['total']}")
        print(f"   Qualificados: {stats['qualificados']}")
        print(f"   Taxa de qualificação: {stats['taxa']:.1f}%")
        
        total_geral += stats['total']
        qualificados_geral += stats['qualificados']
    
    taxa_geral = (qualificados_geral / total_geral) * 100
    
    print(f"\n🎯 Resumo Geral:")
    print(f"   Total de leads: {total_geral}")
    print(f"   Leads qualificados: {qualificados_geral}")
    print(f"   Taxa média de qualificação: {taxa_geral:.1f}%")

def exemplo_analise_dados():
    """Exemplo de análise de dados capturados"""
    print("\n📈 Exemplo de Análise de Dados")
    print("=" * 50)
    
    # Dados simulados para análise
    dados_analise = {
        'categorias': {
            'Restaurantes': 45,
            'Clínicas': 32,
            'Advogados': 28,
            'Oficinas': 35,
            'Lojas': 22
        },
        'qualidade': {
            'Alta': 87,
            'Média': 52,
            'Baixa': 23
        },
        'por_cidade': {
            'São Paulo': 68,
            'Rio de Janeiro': 42,
            'Belo Horizonte': 28,
            'Porto Alegre': 24
        },
        'tendencias': {
            'Jan': 45,
            'Fev': 52,
            'Mar': 68,
            'Abr': 75,
            'Mai': 89,
            'Jun': 94
        }
    }
    
    print("📊 Análise por Categoria:")
    for categoria, count in dados_analise['categorias'].items():
        print(f"   {categoria}: {count} leads")
    
    print("\n⭐ Análise por Qualidade:")
    total_qualidade = sum(dados_analise['qualidade'].values())
    for qualidade, count in dados_analise['qualidade'].items():
        percentual = (count / total_qualidade) * 100
        print(f"   {qualidade}: {count} leads ({percentual:.1f}%)")
    
    print("\n🌍 Análise por Cidade:")
    for cidade, count in dados_analise['por_cidade'].items():
        print(f"   {cidade}: {count} leads")
    
    print("\n📈 Tendência Mensal:")
    for mes, count in dados_analise['tendencias'].items():
        print(f"   {mes}: {count} leads")
    
    # Insights automáticos
    print("\n🔍 Insights Automáticos:")
    print("=" * 50)
    
    categoria_top = max(dados_analise['categorias'], key=dados_analise['categorias'].get)
    cidade_top = max(dados_analise['por_cidade'], key=dados_analise['por_cidade'].get)
    
    print(f"✅ Categoria com mais leads: {categoria_top}")
    print(f"🏆 Cidade com mais leads: {cidade_top}")
    print(f"📊 Taxa de qualidade alta: {(dados_analise['qualidade']['Alta'] / total_qualidade) * 100:.1f}%")
    print(f"📈 Crescimento mensal médio: +12.5%")

def exemplo_configuracao():
    """Exemplo de configuração do sistema"""
    print("\n⚙️ Exemplo de Configuração")
    print("=" * 50)
    
    print("🔑 Configurações Necessárias:")
    print()
    
    print("1. Variáveis de Ambiente:")
    print("   export OPENAI_API_KEY='sua_chave_openai'")
    print("   export GOOGLE_MAPS_API_KEY='sua_chave_google_maps'")
    print("   export HEADLESS_MODE=True")
    print("   export MAX_RESULTS_PER_SEARCH=50")
    print()
    
    print("2. Instalação do ChromeDriver:")
    print("   # Ubuntu/Debian")
    print("   sudo apt-get install chromium-chromedriver")
    print()
    print("   # macOS")
    print("   brew install chromedriver")
    print()
    
    print("3. Comandos de Uso:")
    print("   # Interface Web")
    print("   streamlit run app.py")
    print()
    print("   # Linha de Comando")
    print("   python main.py --termo 'restaurante' --localizacao 'São Paulo, SP'")
    print()
    
    print("4. Estrutura de Arquivos:")
    print("   crew-lead/")
    print("   ├── main.py           # Entrada principal")
    print("   ├── app.py            # Interface web")
    print("   ├── config.py         # Configurações")
    print("   ├── requirements.txt  # Dependências")
    print("   └── README.md         # Documentação")

def main():
    """Função principal com menu interativo"""
    print("🎯 Sistema de Captura de Leads do Google Maps")
    print("Powered by CrewAI")
    print("=" * 60)
    
    while True:
        print("\n📋 Menu de Exemplos:")
        print("1. 🔍 Exemplo Básico")
        print("2. 🚀 Exemplo Avançado")
        print("3. 📈 Análise de Dados")
        print("4. ⚙️ Configuração")
        print("5. ❌ Sair")
        
        try:
            opcao = input("\nEscolha uma opção (1-5): ").strip()
            
            if opcao == "1":
                exemplo_basico()
            elif opcao == "2":
                exemplo_avancado()
            elif opcao == "3":
                exemplo_analise_dados()
            elif opcao == "4":
                exemplo_configuracao()
            elif opcao == "5":
                print("\n👋 Obrigado por usar o Sistema de Captura de Leads!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo do programa...")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main() 