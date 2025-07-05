#!/bin/bash

# Script de Instalação Automática - Sistema de Captura de Leads
# Powered by CrewAI

echo "🎯 Sistema de Captura de Leads do Google Maps"
echo "Powered by CrewAI"
echo "============================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para print colorido
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Verificar se está rodando no Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_warning "Este script foi otimizado para Linux. Pode não funcionar corretamente em outros sistemas."
fi

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar Python
echo "🐍 Verificando Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION encontrado"
else
    print_error "Python 3 não encontrado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# Verificar pip
echo ""
echo "📦 Verificando pip..."
if command_exists pip3; then
    print_status "pip encontrado"
else
    print_error "pip não encontrado. Instalando..."
    sudo apt-get install -y python3-pip
fi

# Criar ambiente virtual
echo ""
echo "🔧 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Ambiente virtual criado"
else
    print_info "Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo ""
echo "🚀 Ativando ambiente virtual..."
source venv/bin/activate
print_status "Ambiente virtual ativado"

# Instalar dependências
echo ""
echo "📚 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt
print_status "Dependências instaladas"

# Verificar Chrome/Chromium
echo ""
echo "🌐 Verificando Chrome/Chromium..."
if command_exists google-chrome; then
    CHROME_VERSION=$(google-chrome --version 2>&1 | cut -d' ' -f3)
    print_status "Google Chrome $CHROME_VERSION encontrado"
elif command_exists chromium-browser; then
    CHROMIUM_VERSION=$(chromium-browser --version 2>&1 | cut -d' ' -f2)
    print_status "Chromium $CHROMIUM_VERSION encontrado"
else
    print_warning "Chrome/Chromium não encontrado. Instalando Chromium..."
    sudo apt-get install -y chromium-browser
fi

# Instalar ChromeDriver
echo ""
echo "🔧 Instalando ChromeDriver..."
if command_exists chromedriver; then
    CHROMEDRIVER_VERSION=$(chromedriver --version 2>&1 | cut -d' ' -f2)
    print_status "ChromeDriver $CHROMEDRIVER_VERSION encontrado"
else
    print_info "Instalando ChromeDriver..."
    sudo apt-get install -y chromium-chromedriver
    print_status "ChromeDriver instalado"
fi

# Verificar se ChromeDriver está no PATH
if command_exists chromedriver; then
    print_status "ChromeDriver está no PATH"
else
    print_warning "ChromeDriver pode não estar no PATH. Verifique a instalação."
fi

# Criar diretórios necessários
echo ""
echo "📁 Criando estrutura de diretórios..."
mkdir -p logs
mkdir -p data
mkdir -p exports
print_status "Diretórios criados"

# Verificar arquivo de configuração
echo ""
echo "⚙️ Verificando configurações..."
if [ ! -f ".env" ]; then
    print_warning "Arquivo .env não encontrado. Criando template..."
    cat > .env << 'EOF'
# Configurações da API OpenAI
OPENAI_API_KEY=sua_chave_openai_aqui

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
EOF
    print_status "Arquivo .env criado. Configure suas chaves de API!"
else
    print_info "Arquivo .env já existe"
fi

# Testar instalação
echo ""
echo "🧪 Testando instalação..."
python3 -c "
import sys
import importlib

modules = [
    'crewai', 'selenium', 'beautifulsoup4', 'requests', 
    'pandas', 'streamlit', 'plotly', 'googlemaps'
]

print('Testando módulos Python...')
for module in modules:
    try:
        if module == 'beautifulsoup4':
            importlib.import_module('bs4')
        elif module == 'googlemaps':
            importlib.import_module('googlemaps')
        else:
            importlib.import_module(module.replace('-', '_'))
        print(f'✓ {module}')
    except ImportError as e:
        print(f'✗ {module}: {e}')
        sys.exit(1)

print('Todos os módulos foram importados com sucesso!')
"

if [ $? -eq 0 ]; then
    print_status "Teste de importação bem-sucedido"
else
    print_error "Erro nos testes de importação"
    exit 1
fi

# Inicializar banco de dados
echo ""
echo "🗄️ Inicializando banco de dados..."
python3 -c "
from utils.database import init_database
try:
    init_database()
    print('✓ Banco de dados inicializado')
except Exception as e:
    print(f'✗ Erro ao inicializar banco: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    print_status "Banco de dados inicializado"
else
    print_error "Erro ao inicializar banco de dados"
fi

# Criar script de inicialização
echo ""
echo "📝 Criando script de inicialização..."
cat > start.sh << 'EOF'
#!/bin/bash
echo "🎯 Iniciando Sistema de Captura de Leads..."
source venv/bin/activate
streamlit run app.py
EOF

chmod +x start.sh
print_status "Script de inicialização criado (start.sh)"

# Mensagem final
echo ""
echo "============================================="
echo -e "${GREEN}🎉 Instalação concluída com sucesso!${NC}"
echo "============================================="
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. 🔑 Configure suas chaves de API no arquivo .env:"
echo "   - OPENAI_API_KEY (obrigatório)"
echo "   - GOOGLE_MAPS_API_KEY (obrigatório)"
echo ""
echo "2. 🚀 Execute o sistema:"
echo "   ./start.sh"
echo "   ou"
echo "   source venv/bin/activate && streamlit run app.py"
echo ""
echo "3. 🌐 Acesse no navegador:"
echo "   http://localhost:8501"
echo ""
echo "4. 💻 Use via linha de comando:"
echo "   source venv/bin/activate"
echo "   python main.py --termo 'restaurante' --localizacao 'São Paulo, SP'"
echo ""
echo "5. 📖 Veja exemplos:"
echo "   python exemplo_uso.py"
echo ""
echo "📚 Documentação completa: README.md"
echo ""
echo -e "${BLUE}🎯 Sistema pronto para capturar leads!${NC}"
echo ""

# Opcional: Abrir automaticamente
read -p "Deseja iniciar o sistema agora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Iniciando sistema..."
    ./start.sh
fi 