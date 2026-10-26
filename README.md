# park-rms-lab

Prototipo de un Revenue Management System (RMS) para un complejo
de ocio con hotel y parque temático. Proyecto personal en desarrollo,
con datos sintéticos, para practicar forecasting de demanda, análisis
de pick-up y recomendación de tarifas con Python y SQL.

> Estado: en desarrollo (fase 0: planteamiento y estructura).

## Problema de negocio

En un complejo con parque y hoteles, la demanda depende de la
estacionalidad, los festivos, la meteorología, los eventos y la
antelación de reserva. Fijar tarifas "a ojo" implica perder ingresos
cuando hay demanda alta (precio demasiado bajo) o ocupación cuando es
baja (precio demasiado alto).

Preguntas que quiero responder con datos:

1. ¿Cuánta demanda se espera para cada fecha futura?
2. ¿Cómo va el pick-up (reservas acumuladas) frente al año anterior y
   al presupuesto, y cuándo es preocupante la desviación?
3. ¿Qué tarifa se debería recomendar según la demanda prevista,
   respetando suelos, techos y paridad?

## Alcance previsto

| Fase | Contenido |
|------|-----------|
| 0 | Planteamiento, estructura del repo, roadmap |
| 1 | Generador de datos sintéticos + esquema SQL |
| 2 | ETL y calidad de datos |
| 3 | Forecast: baseline vs Prophet vs XGBoost, con backtesting |
| 4 | Curvas de pick-up y alertas por desviación |
| 5 | Recomendador de tarifas con reglas de negocio |
| 6 | Dashboard, tests, CI y documentación |

## Datos

Todos los datos son **sintéticos**, generados con reglas de
estacionalidad y calendario. No se usa información de ninguna empresa real.

## Stack previsto

Python, SQL (SQLite/PostgreSQL), pandas, scikit-learn, Prophet,
XGBoost/CatBoost, Streamlit o FastAPI, Docker, GitHub Actions.

## Cómo ejecutarlo

Pendiente: se documentará en la fase 1.

## Licencia

MIT
