# Configuração do Sistema

## Chaves de API Necessárias

### 1. OpenAI API Key (OBRIGATÓRIA)
Esta chave é necessária para os agentes CrewAI funcionarem.

1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova chave
3. Adicione no arquivo `.env`:
```
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 2. Google Maps API Key (OPCIONAL)
Esta chave melhora a precisão da busca, mas não é obrigatória.

1. Acesse: https://console.cloud.google.com/
2. Ative a Google Maps API
3. Crie uma chave
4. Adicione no arquivo `.env`:
```
GOOGLE_MAPS_API_KEY=sua_chave_google_maps_aqui
```

## Configuração Completa

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# Configurações das APIs
OPENAI_API_KEY=sua_chave_openai_aqui
GOOGLE_MAPS_API_KEY=sua_chave_google_maps_aqui

# Configurações do sistema
HEADLESS_MODE=true
SEARCH_DELAY=1
MAX_RESULTS=50
```

## Instalação do ChromeDriver

Para o web scraping funcionar, você precisa do ChromeDriver:

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install chromium-browser chromium-chromedriver
```

### Verificar instalação:
```bash
chromedriver --version
```

## Teste da Configuração

Execute o teste de configuração:
```bash
python -c "from config import Config; print('✅ Configuração OK')"
``` 