# 🚀 Guia de Início Rápido

## ⚡ Instalação em 3 Passos

### 1. 🔧 Instalação Automática
```bash
# Executar script de instalação
./install.sh
```

### 2. 🔑 Configurar APIs
Edite o arquivo `.env` com suas chaves:
```env
OPENAI_API_KEY=sua_chave_openai_aqui
GOOGLE_MAPS_API_KEY=sua_chave_google_maps_aqui
```

### 3. 🚀 Executar Sistema
```bash
# Interface web
./start.sh

# Ou linha de comando
source venv/bin/activate
python main.py --termo "restaurante" --localizacao "São Paulo, SP"
```

## 🗝️ Obter Chaves de API

### OpenAI API Key
1. Acesse: https://platform.openai.com/api-keys
2. Crie conta ou faça login
3. Gere nova chave de API
4. Adicione créditos (mínimo $5)

### Google Maps API Key
1. Acesse: https://console.cloud.google.com/
2. Crie novo projeto
3. Ative APIs necessárias:
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. Crie credenciais (API Key)
5. Configure restrições (opcional)

## 📖 Exemplos de Uso

### Via Interface Web
```bash
streamlit run app.py
# Acesse: http://localhost:8501
```

### Via Linha de Comando
```bash
# Buscar restaurantes em São Paulo
python main.py --termo "restaurante" --localizacao "São Paulo, SP"

# Buscar clínicas no Rio de Janeiro
python main.py --termo "clínica" --localizacao "Rio de Janeiro, RJ" --raio 15000

# Buscar advogados em Belo Horizonte
python main.py --termo "advogado" --localizacao "Belo Horizonte, MG" --max-resultados 100
```

### Exemplos Interativos
```bash
# Menu de exemplos
python exemplo_uso.py
```

## 🎯 Principais Funcionalidades

- ✅ **Busca no Google Maps** - API + Web Scraping
- ✅ **Enriquecimento de Dados** - Emails, telefones, websites
- ✅ **Validação de Qualidade** - Classificação automática
- ✅ **Interface Web** - Dashboard interativo
- ✅ **Exportação** - Excel, CSV, JSON
- ✅ **Banco de Dados** - SQLite integrado

## 🛠️ Troubleshooting

### Erro de ChromeDriver
```bash
# Verificar versão do Chrome
google-chrome --version

# Instalar ChromeDriver
sudo apt-get install chromium-chromedriver
```

### Erro de Importação
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro de API Key
```bash
# Verificar se estão definidas
echo $OPENAI_API_KEY
echo $GOOGLE_MAPS_API_KEY

# Ou verificar no arquivo .env
cat .env
```

## 📊 Estrutura de Arquivos

```
crew-lead/
├── 🚀 main.py              # Entrada principal
├── 🌐 app.py               # Interface web
├── ⚙️ config.py            # Configurações
├── 📦 requirements.txt     # Dependências
├── 📖 README.md           # Documentação completa
├── ⚡ QUICKSTART.md       # Este guia
├── 🔧 install.sh          # Script de instalação
├── 📝 exemplo_uso.py      # Exemplos práticos
│
├── 🤖 crew/               # Módulo CrewAI
├── 👥 agents/             # Agentes
├── 📋 tasks/              # Tarefas
├── 🛠️ tools/              # Ferramentas
└── 🔧 utils/              # Utilitários
```

## 🎯 Próximos Passos

1. **Configurar APIs** - Obter chaves necessárias
2. **Testar Sistema** - Executar exemplos
3. **Primeira Captura** - Buscar leads do seu nicho
4. **Explorar Dashboard** - Analisar resultados
5. **Customizar Agentes** - Adaptar para suas necessidades

## 💡 Dicas Importantes

- 📊 **Rate Limiting**: Google Maps API tem limite de 1000 requests/dia (gratuito)
- 🔒 **Aspectos Legais**: Respeite termos de uso e LGPD
- 🚀 **Performance**: Use `HEADLESS_MODE=True` para melhor performance
- 💾 **Backups**: Dados são salvos automaticamente no SQLite

## 🆘 Suporte

- 📖 **Documentação**: README.md
- 🐛 **Issues**: GitHub Issues
- 💬 **Comunidade**: Discord
- 📧 **Email**: suporte@crewlead.com

---

🎯 **Comece agora mesmo!** Execute `./install.sh` para começar! 