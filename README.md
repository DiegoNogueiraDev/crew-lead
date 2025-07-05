# 🎯 Sistema de Captura de Leads do Google Maps

Um sistema avançado de captura de leads do Google Maps utilizando **CrewAI** para automatizar o processo de busca, enriquecimento e qualificação de leads.

## 🚀 Funcionalidades

### 🔍 Captura Inteligente
- **Busca no Google Maps**: Utiliza API do Google Maps e web scraping
- **Múltiplos critérios**: Busca por termo, localização e raio personalizado
- **Dados completos**: Nome, endereço, telefone, email, website, avaliações

### 🤖 Automação com CrewAI
- **Agente Pesquisador**: Especializado em encontrar leads no Google Maps
- **Agente Enriquecedor**: Adiciona informações de contato e detalhes
- **Agente Validador**: Classifica leads por qualidade e relevância
- **Agente Organizador**: Formata e exporta os resultados

### 📊 Interface Web Moderna
- **Dashboard interativo**: Visualização de métricas e gráficos
- **Gerenciamento de leads**: Edição, filtros e exportação
- **Relatórios avançados**: Análise de performance e comparações

## 🛠️ Instalação

### 1. Clonar o Repositório
```bash
git clone https://github.com/Diego/crew-lead.git
cd crew-lead
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do OpenRouter
OPENROUTER_API_KEY=sk-or-sua_chave_openrouter_aqui
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4

# Configurações do Google Maps API
GOOGLE_MAPS_API_KEY=sua_chave_google_maps_aqui

# Configurações do Selenium
CHROME_DRIVER_PATH=/usr/bin/chromedriver
HEADLESS_MODE=True

# Configurações do banco de dados
DATABASE_URL=sqlite:///leads.db

# Configurações gerais
DEBUG=True
MAX_RESULTS_PER_SEARCH=50
SEARCH_DELAY=2
```

### 4. Instalar ChromeDriver
```bash
# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver

# Windows
# Baixar do site oficial: https://chromedriver.chromium.org/
```

## 🎮 Como Usar

### 🖥️ Interface Web (Recomendado)
```bash
streamlit run app.py
```

Acesse: `http://localhost:8501`

### 💻 Linha de Comando
```bash
python main.py --termo "restaurante" --localizacao "São Paulo, SP" --raio 10000 --max-resultados 50
```

#### Parâmetros disponíveis:
- `--termo, -t`: Termo de busca (obrigatório)
- `--localizacao, -l`: Localização para busca
- `--raio, -r`: Raio de busca em metros (padrão: 10000)
- `--max-resultados, -m`: Número máximo de resultados (padrão: 50)
- `--arquivo-saida, -o`: Arquivo de saída (padrão: leads_YYYYMMDD_HHMMSS.xlsx)

### 📖 Exemplos de Uso

#### Buscar Restaurantes em São Paulo
```bash
python main.py --termo "restaurante" --localizacao "São Paulo, SP"
```

#### Buscar Clínicas em Rio de Janeiro
```bash
python main.py --termo "clínica médica" --localizacao "Rio de Janeiro, RJ" --raio 15000
```

#### Buscar Advogados em Belo Horizonte
```bash
python main.py --termo "advogado" --localizacao "Belo Horizonte, MG" --max-resultados 100
```

## 🏗️ Arquitetura do Sistema

### 📁 Estrutura do Projeto
```
crew-lead/
├── main.py                 # Ponto de entrada principal
├── app.py                  # Interface web Streamlit
├── config.py               # Configurações do sistema
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
│
├── crew/                   # Módulo CrewAI
│   ├── __init__.py
│   └── lead_capture_crew.py
│
├── agents/                 # Agentes CrewAI
│   ├── __init__.py
│   └── lead_agents.py
│
├── tasks/                  # Tarefas CrewAI
│   ├── __init__.py
│   └── lead_tasks.py
│
├── tools/                  # Ferramentas personalizadas
│   ├── __init__.py
│   ├── google_maps_tool.py
│   └── data_enrichment_tool.py
│
├── utils/                  # Utilitários
│   ├── __init__.py
│   ├── database.py
│   └── logger.py
│
└── data/                   # Dados e exportações
    ├── leads.db           # Banco de dados SQLite
    └── exports/           # Arquivos exportados
```

