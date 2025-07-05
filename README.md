# Sistema de Captura e Qualificação de Leads com IA

Este é um sistema avançado para captura de leads do Google Maps, construído com **CrewAI**. Ele automatiza todo o processo de busca, enriquecimento e qualificação de contatos comerciais, transformando uma tarefa manual e demorada em um fluxo de trabalho inteligente e eficiente.

## 🚀 Principais Funcionalidades

- **🔍 Captura Inteligente**: Combina a precisão da **API do Google Maps** com a abrangência do **web scraping** para extrair o máximo de informações.
- **🤖 Automação com Agentes de IA**: Utiliza um time de agentes autônomos (CrewAI) para orquestrar o trabalho:
    - **Agente Pesquisador**: Encontra negócios com base nos seus critérios.
    - **Agente Enriquecedor**: Busca dados adicionais como e-mails, redes sociais e tecnologias usadas no site.
    - **Agente Validador**: Analisa e classifica os leads, atribuindo um score de qualidade.
    - **Agente Organizador**: Formata e prepara os dados para exportação.
- **📊 Dashboard Interativo**: Uma interface web amigável (Streamlit) para iniciar buscas, visualizar resultados, aplicar filtros e exportar dados.
- **💾 Armazenamento Persistente**: Salva todos os leads capturados em um banco de dados **SQLite**, permitindo consultas futuras.
- **📤 Exportação Flexível**: Exporte seus leads qualificados para formatos como **Excel, CSV e JSON**.

## 🛠️ Instalação e Configuração

Siga os 3 passos abaixo para deixar o sistema pronto para uso.

### Passo 1: Instalação Automática

O projeto inclui um script que cuida de toda a configuração inicial.

```bash
# Concede permissão de execução e roda o script
chmod +x ./install.sh
./install.sh
```

Este script irá:
1. Criar um ambiente virtual (`venv`).
2. Ativar o ambiente.
3. Instalar todas as dependências do `requirements.txt`.
4. Criar um arquivo de configuração `.env` a partir do exemplo.

### Passo 2: Configurar Chaves de API e Variáveis de Ambiente

Edite o arquivo `.env` que foi criado na raiz do projeto. Abaixo está um exemplo completo com todas as opções possíveis e comentários explicando cada uma delas.

```env
# =================================================================
#                 CONFIGURAÇÕES OBRIGATÓRIAS
# =================================================================

# CHAVE DA API DO OPENROUTER
# Essencial para o funcionamento dos agentes de IA.
# 1. Acesse: https://openrouter.ai/keys
# 2. Crie uma chave e adicione créditos à sua conta.
OPENROUTER_API_KEY=sk-or-sua_chave_openrouter_aqui

# MODELO DE LINGUAGEM (LLM)
# Modelo que será usado pelos agentes. Veja a lista de modelos disponíveis
# em https://openrouter.ai/models.
# Exemplos: "openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro"
OPENROUTER_MODEL=openai/gpt-4o

# =================================================================
#                 CONFIGURAÇÕES RECOMENDADAS
# =================================================================

# CHAVE DA API DO GOOGLE MAPS
# Altamente recomendado para buscas mais rápidas, precisas e com mais dados.
# Se deixada em branco, o sistema usará web scraping (mais lento e instável).
# 1. Acesse: https://console.cloud.google.com/
# 2. Ative as APIs: Maps JavaScript, Places e Geocoding.
# 3. Crie uma chave de API.
GOOGLE_MAPS_API_KEY=sua_chave_google_maps_aqui

# =================================================================
#                 CONFIGURAÇÕES OPCIONAIS E AVANÇADAS
# =================================================================

# MODO HEADLESS PARA SCRAPING
# Define se o navegador do Selenium rodará em segundo plano (true) ou visível (false).
# Mantenha como "true" para melhor performance em servidores.
HEADLESS_MODE=True

# ATRASO ENTRE BUSCAS (EM SEGUNDOS)
# Delay para o web scraping não sobrecarregar os servidores do Google.
# Aumente este valor se encontrar erros de "rate limiting".
SEARCH_DELAY=2

# CAMINHO PARA O CHROMEDRIVER
# Apenas modifique se o chromedriver não estiver em um caminho padrão.
CHROME_DRIVER_PATH=/usr/bin/chromedriver

# URL DO BANCO DE DADOS
# Por padrão, usa um arquivo SQLite local. Pode ser alterado para PostgreSQL, etc.
DATABASE_URL=sqlite:///leads.db

# MODO DEBUG
# Ativa logs mais detalhados para depuração.
DEBUG=True

# URL e Nome do Site (para OpenRouter)
# Informações opcionais usadas para identificação nos logs do OpenRouter.
OPENROUTER_SITE_URL=https://meuprojeto.com
OPENROUTER_SITE_NAME=Meu Projeto de Leads
```

