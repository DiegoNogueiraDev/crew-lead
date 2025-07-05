import os

# Carregar variáveis de ambiente do .env se disponível
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv não está disponível, usar apenas variáveis de ambiente do sistema
    pass

class Config:
    """Configurações do projeto de captura de leads"""
    
    # Configurações da API OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4")
    
    # Configurações opcionais do OpenRouter
    OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "")
    OPENROUTER_SITE_NAME = os.getenv("OPENROUTER_SITE_NAME", "")
    
    # Configurações do Google Maps API
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # Configurações do Selenium
    CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", "/usr/bin/chromedriver")
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True").lower() == "true"
    
    # Configurações do banco de dados
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///leads.db")
    
    # Configurações gerais
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    MAX_RESULTS_PER_SEARCH = int(os.getenv("MAX_RESULTS_PER_SEARCH", "50"))
    SEARCH_DELAY = int(os.getenv("SEARCH_DELAY", "2"))
    
    # Configurações específicas para leads
    DEFAULT_SEARCH_RADIUS = 10000  # 10km em metros
    DEFAULT_LOCATION = "São Paulo, SP, Brasil"
    
    @classmethod
    def validate(cls):
        """Valida se as configurações necessárias estão definidas"""
        required_vars = [
            "OPENROUTER_API_KEY",
            "GOOGLE_MAPS_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Variáveis de ambiente obrigatórias não definidas: {', '.join(missing_vars)}")
        
        return True 