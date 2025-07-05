# Configuração do Sistema

## Chaves de API Necessárias

### 1. OpenRouter API Key (OBRIGATÓRIA)
Esta chave é necessária para os agentes CrewAI funcionarem. OpenRouter permite acesso a múltiplos modelos de IA.

1. Acesse: https://openrouter.ai/
2. Crie uma conta ou faça login
3. Vá para "Keys" e crie uma nova chave
4. Adicione no arquivo `.env`:
```
OPENROUTER_API_KEY=sk-or-sua_chave_openrouter_aqui
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
# Configurações do OpenRouter
OPENROUTER_API_KEY=sk-or-sua_chave_openrouter_aqui
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4
# Opcionais para rankings no OpenRouter
OPENROUTER_SITE_URL=https://seu-site.com
OPENROUTER_SITE_NAME=Nome do Seu Site

# Configurações do Google Maps
GOOGLE_MAPS_API_KEY=sua_chave_google_maps_aqui

# Configurações do sistema
HEADLESS_MODE=true
SEARCH_DELAY=1
MAX_RESULTS=50
```

## Modelos Disponíveis no OpenRouter

O OpenRouter oferece acesso a múltiplos modelos de IA:

- `openai/gpt-4` - GPT-4 (recomendado)
- `openai/gpt-3.5-turbo` - GPT-3.5 Turbo (mais barato)
- `anthropic/claude-3-opus` - Claude 3 Opus
- `anthropic/claude-3-sonnet` - Claude 3 Sonnet
- `google/gemini-pro` - Gemini Pro
- `meta-llama/llama-2-70b-chat` - Llama 2 70B

Para usar um modelo específico, altere a variável `OPENROUTER_MODEL` no arquivo `.env`.

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