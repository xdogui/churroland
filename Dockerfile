# Imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la app
COPY . .

# Exponer el puerto (Fly asigna 8080)
EXPOSE 8080

# Comando para correr la app con gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
