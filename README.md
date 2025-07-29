# Registro de Actividades Diario - WebApp Flask

# 📝 Registro de Actividades Diario - WebApp Flask

Aplicación web sencilla desarrollada con **Flask** para registrar actividades laborales diarias, organizar tareas por grupo, visualizar un historial mensual y facilitar el seguimiento del trabajo personal o en equipo reducido.

---

## 🎯 Propósito

Reemplazar el uso de planillas Excel manuales, permitiendo un registro más limpio, accesible y eficiente de las tareas diarias.

---

## ⚙️ Tecnologías utilizadas

| Componente       | Tecnología            | Justificación                       |
|------------------|------------------------|-------------------------------------|
| Backend          | Flask (Python)         | Ligero y rápido para MVP            |
| Base de datos    | SQLite + SQLAlchemy    | Persistencia local simple y portátil |
| Autenticación    | Flask-Login            | Manejo seguro de sesiones           |
| Frontend         | HTML + Bootstrap 5     | Interfaz limpia, sin JS complejo    |
| Motor de plantillas | Jinja2              | Nativo en Flask                     |

---

## 🚀 Funcionalidades principales

- Registro y autenticación de usuarios.
- Crear, editar y eliminar **actividades laborales** por fecha.
- Clasificación por **grupos de tareas** personalizados por usuario.
- Visualización mensual de actividades.
- Exportación de actividades del mes a Excel (`.xlsx`).
- Interfaz adaptable y simple de usar.

---

## 📸 Captura de pantalla

*Próximamente*

---

## 🧪 Instalación local

```bash
# Clona el repositorio
git clone https://github.com/AlexPerez7/RegistrApp.git
cd RegistrApp

# Crea entorno virtual (opcional pero recomendado)
python -m venv .venv
.venv\Scripts\activate  # En Windows

# Instala dependencias
pip install -r requirements.txt

# Ejecuta la app
python app.py
