import os
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import re

class ExtractAccessKey:

    def __init__(self, pdf_path):
        self._pdf_path = pdf_path

    # Função para extrair texto de um PDF usando pdfplumber
    def _extract_text_from_pdf(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text

    # Função para extrair a chave de acesso do texto usando expressões regulares
    def _extract_chave_acesso(self, text):
        # Padrões típicos de chaves de acesso em notas fiscais
        regex_patterns = [
            r"\b\d{44}\b",   # 44 dígitos consecutivos
            r"\b\d{4}\.\d{4}\.\d{4}\.\d{4}\.\d{4}\.\d{4}\.\d{4}\.\d{4}\.\d{4}\b"  # Padrão com pontos
        ]

        found = False

        for pattern in regex_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                found = True
                chave_acesso = match.group(0)
                print(chave_acesso)

        if not found:
            print("Nenhuma correspondência de chave de acesso encontrada.")

    def get_access_key(self):
        # Dados de treinamento
        data = [
            ("chave de acesso:32243128152650000171660000035214931037084811", 1),
            ("Chave de acesso:33231260445437000146660010276929561035296465", 1),
            ("chave de acesso:32240228152650000171660000053712871058248335", 1),
            ("FATURAMENTO", 0),
            ("FATURA", 0),
            ("Fatura", 0),
        ]

        # Separando os dados em características (X) e rótulos (y)
        X, y = zip(*data)

        # Criando um vetorizador de palavras
        vectorizer = CountVectorizer()

        # Transformando os dados de treinamento em vetores
        X_vectorized = vectorizer.fit_transform(X)

        # Treinando um modelo de classificação (usando um classificador Naive Bayes como exemplo)
        classifier = MultinomialNB()
        classifier.fit(X_vectorized, y)

        # Exemplo de uso do modelo treinado com um arquivo PDF
        pdf_text = self._extract_text_from_pdf(self._pdf_path)
        pdf_text_vectorized = vectorizer.transform([pdf_text])

        prediction = classifier.predict(pdf_text_vectorized)[0]

        if prediction == 1:
            # Se a chave de acesso está presente, tenta extrair
            self._extract_chave_acesso(pdf_text)
        else:
            print("A chave de acesso não está presente na nota fiscal.")
