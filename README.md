# 🚕 Taxímetro Digital en Python  
**Versión CLI + GUI (Streamlit)**

Este proyecto es un **taxímetro digital moderno**, desarrollado en Python como actividad del Módulo I de la formación en IA con Python en la Factoría F5 – Madrid.

Incluye dos implementaciones completas:

- **CLI_taximeter** → versión de consola para aprender lógica paso a paso  
- **GUI_taximeter** → versión gráfica interactiva construida con **Streamlit**

Ambos sistemas permiten calcular tarifas en función del tiempo parado o en movimiento, almacenar el historial y configurar precios dinámicamente.

## 📁 Estructura del Proyecto

```
PROYECTO1_IRIS_AMORIM/
│
├── CLI_taximeter/
│   ├── main.py             # Versión en consola (CLI)
│   ├── rates.json          # Tarifas configurables
│   ├── history.txt         # Historial CLI
│   └── taximeter.log       # Log del sistema en CLI
│
├── GUI_taximeter/
│   ├── app.py              # Aplicación Streamlit (GUI)
│   ├── rates.json          # Tarifas GUI
│   ├── history.txt         # Historial GUI
│   ├── requirements.txt    # Dependencias para la GUI
│   └── taximeter_gui.log   # Log del sistema en GUI
│
├── .gitignore
└── README.md
```

📌 *La CLI y la GUI funcionan de manera independiente*, cada una con sus propios archivos de tarifas e historial.


## 🎯 Objetivos del Proyecto

- Modernizar el funcionamiento tradicional de un taxímetro.  
- Proporcionar un sistema **preciso, simple y ampliable**.  
- Registrar historiales de viajes.  
- Permitir tarifas configurables por el usuario.
- Añadir trazabilidad mediante logging.


## 🧩 Funcionalidades Principales

### 🟢 CLI (Versión Esencial)

Comandos disponibles:

- `start` → iniciar viaje  
- `stop` → marcar estado **parado**  
- `move` → marcar estado **moviendo**  
- `finish` → finalizar viaje  
- `show` → mostrar coste parcial  
- `rates` → ver/modificar tarifas  
- `history` → ver historial  
- `exit` → salir  

### 🟣 GUI (Versión Avanzada en Streamlit)

La interfaz gráfica permite:

- Iniciar o finalizar una carrera con botones.  
- Cambiar entre estados **🛑 parado** y **🟢 moviendo**.  
- Ver el coste actualizado en tiempo real.  
- Ver contadores de tiempo parado/moviendo.  
- Ajustar tarifas desde la barra lateral.  
- Guardar viajes automáticamente en `history.txt`.  
- Leer el historial desde la propia aplicación.  
- Registrar eventos en `taximeter_gui.log`.


## 📦 Archivos importantes

| Archivo             | Ubicación        | Descripción                                        |
| ------------------- | ---------------- | -------------------------------------------------- |
| `main.py`           | `/CLI_taximeter` | Implementación del taxímetro en terminal.          |
| `app.py`            | `/GUI_taximeter` | Aplicación Streamlit con interfaz gráfica.         |
| `rates.json`        | En cada módulo   | Tarifas personalizadas de “parado” y “movimiento”. |
| `history.txt`       | En cada módulo   | Registro de viajes realizados.                     |
| `taximeter.log`     | `/CLI_taximeter` | Registro de logs de la versión CLI.                |
| `taximeter_gui.log` | `/GUI_taximeter` | Registro de logs de la versión GUI.                |
| `requirements.txt`  | `/GUI_taximeter` | Dependencias necesarias para ejecutar la GUI.      |


## 🧠 ¿Cómo funciona el cálculo del taxímetro?

El sistema calcula el precio total mediante dos cronómetros:

- **Tiempo Parado** → tarifa baja (€/s)  
- **Tiempo en Movimiento** → tarifa alta (€/s)

Cada vez que el estado cambia, se calcula el tiempo transcurrido desde la última marca y se suma al contador correspondiente.

Fórmula del coste total:
```
total = (tiempo_parado * tarifa_parado)
+ (tiempo_moviendo * tarifa_movimiento)
```


## ▶️ Cómo ejecutar el proyecto

### 🟢 Modo CLI

**1.** Instala Python 3  
**2.** Clona el repositorio:
```
git clone https://github.com/Bootcamp-IA-P6/Proyecto1_Iris_Amorim
cd Proyecto1_Iris_Amorim/CLI_taximeter
```

**3.** Ejecuta:
```
python3 main.py
```

### 🟣 Modo GUI (Streamlit)

**1.** Entra en la carpeta GUI:
```
cd GUI_taximeter
```

**2.** (Opcional) Activa el entorno virtual:
```
source .venv/bin/activate      # macOS / Linux  
.\.venv\Scripts\activate       # Windows
```

**3.** Instala dependencias:
```
pip install -r requirements.txt
```

**4.** Ejecuta la aplicación:
```
streamlit run app.py
```

## 💻 Ejemplo de uso (CLI)
```
> start
Trip started. Current state: 'stopped'.

> move
State changed to 'moving'.

> show
Current fare: €0.25

> finish
--- Trip Summary ---
Stopped time : 3.2 seconds
Moving time  : 12.5 seconds
Total fare   : €0.73
```

## 🧪 Mejoras futuras

- Conexión con base de datos (SQL)
- Simulación de GPS o velocidad
- Dashboard analítico de viajes
- Versión móvil / web avanzada
- Exportación del historial en PDF o CSV

## 🤝 Contribuciones

Proyecto educativo, abierto a sugerencias y mejoras.

## 🙋‍♀️ Autora

Iris Fernanda Amorim

Proyecto práctico de aprendizaje de Python.


