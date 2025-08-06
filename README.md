# 🧠 Api Task Backend - Task Manager API

Este proyecto es una solución al desafío técnico propuesto por Crehana para el rol de **Backend Developer**, utilizando **Python + FastAPI** y aplicando una arquitectura limpia y escalable.

---

## 🚀 Tecnologías utilizadas

- **FastAPI** (Framework principal)
- **Tortoise ORM** (ORM asincrónico)
- **PostgreSQL** (Base de datos relacional)
- **JWT** (Autenticación)
- **Docker + Docker Compose** (Entorno de desarrollo)
- **Pytest** (Testing)
- **Flake8 + Black** (Estilo y calidad de código)

---

## 📁 Estructura del proyecto

```bash
app/
├── api/                  # Rutas (Controllers)
├── core/                 # Configuración y seguridad
├── domain/               # Esquemas de Pydantic
├── infrastructure/
│   └── database/
│       ├── models/       # Modelos Tortoise
│       └── repositories/ # Acceso a datos (repositorios)
├── services/             # Servicios con lógica de negocio
├── main.py               # Punto de entrada de la app
docker/
│   └── docker-compose.yml # Configuración Docker
│   └── Dockerfile/       # Imagen de la app
tests/                    # Pruebas unitarias e integración
.env                      # Variables de entorno
```

---
## 🛠️ Instalación en entorno local

### 1. Clona el repositorio
```
git clone https://github.com/JulianRp2177/api-task-manager.git
cd api-task
```
### 2. Crea y activa un entorno virtual

```
python3 -m venv venv
source venv/bin/activate  

```

### 3. Instala las dependencias

```
pip install -r requirements.txt

```

### 4. Crea el archivo .env en la raíz del proyecto
Este archivo es requerido para que la aplicación funcione correctamente

```
cd api-task
touch .env
```
Agrega las variables de entorno correspondientes

```
DATABASE_URL=postgres://postgres:postgres@db:5432/crehana_db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUGGER=False
```


### 5. 🐳 Ejecución con Docker
Debes tener instalado:

-   Docker

-   Docker Compose

Si no lo tienes, puedes instalarlo desde: https://docs.docker.com/get-docker/

 Ejecutar con Docker Compose

```
docker compose -f docker/Docker-compose.yml up --build
```
🔗 Accede a la documentación Swagger en http://localhost:8000/docs

Esto levantará un contenedor con FastAPI y base de datos SQLite.

---

## 📋 Endpoints principales
### 🔐 /auth
- POST /register: Registrar nuevo usuario

- POST /login: Login con JWT

### 📋 /task
- POST /lists: Crear lista de tareas

- GET /lists: Ver todas las listas

- GET /lists/{id}: Ver lista con tareas y % de completitud

- POST /lists/{id}/tasks: Crear tarea en lista

- GET /lists/{id}/tasks?completed=true&priority=3: Filtros por estado/prioridad

- PATCH /tasks/{id}: Actualizar tarea

- DELETE /tasks/{id}: Eliminar tarea

### 👤 /assigned_task
- POST /{task_id}: Asignar tarea a usuario (simula envío de email con print())

---
## 🧪 Ejecutar pruebas

### 1. Activa tu entorno virtual

```
source venv/bin/activate
```
### 2. Ejecuta todos los tests desde la terminal

```
pytest
```

### 3. Con reporte de cobertura
```
pytest --cov=app --cov-report=term-missing
```

---
## 🔍 Linter y formato de código

### 1. Formatear con black
```
black app/
```

### 2. Verificar con flake8

## Configuración de .flake8
```
[flake8]
exclude = .venv,__pycache__,migrations, venv
max-line-length = 88
ignore = E203, W503

```
## verificación
```
flake8 .
```

---

## 🐞 Debugging remoto con debugpy (modo seguro)
La aplicación permite activar el debugger debugpy para conectarte desde VS Code de manera segura y controlada.

### ✅ ¿Cómo activarlo?
En el archivo .env, establece la variable:

```
DEBUGGER=True
```

Al iniciar la aplicación, si el proceso cumple las condiciones de seguridad, verás:
```
⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳
```

- Tener en cuenta en la raiz del proyecto hay un archivo launch.json con la configuracion debe copiarse a la carpeta .vscode del depurador creando un archivo Python Debugger

---

## 📄 Licencia

MIT © 2025 - JULIAN RODRIGUEZ
