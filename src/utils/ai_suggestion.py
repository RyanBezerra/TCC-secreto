"""
Sistema de IA para Sugestão de Aulas
Entende a pergunta do aluno e sugere aulas relevantes do banco de dados
"""

import re
from typing import List, Dict, Optional
from ..core.database import db_manager
from ..utils.logger import get_logger

logger = get_logger('ai_suggestion')

class AISuggestionEngine:
    """Motor de IA para sugestão de aulas baseado na pergunta do aluno"""
    
    def __init__(self):
        self.db_manager = db_manager
        
        # Palavras-chave e sinônimos para diferentes áreas
        self.subject_keywords = {
            'informatica': {
                'keywords': ['computador', 'pc', 'windows', 'pasta', 'arquivo', 'programação', 'python', 'java', 'html', 'css', 'javascript', 'software', 'hardware', 'internet', 'navegador', 'email', 'word', 'excel', 'powerpoint', 'sistema', 'aplicativo', 'programa', 'ferramenta', 'dispositivo'],
                'synonyms': ['tecnologia', 'digital', 'informática', 'computação']
            },
            'matematica': {
                'keywords': ['matemática', 'matematica', 'número', 'numero', 'soma', 'subtração', 'multiplicação', 'divisão', 'equação', 'álgebra', 'geometria', 'cálculo', 'estatística', 'probabilidade', 'fração', 'decimal', 'porcentagem', 'cálculos', 'números', 'operações', 'problemas', 'exercícios'],
                'synonyms': ['matemática', 'números', 'cálculos']
            },
            'portugues': {
                'keywords': ['português', 'portugues', 'gramática', 'gramatica', 'ortografia', 'redação', 'texto', 'leitura', 'escrita', 'literatura', 'poesia', 'prosa', 'verbos', 'substantivos', 'adjetivos', 'língua portuguesa', 'linguagem', 'comunicação', 'expressão'],
                'synonyms': ['português', 'linguagem', 'comunicação']
            },
            'ciencias': {
                'keywords': ['ciência', 'ciencia', 'física', 'fisica', 'química', 'quimica', 'biologia', 'geografia', 'história', 'historia', 'natureza', 'meio ambiente', 'ecologia', 'anatomia', 'botânica', 'zoologia', 'estudos', 'pesquisa', 'experimento', 'observação'],
                'synonyms': ['ciências', 'pesquisa', 'experimento']
            },
            'culinaria': {
                'keywords': ['culinária', 'culinaria', 'cozinha', 'receita', 'comida', 'alimento', 'temperar', 'tempero', 'cozinhar', 'assar', 'fritar', 'ferver', 'ingrediente', 'sabor', 'gastronomia', 'chef', 'prato', 'refeição'],
                'synonyms': ['gastronomia', 'cozinha', 'alimentação']
            }
        }
        
        # Padrões de perguntas comuns
        self.question_patterns = {
            'como_fazer': r'como\s+(fazer|criar|usar|aplicar|implementar|desenvolver|construir|gerar|produzir)',
            'o_que_e': r'o\s+que\s+é|o\s+que\s+são|definição|conceito|significado',
            'quero_aprender': r'quero\s+aprender|gostaria\s+de\s+aprender|preciso\s+aprender|desejo\s+aprender',
            'dificuldade': r'dificuldade|problema|não\s+consigo|não\s+entendo|não\s+sei\s+como',
            'exemplo': r'exemplo|exemplos|demonstração|mostrar|ilustrar'
        }
    
    def analyze_student_question(self, question: str) -> Dict:
        """Analisa a pergunta do aluno e extrai informações relevantes"""
        question_lower = question.lower().strip()
        
        analysis = {
            'original_question': question,
            'subject_area': self._identify_subject_area(question_lower),
            'question_type': self._identify_question_type(question_lower),
            'keywords': self._extract_keywords(question_lower),
            'intent': self._identify_intent(question_lower),
            'difficulty_level': self._estimate_difficulty(question_lower)
        }
        
        logger.info(f"Análise da pergunta: {analysis}")
        return analysis
    
    def _identify_subject_area(self, question: str) -> str:
        """Identifica a área de conhecimento da pergunta"""
        for subject, data in self.subject_keywords.items():
            for keyword in data['keywords'] + data['synonyms']:
                if keyword in question:
                    return subject
        return 'geral'
    
    def _identify_question_type(self, question: str) -> str:
        """Identifica o tipo de pergunta"""
        for pattern_name, pattern in self.question_patterns.items():
            if re.search(pattern, question):
                return pattern_name
        return 'geral'
    
    def _extract_keywords(self, question: str) -> List[str]:
        """Extrai palavras-chave relevantes da pergunta"""
        # Remover palavras comuns
        common_words = {'como', 'o', 'que', 'é', 'são', 'para', 'com', 'em', 'de', 'da', 'do', 'das', 'dos', 'um', 'uma', 'uns', 'umas', 'me', 'minha', 'meu', 'nossa', 'nosso', 'quero', 'gostaria', 'preciso', 'desejo', 'fazer', 'aprender', 'saber', 'entender'}
        
        # Dividir em palavras e filtrar
        words = re.findall(r'\b\w+\b', question)
        keywords = [word for word in words if len(word) > 2 and word not in common_words]
        
        return keywords[:5]  # Limitar a 5 palavras-chave mais relevantes
    
    def _identify_intent(self, question: str) -> str:
        """Identifica a intenção do aluno"""
        if any(word in question for word in ['como', 'fazer', 'criar', 'usar']):
            return 'tutorial'
        elif any(word in question for word in ['o que', 'definição', 'conceito']):
            return 'explicacao'
        elif any(word in question for word in ['quero', 'gostaria', 'preciso']):
            return 'aprendizado'
        elif any(word in question for word in ['exemplo', 'demonstração']):
            return 'exemplo'
        else:
            return 'geral'
    
    def _estimate_difficulty(self, question: str) -> str:
        """Estima o nível de dificuldade baseado na pergunta"""
        beginner_words = ['básico', 'iniciante', 'primeiro', 'começar', 'simples', 'fácil']
        advanced_words = ['avançado', 'complexo', 'difícil', 'profissional', 'especializado']
        
        if any(word in question for word in beginner_words):
            return 'iniciante'
        elif any(word in question for word in advanced_words):
            return 'avancado'
        else:
            return 'intermediario'
    
    def _get_available_areas(self) -> List[str]:
        """Retorna as áreas que têm aulas disponíveis no banco de dados"""
        try:
            # Buscar todas as aulas para identificar áreas disponíveis
            all_aulas = self.db_manager.get_all_aulas()
            available_areas = set()
            
            for aula in all_aulas:
                titulo = aula.get('titulo', '').lower()
                descricao = aula.get('descricao', '').lower()
                tags = aula.get('tags', '').lower()
                
                # Verificar se a aula pertence a alguma área conhecida
                for area, data in self.subject_keywords.items():
                    for keyword in data['keywords']:
                        if keyword in titulo or keyword in descricao or keyword in tags:
                            available_areas.add(area)
                            break
            
            return list(available_areas)
        except Exception as e:
            logger.error(f"Erro ao verificar áreas disponíveis: {e}")
            return ['informatica']  # Fallback para informática
    
    def suggest_lessons(self, question: str, max_results: int = 3) -> List[Dict]:
        """Sugere aulas baseadas na pergunta do aluno"""
        try:
            # Analisar a pergunta
            analysis = self.analyze_student_question(question)
            
            # Verificar se há aulas disponíveis na área identificada
            available_areas = self._get_available_areas()
            identified_area = analysis['subject_area']
            
            # Se a área identificada não tem aulas disponíveis, retornar vazio
            if identified_area != 'geral' and identified_area not in available_areas:
                logger.info(f"Área '{identified_area}' não tem aulas disponíveis")
                return []
            
            # Buscar aulas relevantes
            suggestions = []
            
            # Estratégia 1: Busca por palavras-chave principais (mais rigorosa)
            if analysis['keywords']:
                for keyword in analysis['keywords'][:2]:  # Usar apenas as 2 palavras mais relevantes
                    results = self.db_manager.search_aulas_keyword(keyword, limit=1)
                    # Filtrar resultados por relevância mínima
                    filtered_results = [r for r in results if r.get('relevance_score', 0) >= 3]
                    suggestions.extend(filtered_results)
            
            # Estratégia 2: Busca por área de conhecimento (apenas se a área for informática)
            if identified_area == 'informatica':  # Apenas informática tem aulas disponíveis
                subject_keywords = self.subject_keywords.get(identified_area, {}).get('keywords', [])
                for keyword in subject_keywords[:1]:  # Usar apenas 1 palavra da área
                    results = self.db_manager.search_aulas_keyword(keyword, limit=1)
                    filtered_results = [r for r in results if r.get('relevance_score', 0) >= 5]
                    suggestions.extend(filtered_results)
            
            # Estratégia 3: Busca pela pergunta completa (mais rigorosa)
            full_results = self.db_manager.search_aulas_keyword(question, limit=1)
            filtered_full_results = [r for r in full_results if r.get('relevance_score', 0) >= 5]
            suggestions.extend(filtered_full_results)
            
            # Remover duplicatas e ordenar por relevância
            unique_suggestions = self._remove_duplicates(suggestions)
            ranked_suggestions = self._rank_suggestions(unique_suggestions, analysis)
            
            # Filtrar por relevância mínima final
            final_suggestions = [s for s in ranked_suggestions if s.get('ai_score', 0) >= 5]
            
            # Adicionar explicação da sugestão
            for suggestion in final_suggestions[:max_results]:
                suggestion['ai_explanation'] = self._generate_explanation(suggestion, analysis)
                suggestion['match_reason'] = self._get_match_reason(suggestion, analysis)
            
            logger.info(f"Sugestões encontradas: {len(final_suggestions[:max_results])}")
            return final_suggestions[:max_results]
            
        except Exception as e:
            logger.error(f"Erro ao sugerir aulas: {e}")
            return []
    
    def _remove_duplicates(self, suggestions: List[Dict]) -> List[Dict]:
        """Remove sugestões duplicadas baseado no ID da aula"""
        seen_ids = set()
        unique_suggestions = []
        
        for suggestion in suggestions:
            aula_id = suggestion.get('id_aula')
            if aula_id and aula_id not in seen_ids:
                seen_ids.add(aula_id)
                unique_suggestions.append(suggestion)
        
        return unique_suggestions
    
    def _rank_suggestions(self, suggestions: List[Dict], analysis: Dict) -> List[Dict]:
        """Rankeia as sugestões baseado na relevância"""
        for suggestion in suggestions:
            score = 0
            
            # Score base
            score += suggestion.get('relevance_score', 0)
            
            # Bonus por área de conhecimento
            if analysis['subject_area'] != 'geral':
                titulo = suggestion.get('titulo', '').lower()
                descricao = suggestion.get('descricao', '').lower()
                tags = suggestion.get('tags', '').lower()
                
                subject_keywords = self.subject_keywords.get(analysis['subject_area'], {}).get('keywords', [])
                for keyword in subject_keywords:
                    if keyword in titulo:
                        score += 5
                    elif keyword in descricao or keyword in tags:
                        score += 2
            
            # Bonus por palavras-chave da pergunta
            for keyword in analysis['keywords']:
                titulo = suggestion.get('titulo', '').lower()
                if keyword in titulo:
                    score += 3
            
            suggestion['ai_score'] = score
        
        # Ordenar por score
        return sorted(suggestions, key=lambda x: x.get('ai_score', 0), reverse=True)
    
    def _generate_explanation(self, suggestion: Dict, analysis: Dict) -> str:
        """Gera uma explicação de por que a aula foi sugerida"""
        titulo = suggestion.get('titulo', 'Esta aula')
        
        explanations = []
        
        # Explicação baseada na área de conhecimento
        if analysis['subject_area'] != 'geral':
            area_names = {
                'informatica': 'informática',
                'matematica': 'matemática',
                'portugues': 'português',
                'ciencias': 'ciências'
            }
            area_name = area_names.get(analysis['subject_area'], analysis['subject_area'])
            explanations.append(f"Esta aula está relacionada à área de {area_name}")
        
        # Explicação baseada no tipo de pergunta
        if analysis['question_type'] == 'como_fazer':
            explanations.append("Esta aula ensina passo a passo como fazer")
        elif analysis['question_type'] == 'o_que_e':
            explanations.append("Esta aula explica conceitos e definições")
        elif analysis['question_type'] == 'quero_aprender':
            explanations.append("Esta aula é ideal para quem quer aprender")
        
        # Explicação baseada nas palavras-chave
        if analysis['keywords']:
            keywords_str = ', '.join(analysis['keywords'][:2])
            explanations.append(f"Esta aula aborda tópicos relacionados a: {keywords_str}")
        
        if explanations:
            return f"{titulo} foi sugerida porque: " + "; ".join(explanations) + "."
        else:
            return f"{titulo} pode ser útil para sua pergunta."
    
    def _get_match_reason(self, suggestion: Dict, analysis: Dict) -> str:
        """Retorna o motivo específico da correspondência"""
        titulo = suggestion.get('titulo', '').lower()
        
        # Verificar correspondência por palavras-chave
        for keyword in analysis['keywords']:
            if keyword in titulo:
                return f"Corresponde à palavra-chave: '{keyword}'"
        
        # Verificar correspondência por área
        if analysis['subject_area'] != 'geral':
            subject_keywords = self.subject_keywords.get(analysis['subject_area'], {}).get('keywords', [])
            for keyword in subject_keywords:
                if keyword in titulo:
                    return f"Corresponde à área de {analysis['subject_area']}"
        
        return "Correspondência geral com sua pergunta"

# Instância global do motor de IA
ai_suggestion_engine = AISuggestionEngine()

def suggest_lessons_for_student(question: str, max_results: int = 3) -> List[Dict]:
    """
    Função principal para sugerir aulas baseadas na pergunta do aluno
    
    Args:
        question: Pergunta do aluno
        max_results: Número máximo de sugestões
    
    Returns:
        Lista de aulas sugeridas com explicações da IA
    """
    return ai_suggestion_engine.suggest_lessons(question, max_results)

def analyze_student_question(question: str) -> Dict:
    """
    Analisa a pergunta do aluno e retorna informações sobre ela
    
    Args:
        question: Pergunta do aluno
    
    Returns:
        Dicionário com análise da pergunta
    """
    return ai_suggestion_engine.analyze_student_question(question)
