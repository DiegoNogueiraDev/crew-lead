import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import os

class LeadDatabase:
    """Classe para gerenciar o banco de dados de leads"""
    
    def __init__(self, db_path: str = "leads.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Criar tabela de leads
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT,
                telefone TEXT,
                email TEXT,
                website TEXT,
                categoria TEXT,
                avaliacao REAL,
                numero_avaliacoes INTEGER,
                horario_funcionamento TEXT,
                latitude REAL,
                longitude REAL,
                termo_busca TEXT,
                localizacao_busca TEXT,
                data_captura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT
            )
        ''')
        
        # Criar tabela de campanhas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campanhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                termo_busca TEXT,
                localizacao TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'ativa'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_lead(self, lead: Dict) -> Optional[int]:
        """
        Salva um lead no banco de dados
        
        Args:
            lead: Dicionário com dados do lead
        
        Returns:
            ID do lead salvo
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO leads (
                nome, endereco, telefone, email, website, categoria,
                avaliacao, numero_avaliacoes, horario_funcionamento,
                latitude, longitude, termo_busca, localizacao_busca, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            lead.get('nome', ''),
            lead.get('endereco', ''),
            lead.get('telefone', ''),
            lead.get('email', ''),
            lead.get('website', ''),
            lead.get('categoria', ''),
            lead.get('avaliacao', 0.0),
            lead.get('numero_avaliacoes', 0),
            lead.get('horario_funcionamento', ''),
            lead.get('latitude', 0.0),
            lead.get('longitude', 0.0),
            lead.get('termo_busca', ''),
            lead.get('localizacao_busca', ''),
            lead.get('observacoes', '')
        ))
        
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return lead_id
    
    def get_leads(self, limit: Optional[int] = None, campaign_id: Optional[int] = None) -> List[Dict]:
        """
        Recupera leads do banco de dados
        
        Args:
            limit: Número máximo de leads a retornar
            campaign_id: ID da campanha para filtrar
        
        Returns:
            Lista de leads
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM leads ORDER BY data_captura DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        leads = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return leads
    
    def export_to_excel(self, filename: str, filter_term: Optional[str] = None) -> bool:
        """
        Exporta leads para arquivo Excel
        
        Args:
            filename: Nome do arquivo Excel
            filter_term: Termo para filtrar leads
        
        Returns:
            True se exportação foi bem-sucedida
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = "SELECT * FROM leads"
            if filter_term:
                query += f" WHERE termo_busca LIKE '%{filter_term}%'"
            query += " ORDER BY data_captura DESC"
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            # Garantir que o diretório existe
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)
            
            # Exportar para Excel
            df.to_excel(filename, index=False, engine='openpyxl')
            return True
            
        except Exception as e:
            print(f"Erro ao exportar para Excel: {e}")
            return False

# Função de conveniência para inicializar o banco
def init_database(db_path: str = "leads.db"):
    """Inicializa o banco de dados"""
    db = LeadDatabase(db_path)
    return db 