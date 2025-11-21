<p align="center">
  <img src="https://drive.google.com/file/d/1V5uYyZskpJcseOxHpAkq_p6iPCQ4dkAU/view?usp=sharing" alt="AccuSport Logo" width="160px">
</p>

<p align="center">
  <img src="https://drive.google.com/file/d/1H3F6j81pJaP-g1O07QdBppXVQuickddx/view?usp=sharin"AccuSport_Scoutin.png" alt="AccuSport Scouting Banner" width="100%">
</p>

# ⚽ AccuSport Scouting System  
**Plataforma profesional de análisis, registro y seguimiento de futbolistas – AccuSport Colombia**

Este repositorio contiene el desarrollo completo del **AccuSport Scouting System**, una plataforma tecnológica avanzada diseñada para profesionalizar el análisis y scouting de futbolistas en Colombia y Latinoamérica.  
El sistema combina metodologías modernas de scouting, análisis de datos, dashboards interactivos y un backend escalable en la nube.

---

# 🚀 Propósito del Proyecto

El objetivo principal del sistema es:
 
- Estandarizar el proceso de observación y análisis de futbolistas.
- Registrar jugadores, equipos, ligas, partidos y métricas clave.
- Integrar formularios para carga manual o importación vía Excel.
- Almacenar todo en una base de datos en la nube (PostgreSQL + Railway).
- Facilitar la creación de reportes profesionales automáticos.
- Permitir compartir perfiles de jugadores en LinkedIn y redes.
- Servir como herramienta central de AccuSport Colombia para scouting profesional.

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

## 📊 3. KPIs Modernos Integrados

- xThreat  
- Acciones progresivas  
- Heatmaps  
- Duelos ganados  
- Recuperaciones por zona  
- Acciones por 90’  
- Expected Play Contribution  
- Indicadores técnico–tácticos  
- Índices de rendimiento por posición  

---

## 🥇 4. Análisis por Posición

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

### **Backend**
- Lenguaje: **Python**  
- Base de datos: **PostgreSQL (Railway Cloud)**  
- Scripts de carga:
  - Importación de Excel → PostgreSQL  
  - Carga de jugadores  
  - Conexión vía psycopg2 / SQLAlchemy  

### **Frontend**
- **Streamlit**  
- Formularios interactivos  
- Visualización gráfica  
- Dashboard modular  

### **Infraestructura**
- Railway para la BD  
- Streamlit Cloud para despliegue  
- GitHub para versionamiento  

---

# 🗂 Modelo de Datos

Tablas principales:

| Tabla | Descripción |
|-------|-------------|
| `players` | Datos del jugador |
| `teams` | Club o academia |
| `leagues` | Liga o competencia |
| `matches` | Información de los partidos |
| `stats` | Métricas del rendimiento |
| `scouting_reports` | Informes detallados |

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

# 🛠 Instalación Local
git clone https://github.com/usuario/accusport-scouting-system.git
cd accusport-scouting-system
pip install -r requirements.txt
streamlit run streamlit_app/Main.py 

```

# 🌐 Visión a Futuro

Reportes PDF automáticos

Comparador de jugadores

Panel para clubes/agentes

Machine Learning para predicción de talento

Integración con APIs (Wyscout, InStat, FBref)

Módulo multiusuarios

Tableros profesionales y responsivos

# 👨‍💻 Autor

Andrés Barrero
Analista – Scout – Desarrollador de herramientas deportivas
Colombia 🇨🇴

# ⭐ Contribuciones

Aportes, sugerencias y mejoras son bienvenidas.

# 📄 Licencia

MIT License
