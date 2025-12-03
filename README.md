
# 🚕 Taxímetro Digital en Python

Este proyecto es un prototipo funcional de un **taxímetro digital moderno**, implementado en Python, como actividade del modulo 1 de la formación en IA con python de la Factoría F5 - Madrid.  

Permite calcular tarifas basadas en el tiempo que el taxi se encuentra **parado** o **en movimiento**, registrar historiales y configurar precios dinámicamente.

---

## 🎯 Objetivos del Proyecto

- Modernizar el sistema tradicional de taxímetros.
- Crear un sistema preciso, simple y fácil de expandir.
- Ofrecer una interfaz CLI clara para aprender programación paso a paso.
- Guardar el historial de trayectos.
- Permitir modificar las tarifas según necesidad.

---

## 🧩 Funcionalidades Principales

### 🟢 Nivel Esencial (CLI)
- Iniciar un trayecto (`start`)
- Cambiar estado a **parado** (`stop`)
- Cambiar estado a **en movimiento** (`move`)
- Finalizar trayecto (`finish`)
- Mostrar tarifa parcial (`show`)
- Salir del programa (`exit`)

### 🟠 Nivel Medio
- Guardar historial de trayectos en `history.txt`
- Configurar tarifas personalizadas mediante `rates.json`
- Ver tarifas actuales y modificarlas con el comando `rates`
- Consultar historial con el comando `history`

---

## 📦 Archivos importantes

| Archivo        | Descripción |
|----------------|-------------|
| `main.py`      | Lógica principal del taxímetro en CLI. |
| `rates.json`   | Archivo de configuración para tarifas personalizadas. |
| `history.txt`  | Registro histórico de viajes completados. |

---

## 🧠 ¿Cómo funciona el cálculo del taxímetro?

El sistema utiliza dos cronómetros:

- **⏱️ Tiempo parado** → tarifa por segundo más baja  
- **🚕 Tiempo en movimiento** → tarifa por segundo más alta  

Cada vez que el usuario cambia de estado, el programa calcula cuánto tiempo ha pasado desde el estado anterior y actualiza los contadores.

---

## ▶️ Cómo ejecutar el programa

1. Asegúrate de tener **Python 3** instalado.
2. Clona el repositorio:

```bash
git clone https://github.com/IrisFernandaAmorim/taximetro
cd taximetro

3. Ejecuta el programa:

python3 main.py


## Ejemplo de uso

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


🧪 Mejoras futuras

Interfaz gráfica (Tkinter o Qt)
Base de datos real (SQLite)
Sistema de GPS simulado
Versión móvil o web

🤝 Contribuciones

Este proyecto es educativo y abierto a mejoras.


🙋‍♀️ Autor

Iris Fernanda Amorim
Proyecto de aprendizaje y práctica de Python3.