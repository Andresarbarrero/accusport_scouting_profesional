<p align="center">
  <img src="https://github.com/Andresarbarrero/accusport_scouting_profesional/blob/main/img/Logo%20ORG.jpg" alt="AccuSport Logo" width="160px">
</p>

<p align="center">
  <img src="https://github.com/Andresarbarrero/accusport_scouting_profesional/blob/main/img/Banner%20ORG.png" alt="AccuSport Scouting Banner" width="100%">
</p>

# ⚽ AccuSport Scouting System  
**Plataforma profesional de análisis, registro y seguimiento de futbolistas – AccuSport Colombia**

Este repositorio contiene el desarrollo completo del **AccuSport Scouting System**, una plataforma tecnológica integral diseñada para profesionalizar el scouting y análisis futbolístico en Colombia, Latinoamérica y el mundo.
Su objetivo es unir metodologías modernas de observación, herramientas tecnológicas de análisis, bases de datos escalables, formularios inteligentes, dashboards interactivos y reportería profesional en un solo ecosistema técnico.
---

# 🚀 Propósito del Proyecto

AccuSport System nace para resolver una necesidad crítica:

Centralizar, estandarizar y profesionalizar el proceso de scouting y análisis de jugadores con un enfoque moderno y global.
 
Los objetivos principales son:

- Registrar jugadores, equipos, competencias y partidos con estructura profesional.  
- Estandarizar el proceso de observación en vivo, por video y mediante plataformas tecnológicas.  
- Integrar carga manual vía formularios y carga masiva mediante Excel.  
- Almacenar toda la información en una base de datos en la nube altamente escalable (PostgreSQL + Railway).  
- Permitir análisis modernos mediante dashboards interactivos y perfiles profesionales.  
- Generar reportes automáticos y plantillas listas para publicar en redes sociales (LinkedIn, Instagram, etc.).  
- Servir como herramienta central de AccuSport Colombia para scouting profesional y cómo una base para scouts, clubes, agencias y analistas en múltiples regiones del mundo.

---
# 🌍 Enfoque Global: Scouting Mundial con Tecnología

AccuSport System combina **scouting tradicional presencial** con **scouting digital moderno**, utilizando herramientas avanzadas como:

- **WyScout**  
- **InStat**  
- **SICS VideoMatch**  
- **Hudl**  
- **BePro / Veo**  
- **FBref / Opta-like data (según disponibilidad futura)**  

Además, incorpora un módulo de análisis contextual mediante la **API de football-data.org**, lo que permite:

- Consultar ligas de todo el mundo  
- Acceder a partidos, resultados y calendarios  
- Crear reportes automáticos de contexto competitivo  
- Guardar estos reportes en la base de datos  

Este enfoque permite trabajar **con ligas locales, regionales y también con ligas internacionales en Europa, Asia, África y América**.

---

# 📘 Base Conceptual: Guía Completa de Scouting en Fútbol

Este proyecto está fundamentado en una metodología integral basada en análisis técnico, táctico, físico, psicológico y biomecánico.

---

## 🎯 1. Dimensiones del Análisis de un Futbolista

### **✔ Técnica**
- Conducción  
- Control orientado  
- Pase corto y largo  
- Centros  
- Tiro y definición  
- Primer toque  

### **✔ Táctica**
- Toma de decisiones  
- Lectura de juego  
- Movilidad sin balón  
- Ubicación por fases  
- Asociación  
- Transiciones  

### **✔ Física**
- Velocidad  
- Aceleración  
- Potencia  
- Resistencia  
- Agilidad  
- Fuerza en duelos  

### **✔ Psicológica / Mental**
- Personalidad  
- Liderazgo  
- Intensidad  
- Concentración  
- Competitividad  
- Inteligencia emocional  

### **✔ Biomecánica**
- Altura, peso, somatotipo  
- Técnica de carrera  
- Edad biológica vs edad cronológica  

---

## 🧠 2. Modelo de Observación Moderno

Integrando las **cuatro fases del juego**:

1. Fase ofensiva  
2. Transición defensa–ataque  
3. Fase defensiva  
4. Transición ataque–defensa  

Cada jugador se evalúa según su impacto en estas fases.

---

# 📊 3. KPIs Fundamentales (Versión Inicial)

