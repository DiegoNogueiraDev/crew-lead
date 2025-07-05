from crewai.tools import BaseTool
import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional
import time
from urllib.parse import urljoin, urlparse
from config import Config

class DataEnrichmentTool(BaseTool):
    """Ferramenta para enriquecer dados de leads com informações adicionais"""
    
    name: str = "DataEnrichment"
    description: str = "Ferramenta para enriquecer dados de leads com informações de contato e detalhes adicionais"
    
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def enrich_contact_info(self, lead_data: Dict) -> Dict:
        """
        Enriquece informações de contato de um lead
        
        Args:
            lead_data: Dados básicos do lead
            
        Returns:
            Dados enriquecidos do lead
        """
        enriched_data = lead_data.copy()
        
        try:
            # Enriquecer com informações do website
            if lead_data.get('website'):
                website_info = self._extract_website_info(lead_data['website'])
                enriched_data.update(website_info)
            
            # Buscar informações adicionais por nome e localização
            if lead_data.get('nome') and lead_data.get('endereco'):
                additional_info = self._search_additional_info(
                    lead_data['nome'], 
                    lead_data['endereco']
                )
                enriched_data.update(additional_info)
            
            # Validar e limpar dados
            enriched_data = self._validate_and_clean_data(enriched_data)
            
            return enriched_data
            
        except Exception as e:
            print(f"Erro ao enriquecer dados: {e}")
            return lead_data
    
    def _extract_website_info(self, website_url: str) -> Dict:
        """Extrai informações do website da empresa"""
        info = {}
        
        try:
            response = self.session.get(website_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar email
            emails = self._find_emails(soup, website_url)
            if emails:
                info['email'] = emails[0]
                info['emails_encontrados'] = emails
            
            # Buscar redes sociais
            social_media = self._find_social_media(soup)
            if social_media:
                info['redes_sociais'] = social_media
            
            # Buscar descrição da empresa
            description = self._find_company_description(soup)
            if description:
                info['descricao'] = description
            
            # Buscar telefones adicionais
            phones = self._find_additional_phones(soup)
            if phones:
                info['telefones_adicionais'] = phones
            
            # Buscar informações sobre a empresa
            company_info = self._find_company_info(soup)
            info.update(company_info)
            
            time.sleep(1)  # Delay para ser respeitoso com o servidor
            
        except requests.RequestException as e:
            print(f"Erro ao acessar website {website_url}: {e}")
        except Exception as e:
            print(f"Erro ao extrair informações do website: {e}")
        
        return info
    
    def _find_emails(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Busca emails no conteúdo da página"""
        emails = set()
        
        # Buscar emails no texto
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text_content = soup.get_text()
        found_emails = re.findall(email_pattern, text_content)
        emails.update(found_emails)
        
        # Buscar emails em links mailto
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))
        for link in mailto_links:
            email = link.get('href').replace('mailto:', '')
            emails.add(email)
        
        # Filtrar emails comuns de spam/placeholder
        spam_emails = ['example@example.com', 'test@test.com', 'admin@domain.com']
        emails = [email for email in emails if email.lower() not in spam_emails]
        
        return list(emails)
    
    def _find_social_media(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Busca links de redes sociais"""
        social_media = {}
        
        # Padrões para redes sociais
        patterns = {
            'facebook': r'facebook\.com/[^/\s]+',
            'instagram': r'instagram\.com/[^/\s]+',
            'linkedin': r'linkedin\.com/[^/\s]+',
            'twitter': r'twitter\.com/[^/\s]+',
            'youtube': r'youtube\.com/[^/\s]+',
            'whatsapp': r'wa\.me/[^/\s]+|whatsapp\.com/[^/\s]+'
        }
        
        # Buscar em links
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            for platform, pattern in patterns.items():
                if re.search(pattern, href, re.IGNORECASE):
                    social_media[platform] = href
                    break
        
        return social_media
    
    def _find_company_description(self, soup: BeautifulSoup) -> str:
        """Busca descrição da empresa"""
        # Buscar em meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')
        
        # Buscar em seções sobre/sobre nós
        about_sections = soup.find_all(['div', 'section'], 
                                     string=re.compile(r'sobre|about|quem somos', re.IGNORECASE))
        if about_sections:
            return about_sections[0].get_text(strip=True)[:500]
        
        # Buscar no primeiro parágrafo
        paragraphs = soup.find_all('p')
        if paragraphs:
            return paragraphs[0].get_text(strip=True)[:300]
        
        return ""
    
    def _find_additional_phones(self, soup: BeautifulSoup) -> List[str]:
        """Busca telefones adicionais no conteúdo"""
        phones = set()
        
        # Padrões para telefones brasileiros
        phone_patterns = [
            r'\(\d{2}\)\s?\d{4,5}-?\d{4}',  # (11) 99999-9999
            r'\d{2}\s?\d{4,5}-?\d{4}',      # 11 99999-9999
            r'\+55\s?\d{2}\s?\d{4,5}-?\d{4}' # +55 11 99999-9999
        ]
        
        text_content = soup.get_text()
        for pattern in phone_patterns:
            found_phones = re.findall(pattern, text_content)
            phones.update(found_phones)
        
        return list(phones)
    
    def _find_company_info(self, soup: BeautifulSoup) -> Dict:
        """Busca informações adicionais da empresa"""
        info = {}
        
        # Buscar CNPJ
        cnpj_pattern = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
        cnpj_match = re.search(cnpj_pattern, soup.get_text())
        if cnpj_match:
            info['cnpj'] = cnpj_match.group()
        
        # Buscar ano de fundação
        year_pattern = r'desde\s+(\d{4})|fundad[ao]\s+em\s+(\d{4})'
        year_match = re.search(year_pattern, soup.get_text(), re.IGNORECASE)
        if year_match:
            info['ano_fundacao'] = year_match.group(1) or year_match.group(2)
        
        return info
    
    def _search_additional_info(self, company_name: str, address: str) -> Dict:
        """Busca informações adicionais da empresa na web"""
        info = {}
        
        try:
            # Buscar no Google (simulado - em produção usar APIs específicas)
            search_query = f"{company_name} {address}"
            
            # Aqui você poderia integrar com APIs como:
            # - Google Custom Search API
            # - Bing Search API
            # - APIs de dados empresariais
            
            # Por enquanto, retornar informações básicas
            info['fonte_pesquisa'] = f"Pesquisa por: {search_query}"
            
        except Exception as e:
            print(f"Erro ao buscar informações adicionais: {e}")
        
        return info
    
    def _validate_and_clean_data(self, data: Dict) -> Dict:
        """Valida e limpa os dados enriquecidos"""
        cleaned_data = data.copy()
        
        # Validar email
        if 'email' in cleaned_data:
            email = cleaned_data['email']
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                del cleaned_data['email']
        
        # Limpar telefones
        if 'telefones_adicionais' in cleaned_data:
            phones = cleaned_data['telefones_adicionais']
            cleaned_phones = []
            for phone in phones:
                # Remover caracteres não numéricos exceto + ( )
                cleaned_phone = re.sub(r'[^\d+()-\s]', '', phone)
                if len(cleaned_phone) >= 10:  # Mínimo para um telefone válido
                    cleaned_phones.append(cleaned_phone)
            cleaned_data['telefones_adicionais'] = cleaned_phones
        
        # Limpar URLs de redes sociais
        if 'redes_sociais' in cleaned_data:
            for platform, url in cleaned_data['redes_sociais'].items():
                if not url.startswith('http'):
                    cleaned_data['redes_sociais'][platform] = 'https://' + url
        
        return cleaned_data
    
    def _run(self, lead_data: str) -> str:
        """Executa a ferramenta e retorna resultado como string"""
        import json
        
        # Converter string para dict se necessário
        if isinstance(lead_data, str):
            try:
                lead_data = json.loads(lead_data)
            except json.JSONDecodeError:
                return json.dumps({"erro": "Formato de dados inválido"}, ensure_ascii=False)
        
        enriched_data = self.enrich_contact_info(lead_data)
        return json.dumps(enriched_data, indent=2, ensure_ascii=False) 