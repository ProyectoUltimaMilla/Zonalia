# Imagen de la API de Zonalia (issue #6). Instala el paquete de servicios/ y arranca uvicorn.
FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .

RUN useradd --create-home zonalia
USER zonalia

EXPOSE 8000
CMD ["uvicorn", "zonalia.api.main:app", "--host", "0.0.0.0", "--port", "8000"]