Para esta primera etapa del proyecto escogimos un conjunto de **métricas clave** que son:

- Fundamentales en el scouting moderno  
- Posibles de medir desde tu BD actual  
- Atractivas visualmente para dashboards y redes  
- Escalables para futuras métricas avanzadas  

## KPIs que sí maneja AccuSport desde la V1:
**Generales**  
- Partidos jugados  
- Minutos jugados  
- Goles  
- Asistencias  
- Tiros totales  
- Tiros al arco  
- Pases completados  
- Centros intentados / completados  
- Duelos ganados / perdidos  
- Tarjetas  

**Defensivos**  
- Intercepciones  
- Entradas ganadas  
- Despejes  
- Bloqueos  

**Ofensivos**  
- Regates intentados / exitosos  
- Ocasiones creadas  

**Valoraciones (1–5)**  
- Técnica  
- Táctica  
- Física  
- Mental  

**Potencial (categorías estándar)**  
- Bajo – Medio – Alto – Elite  
---

## 🥇 4. Análisis por Posición (Versión futura)

### **Porteros**
- Juego aéreo  
- 1v1  
- Atajadas  
- Inicio de juego  

### **Defensas**
- Perfilamiento  
- Timing defensivo  
- Salida limpia  
- Duelos  

### **Mediocampistas**
- Visión  
- Progresiones  
- Coberturas  
- Asociación  

### **Extremos / Interior Ofensivo**
- Regate 1v1  
- Velocidad  
- Centros  
- Desmarque  

### **Delanteros**
- Definición  
- Movimientos  
- Presión alta  
- Juego de espaldas  

---


# 🧱 Arquitectura del Sistema

## Backend
- **Lenguaje:** Python  
- **Base de datos:** PostgreSQL (Railway Cloud)  
- **Librerías:** psycopg2, SQLAlchemy  
- **Módulos:**  
  - Carga de Excel → BD  
  - Validación y actualización de jugadores  
  - Integración API football-data.org  

## Frontend (App)
- **Framework:** Streamlit  
- **Módulos principales:**  
  - Registro de jugadores  
  - Edición de perfiles  
  - Carga de informes  
  - Dashboard de análisis  
  - Módulo API internacional  

## Infraestructura
- Railway → Base de datos  
- Streamlit Cloud → Despliegue  
- GitHub → Versionamiento  

---

# 🗂 Modelo de Datos

## Tablas principales:

| Tabla | Descripción |
|-------|-------------|
| players | Información del jugador (perfil, físico, atributos) |
| teams | Clubes o academias |
| leagues | Ligas nacionales e internacionales |
| matches | Partidos y calendarios |
| stats | Estadísticas por partido |
| scouting_reports | Informes detallados|
| api_context_reports | Reportes automáticos de la API |

---
# 🌐 Módulo Internacional – API football-data.org

Este módulo permite:

- Seleccionar una liga del mundo  
- Consultar temporadas y partidos  
- Generar un **reporte automático** con:  
  - Resultado  
  - Equipos  
  - Fecha  
  - Resumen interpretado  
- Añadir comentarios manuales del usuario  
- Guardarlo en la base de datos como **contexto competitivo**  

---

# 🔧 Conexión a PostgreSQL – Railway

```python
import psycopg2
import os

connection = psycopg2.connect(
    host=os.getenv("PGHOST"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    database=os.getenv("PGDATABASE"),
    port=os.getenv("PGPORT")
)
```
# 🛠 Instalación Local

```bash
git clone https://github.com/usuario/accusport-scouting-system.git
cd accusport-scouting-system
pip install -r requirements.txt
streamlit run streamlit_app/Main.py 
```

# 🌐 Visión a Futuro

- Dashboards avanzados
- Comparador de jugadores profesional
- Reportes PDF automáticos
- Módulo multiusuario
- Machine Learning para predicción de talento
- Integraciones con APIs premium
- Panel para clubes y agencias
 
# 👨‍💻 Autor

Andrés Barrero
Analista – Scout – Desarrollador de herramientas deportivas
Colombia 🇨🇴

# ⭐ Contribuciones

Aportes, sugerencias y mejoras son bienvenidas.

# 📄 Licencia

MIT License
