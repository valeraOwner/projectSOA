# Usa una imagen base de Python
FROM python:3.11-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt y instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de tu aplicación al contenedor
COPY . .

# Establece la ruta base de Python para que pueda importar desde /app
ENV PYTHONPATH=/app

# Expone el puerto en el que Flask escuchará
EXPOSE 5400

# Comando para ejecutar la aplicación Flask
# Asegúrate de que 'app.py' sea tu archivo principal de Flask
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5400"]