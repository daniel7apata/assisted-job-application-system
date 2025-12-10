# Imagen base ligera de Python
FROM public.ecr.aws/lambda/python:3.11

# Copia archivos al contenedor
COPY . .

# Instala dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Establece el handler de Lambda
CMD ["main.handler"]