### 🔄 Fluxo de Trabalho
1. **Pesquisa**: Agente pesquisador busca estabelecimentos no Google Maps
2. **Enriquecimento**: Agente enriquecedor adiciona informações extras
3. **Validação**: Agente validador classifica leads por qualidade
4. **Organização**: Agente organizador formata e exporta resultados

## 🔧 Configuração Avançada

### 🗝️ Obter Chaves de API

#### OpenRouter API Key
1. Acesse [OpenRouter](https://openrouter.ai/)
2. Crie uma conta ou faça login
3. Vá para "Keys" e crie uma nova chave de API
4. Adicione créditos à sua conta
5. Escolha o modelo desejado (ex: openai/gpt-4, anthropic/claude-3-opus)

#### Google Maps API Key
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto ou selecione um existente
3. Ative as APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. Crie credenciais (API Key)
5. Configure restrições de uso

### 📊 Banco de Dados

O sistema usa SQLite por padrão, mas pode ser configurado para outros bancos:

```python
# config.py
DATABASE_URL = "postgresql://user:password@localhost/leads"
# ou
DATABASE_URL = "mysql://user:password@localhost/leads"
```

### 🔍 Customização de Agentes

Você pode customizar os agentes editando `agents/lead_agents.py`:

```python
def pesquisador_leads(self) -> Agent:
    return Agent(
        role='Pesquisador de Leads Personalizado',
        goal='Seu objetivo personalizado',
        backstory='Sua história personalizada',
        # ... outras configurações
    )
```

## 📊 Métricas e Monitoramento

### 📈 Métricas Disponíveis
- **Leads capturados**: Número total de leads encontrados
- **Taxa de qualificação**: Percentual de leads qualificados
- **Cobertura geográfica**: Distribuição por localização
- **Performance por categoria**: Análise por tipo de negócio

### 📋 Logs e Debugging
Os logs são salvos em `logs/lead_capture_YYYYMMDD.log`:

```python
# Habilitar debug
DEBUG=True
```

## 🚨 Limitações e Considerações

### ⚠️ Rate Limiting
- Google Maps API: 1000 requests/dia (gratuito)
- Selenium: Delay configurável entre requests
- Recomendado: `SEARCH_DELAY=2` segundos

### 🔒 Aspectos Legais
- Respeite os termos de uso do Google Maps
- Não use para spam ou atividades não autorizadas
- Considere a LGPD para dados pessoais

### 🌐 Proxy e VPN
Para uso intensivo, considere usar proxy:

```python
# tools/google_maps_tool.py
chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
```

## 🤝 Contribuindo

### 🐛 Reportar Bugs
1. Verifique se o bug já foi reportado
2. Crie uma issue detalhada
3. Inclua logs e informações do sistema

### 🔧 Desenvolvimento
```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar testes
pytest tests/

# Verificar código
black .
flake8 .
```

## 📝 Changelog

### v1.0.0 (2024-01-15)
- ✅ Implementação inicial do sistema
- ✅ Interface web com Streamlit
- ✅ Agentes CrewAI para automação
- ✅ Suporte a Google Maps API e web scraping
- ✅ Banco de dados SQLite integrado

## 📞 Suporte

### 🆘 Problemas Comuns

#### Erro de ChromeDriver
```bash
# Verificar versão do Chrome
google-chrome --version

# Baixar ChromeDriver compatível
# https://chromedriver.chromium.org/downloads
```

#### Erro de API Key
```bash
# Verificar se as chaves estão definidas
echo $OPENAI_API_KEY
echo $GOOGLE_MAPS_API_KEY
```

#### Erro de Dependências
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### 📧 Contato
- **Email**: suporte@crewlead.com
- **GitHub Issues**: [github.com/seu-usuario/crew-lead/issues](https://github.com/seu-usuario/crew-lead/issues)
- **Discord**: [discord.gg/crewlead](https://discord.gg/crewlead)

## 📜 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

🚀 **Desenvolvido com CrewAI** - Automatize sua geração de leads hoje mesmo! 