# Azure Diagram Backend

Este proyecto proporciona un backend para generar diagramas de infraestructura de Azure. Está desarrollado en Python utilizando Flask y está desplegado en Vercel.

## Requisitos

- Python 3.x
- Flask
- Vercel CLI

## Instalación

. Crea un entorno virtual e instala las dependencias:
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta el servidor localmente:
    ```bash
    flask run
    ```

2. La API estará disponible en `http://localhost:5000`.

## Despliegue en Vercel

1. Instala Vercel CLI si aún no lo has hecho:
    ```bash
    npm install -g vercel
    ```

2. Inicia sesión en Vercel:
    ```bash
    vercel login
    ```

3. Despliega el proyecto en Vercel:
    ```bash
    vercel
    ```

4. Configura las variables de entorno en el dashboard de Vercel si es necesario.

## Endpoints

### `GET /`
Retorna un mensaje indicando que la API está en funcionamiento.

### `POST /generate-diagram`
Genera un diagrama de infraestructura de Azure basado en los recursos, relaciones y clusters proporcionados en el cuerpo de la solicitud.

**Ejemplo de solicitud:**
```json
{
  "resources": [
    {"name": "VM1", "type": "vm"},
    {"name": "VM2", "type": "vm"}
  ],
  "relationships": [
    {"source": "VM1", "target": "VM2"}
  ],
  "clusters": [
    {"name": "Cluster1", "resources": [{"name": "VM1", "type": "vm"}]}
  ]
}
