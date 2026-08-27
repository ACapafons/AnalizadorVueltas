# 🏎️ Analizador de Vueltas — Motorsport Telemetry Tool

Herramienta de análisis de telemetría básica para sesiones de carreras.  
Carga datos de clasificación desde archivos CSV y analiza el rendimiento de pilotos.

> **Sesión de ejemplo incluida**: Clasificación del GP de Mónaco 2023 — Fórmula 1

---

## 📊 Funcionalidades

### 🔹 Entrada de datos
- Lee archivos **CSV** con datos detallados de cada vuelta
- Detecta automáticamente los CSV de la misma carpeta

### 🔹 Análisis
- ⚡ **Vuelta más rápida** de la sesión: tiempo, piloto, equipo y neumáticos
- 📊 **Estadísticas por piloto**: mejor vuelta y tiempo promedio
- 🔮 **Vuelta ideal**: suma de los mejores sectores individuales de toda la sesión
- ⏱️ **Diferencias respecto a la pole**: gap de cada piloto

### 🔹 Sesiones
- Filtra el análisis por **Q1, Q2, Q3** o analiza todo de golpe

---

## 🗂️ Formato del CSV

```csv
piloto,numero,equipo,sesion,vuelta,tiempo,sector1,sector2,sector3,neumaticos
Verstappen,1,Red Bull Racing,Q3,2,1:11.365,19.598,37.712,14.055,Blando
Alonso,14,Aston Martin,Q3,2,1:11.449,19.523,37.621,14.305,Blando
```

| Columna     | Descripción                            |
|-------------|----------------------------------------|
| `piloto`    | Apellido del piloto                    |
| `numero`    | Número de coche                        |
| `equipo`    | Nombre del equipo                      |
| `sesion`    | Q1 / Q2 / Q3                          |
| `vuelta`    | Número de vuelta en esa sesión         |
| `tiempo`    | Tiempo total en formato `m:ss.mmm`     |
| `sector1`   | Tiempo sector 1 en segundos            |
| `sector2`   | Tiempo sector 2 en segundos            |
| `sector3`   | Tiempo sector 3 en segundos            |
| `neumaticos`| Compuesto usado (Blando/Medio/Duro)    |

---

## 🚀 Uso

```bash
python analizador.py
```

No requiere ninguna librería externa, solo Python 3.

---

## 📁 Estructura del proyecto

```
AnalizadorVueltas/
├── analizador.py          # Script principal
├── monaco_2023_qualy.csv  # Datos reales GP Mónaco 2023 - Clasificación
└── README.md
```

---

## 🏁 Resultado de la Clasificación — GP Mónaco 2023

| Pos | Piloto      | Equipo            | Q3          |
|-----|-------------|-------------------|-------------|
| 1   | Verstappen  | Red Bull Racing   | 1:11.365 🏆 |
| 2   | Alonso      | Aston Martin      | 1:11.449   |
| 3   | Leclerc     | Ferrari           | 1:11.471   |
| 4   | Ocon        | Alpine            | 1:11.553   |
| 5   | Sainz       | Ferrari           | 1:11.630   |
| 6   | Hamilton    | Mercedes          | 1:11.725   |
| 7   | Gasly       | Alpine            | 1:11.933   |
| 8   | Russell     | Mercedes          | 1:11.964   |
| 9   | Tsunoda     | AlphaTauri        | 1:12.082   |
| 10  | Norris      | McLaren           | 1:12.254   |

> Nota: Leclerc recibió una penalización de 3 posiciones en parrilla por obstruir a Norris en Q3.