No arquivo `.env` você também pode configurar o modelo de linguagem a ser usado (ex: `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`, etc.).

### Passo 3: Instalar o ChromeDriver (se necessário)

Para a função de web scraping, o sistema utiliza o Selenium, que requer o ChromeDriver.

```bash
# Para sistemas baseados em Debian/Ubuntu
sudo apt-get update
sudo apt-get install chromium-chromedriver

# Para macOS (usando Homebrew)
brew install chromedriver
```
Se você encontrar problemas, verifique se a versão do ChromeDriver é compatível com a do seu navegador Chrome.

## 🎮 Como Usar o Sistema

Você pode interagir com o sistema de duas formas:

### 🖥️ Interface Web (Recomendado)

A forma mais simples de usar. Ideal para visualizar e gerenciar os leads.

```bash
# Execute o script para iniciar a aplicação web
./start.sh
```
Acesse o dashboard em `http://localhost:8501`.

### 💻 Linha de Comando

Para automação e integração com outros scripts.

```bash
# Lembre-se de ativar o ambiente virtual primeiro
source venv/bin/activate

# Exemplo: Buscar restaurantes em São Paulo
python main.py --termo "restaurante" --localizacao "São Paulo, SP"

# Exemplo: Buscar advogados em Belo Horizonte com mais resultados
python main.py -t "advogado" -l "Belo Horizonte, MG" -m 100
```

**Parâmetros disponíveis:**

| Parâmetro           | Atalho | Descrição                                             | Padrão                               |
|---------------------|--------|-------------------------------------------------------|--------------------------------------|
| `--termo`           | `-t`   | Termo de busca (ex: "dentista", "escritório de TI").    | **Obrigatório**                      |
| `--localizacao`     | `-l`   | A cidade e estado para a busca (ex: "Curitiba, PR").    | **Obrigatório**                      |
| `--raio`            | `-r`   | Raio da busca em metros.                                | `10000`                              |
| `--max-resultados`  | `-m`   | Número máximo de resultados a serem capturados.       | `50`                                 |
| `--arquivo-saida`   | `-o`   | Nome do arquivo Excel para exportação.                | `leads_AAAAMMDD_HHMMSS.xlsx`         |

## 🏗️ Arquitetura e Estrutura do Projeto

O sistema é modular e organizado para facilitar a manutenção e customização.

```
crew-lead/
├── 🚀 main.py              # Ponto de entrada para a CLI
├── 🌐 app.py               # Interface web com Streamlit
├── ⚙️ config.py             # Carrega as configurações do .env
├── 📦 requirements.txt     # Dependências do projeto
├── 📄 README.md            # Esta documentação
├── 🔧 install.sh           # Script de instalação
├── 🚀 start.sh             # Script para iniciar a interface web
│
├── 🤖 crew/                # Orquestração dos agentes (CrewAI)
├── 👥 agents/              # Definição dos papéis e objetivos dos agentes
├── 📋 tasks/               # Definição das tarefas que os agentes executam
├── 🛠️ tools/               # Ferramentas que os agentes usam (ex: busca no Maps)
└── 🔧 utils/               # Módulos de utilidade (banco de dados, logs)
```

## 🆘 Troubleshooting

- **Erro de ChromeDriver**: Verifique se a versão instalada é compatível com seu Google Chrome. Ocasionalmente, pode ser necessário especificar o caminho para o executável no `.env`.
- **Erro de Chave de API**: Garanta que o arquivo `.env` está na raiz do projeto e que as chaves foram copiadas corretamente, sem espaços extras. Verifique também se há créditos na sua conta OpenRouter.
- **Erro de `ModuleNotFoundError`**: Certifique-se de que o ambiente virtual está ativado (`source venv/bin/activate`) antes de executar os scripts Python.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* para reportar bugs ou sugerir novas funcionalidades.

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 