# 📘 DECISION_LOG.md

Este documento explica las decisiones técnicas más relevantes tomadas durante el desarrollo de la solución al desafío técnico de Crehana (Backend Developer).

---

## 📦 1. Elección del ORM: Tortoise ORM

- **Razón:** Se buscaba un ORM asincrónico compatible con FastAPI. Tortoise ORM es liviano, fácil de integrar y tiene buena documentación.
- **Ventajas:**
  - Soporte nativo para async/await
  - Generación automática de esquemas (`generate_schemas`)
  - Integración simple para pruebas usando SQLite en memoria

---

## 🧱 2. Arquitectura del proyecto

Se aplicó una estructura basada en **Clean Architecture**, con separación por capas:

- **`api/routes/`**: Orquestación de rutas HTTP
- **`services/`**: Servicios con lógica de negocio 
- **`infrastructure/database/models`**: Modelos ORM
- **`infrastructure/database/repositories`**: Acceso a datos
- **`domain/schemas/`**: Pydantic para validaciones
- **`core/`**: Configuración, seguridad, y utilidades

> Esta arquitectura facilita testeo, escalabilidad y mantenimiento.

---

## 🔐 3. Autenticación con JWT

- Se implementó un sistema básico de autenticación con:
  - Hashing de contraseñas (`passlib[bcrypt]`)
  - Generación y verificación de JWT (`python-jose`)
- **Campos protegidos:** Se incluye un `SECRET_KEY` configurable por entorno para firmar tokens.

---

## 🗂️ 4. Gestión de tareas

- CRUD completo de:
  - **Listas de tareas**
  - **Tareas dentro de listas**
- Se agregó soporte para:
  - Filtros por `completed` y `priority`
  - Cálculo automático del **porcentaje de completitud** de cada lista

---

## 👤 5. Asignación de tareas + notificación ficticia

- Se permite asignar usuarios a tareas por su correo electrónico.
- Se simula una notificación de envio de correo `Falsa` al asignar, tal como lo pedía el reto.

---

## ⚙️ 6. Docker + PostgreSQL

- Se incluyó un entorno completamente dockerizado con `docker-compose`.
- Se utiliza una base de datos real (PostgreSQL), aislada por contenedor.
- La aplicación es totalmente levantable con:
  ```bash
  docker compose -f docker/Docker-compose.yml up --build


### ✨ Conclusión
## Todas las decisiones fueron orientadas a:

- Mantener un código limpio, modular y testeable

- Seguir principios SOLID y DRY

- Cumplir los requisitos exactos del reto técnico