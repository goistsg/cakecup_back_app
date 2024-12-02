# Imagem base
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para Python e PyNest
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PYNEST_ENV=development

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala o PyNest e outras dependências
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pynest-api

# Copia o código do projeto
COPY . .

# Script de inicialização
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expõe a porta
EXPOSE $PORT

# Usa o script de entrypoint para inicialização
ENTRYPOINT ["docker-entrypoint.sh"]

# Comando padrão (pode ser sobrescrito)
CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8000", "--reload"] 