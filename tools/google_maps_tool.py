from crewai.tools import BaseTool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import googlemaps
import time
import json
from typing import List, Dict, Optional
from config import Config

class GoogleMapsSearchTool(BaseTool):
    """Ferramenta para buscar estabelecimentos no Google Maps"""
    
    name: str = "GoogleMapsSearch"
    description: str = "Ferramenta para pesquisar estabelecimentos no Google Maps usando diferentes métodos"
    
    def __init__(self):
        super().__init__()
        self.gmaps = googlemaps.Client(key=Config.GOOGLE_MAPS_API_KEY) if Config.GOOGLE_MAPS_API_KEY else None
        self.driver = None
        
    def setup_driver(self):
        """Configura o driver do Selenium para web scraping"""
        chrome_options = Options()
        if Config.HEADLESS_MODE:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def search_businesses(self, search_term: str, location: str, radius: int = 10000, max_results: int = 50) -> List[Dict]:
        """
        Busca estabelecimentos no Google Maps
        
        Args:
            search_term: Termo de busca (ex: "restaurante", "dentista")
            location: Localização (ex: "São Paulo, SP")
            radius: Raio de busca em metros
            max_results: Número máximo de resultados
            
        Returns:
            Lista de estabelecimentos encontrados
        """
        try:
            # Tentar usar Google Maps API primeiro
            if self.gmaps:
                return self._search_with_api(search_term, location, radius, max_results)
            else:
                # Fallback para web scraping
                return self._search_with_scraping(search_term, location, max_results)
                
        except Exception as e:
            print(f"Erro ao buscar estabelecimentos: {e}")
            return []
    
    def _search_with_api(self, search_term: str, location: str, radius: int, max_results: int) -> List[Dict]:
        """Busca usando Google Maps API"""
        try:
            # Geocodificar a localização
            geocode_result = self.gmaps.geocode(location)
            if not geocode_result:
                raise ValueError(f"Localização não encontrada: {location}")
            
            lat_lng = geocode_result[0]['geometry']['location']
            
            # Buscar estabelecimentos próximos
            places_result = self.gmaps.places_nearby(
                location=lat_lng,
                radius=radius,
                keyword=search_term,
                type="establishment"
            )
            
            businesses = []
            for place in places_result.get('results', [])[:max_results]:
                # Obter detalhes do estabelecimento
                details = self.gmaps.place(
                    place_id=place['place_id'],
                    fields=['name', 'formatted_address', 'formatted_phone_number', 
                           'website', 'rating', 'user_ratings_total', 'opening_hours',
                           'geometry', 'types', 'photos']
                )
                
                place_details = details.get('result', {})
                
                business = {
                    'nome': place_details.get('name', ''),
                    'endereco': place_details.get('formatted_address', ''),
                    'telefone': place_details.get('formatted_phone_number', ''),
                    'website': place_details.get('website', ''),
                    'categoria': ', '.join(place_details.get('types', [])),
                    'avaliacao': place_details.get('rating', 0),
                    'numero_avaliacoes': place_details.get('user_ratings_total', 0),
                    'horario_funcionamento': self._format_opening_hours(place_details.get('opening_hours', {})),
                    'latitude': place_details.get('geometry', {}).get('location', {}).get('lat', 0),
                    'longitude': place_details.get('geometry', {}).get('location', {}).get('lng', 0),
                    'place_id': place['place_id'],
                    'fotos': self._get_photo_urls(place_details.get('photos', []))
                }
                
                businesses.append(business)
                
                # Delay para evitar rate limiting
                time.sleep(Config.SEARCH_DELAY)
            
            return businesses
            
        except Exception as e:
            print(f"Erro na busca via API: {e}")
            return []
    
    def _search_with_scraping(self, search_term: str, location: str, max_results: int) -> List[Dict]:
        """Busca usando web scraping do Google Maps"""
        try:
            self.setup_driver()
            
            # Construir URL de busca
            query = f"{search_term} {location}"
            url = f"https://www.google.com/maps/search/{query}"
            
            self.driver.get(url)
            time.sleep(3)
            
            # Aguardar carregamento dos resultados
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-result-index]"))
            )
            
            businesses = []
            result_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-result-index]")
            
            for i, element in enumerate(result_elements[:max_results]):
                try:
                    # Clicar no resultado para obter mais detalhes
                    element.click()
                    time.sleep(2)
                    
                    # Extrair informações
                    business = self._extract_business_info()
                    if business:
                        businesses.append(business)
                        
                except Exception as e:
                    print(f"Erro ao extrair informações do estabelecimento {i}: {e}")
                    continue
                    
                time.sleep(Config.SEARCH_DELAY)
            
            return businesses
            
        except Exception as e:
            print(f"Erro no web scraping: {e}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
    
    def _extract_business_info(self) -> Optional[Dict]:
        """Extrai informações do estabelecimento da página"""
        try:
            business = {}
            
            # Nome
            nome_element = self.driver.find_element(By.CSS_SELECTOR, "h1")
            business['nome'] = nome_element.text if nome_element else ""
            
            # Endereço
            try:
                endereco_element = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']")
                business['endereco'] = endereco_element.text if endereco_element else ""
            except NoSuchElementException:
                business['endereco'] = ""
            
            # Telefone
            try:
                telefone_element = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id*='phone']")
                business['telefone'] = telefone_element.text if telefone_element else ""
            except NoSuchElementException:
                business['telefone'] = ""
            
            # Website
            try:
                website_element = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='authority']")
                business['website'] = website_element.get_attribute('href') if website_element else ""
            except NoSuchElementException:
                business['website'] = ""
            
            # Avaliação
            try:
                rating_element = self.driver.find_element(By.CSS_SELECTOR, "[jsaction*='rating']")
                business['avaliacao'] = float(rating_element.text.split()[0]) if rating_element else 0
            except (NoSuchElementException, ValueError):
                business['avaliacao'] = 0
            
            # Categoria
            try:
                categoria_element = self.driver.find_element(By.CSS_SELECTOR, "[jsaction*='category']")
                business['categoria'] = categoria_element.text if categoria_element else ""
            except NoSuchElementException:
                business['categoria'] = ""
            
            # Valores padrão
            business['numero_avaliacoes'] = 0
            business['horario_funcionamento'] = ""
            business['latitude'] = 0
            business['longitude'] = 0
            business['place_id'] = ""
            business['fotos'] = []
            
            return business
            
        except Exception as e:
            print(f"Erro ao extrair informações: {e}")
            return None
    
    def _format_opening_hours(self, opening_hours: Dict) -> str:
        """Formata horário de funcionamento"""
        if not opening_hours or 'weekday_text' not in opening_hours:
            return ""
        
        return "; ".join(opening_hours['weekday_text'])
    
    def _get_photo_urls(self, photos: List[Dict]) -> List[str]:
        """Obtém URLs das fotos"""
        urls = []
        for photo in photos[:3]:  # Máximo 3 fotos
            if 'photo_reference' in photo:
                url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key={Config.GOOGLE_MAPS_API_KEY}"
                urls.append(url)
        return urls
    
    def _run(self, search_term: str, location: str, radius: int = 10000, max_results: int = 50) -> str:
        """Executa a ferramenta e retorna resultado como string"""
        results = self.search_businesses(search_term, location, radius, max_results)
        return json.dumps(results, indent=2, ensure_ascii=False) 