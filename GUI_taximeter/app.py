import streamlit as st
import time
import json
import os

# --- 1. CONFIGURACIÓN Y ARCHIVOS ---
RATES_FILE = "rates.json"
HISTORY_FILE = "history.txt"

# --- 2. FUNCIONES DE AYUDA (Tus herramientas) ---

def load_rates():
    # Si existe el archivo, lo leemos. Si no, usamos valores por defecto.
    if os.path.exists(RATES_FILE):
        with open(RATES_FILE, "r") as f:
            return json.load(f)
    return {"stopped": 0.02, "moving": 0.05}

def save_rates(rates):
    # Guardamos los precios en el archivo
    with open(RATES_FILE, "w") as f:
        json.dump(rates, f)

def save_trip_to_history(stopped_time, moving_time, total_fare):
    # Escribimos el viaje en el historial
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{time.ctime()} | Parado: {stopped_time:.1f}s | "
                f"Moviendo: {moving_time:.1f}s | Total: €{total_fare:.2f}\n")

# --- 3. LA "MOCHILA" (Session State) ---
# Aquí guardamos las cosas para que no se borren al pulsar botones.

if 'trip_active' not in st.session_state:
    st.session_state.trip_active = False  # ¿Está el taxi ocupado?
if 'state' not in st.session_state:
    st.session_state.state = "stopped"    # ¿Parado o moviéndose?
if 'last_time' not in st.session_state:
    st.session_state.last_time = 0.0      # Última vez que miramos el reloj
if 'total_stopped' not in st.session_state:
    st.session_state.total_stopped = 0.0  # Tiempo total parado acumulado
if 'total_moving' not in st.session_state:
    st.session_state.total_moving = 0.0   # Tiempo total moviéndose acumulado
if 'rates' not in st.session_state:
    st.session_state.rates = load_rates() # Cargamos las tarifas en la mochila

# --- 4. INTERFAZ GRÁFICA (Lo que ves en pantalla) ---

st.title("🚖 Taxímetro Digital Interactivo")

# BARRA LATERAL (Configuración)
st.sidebar.header("⚙️ Configuración")
st.sidebar.write("Ajusta los precios por segundo:")

# Usamos number_input para cambiar precios fácilmente
new_stopped_rate = st.sidebar.number_input("Precio Parado (€/s)", value=st.session_state.rates["stopped"], format="%.3f")
new_moving_rate = st.sidebar.number_input("Precio Moviendo (€/s)", value=st.session_state.rates["moving"], format="%.3f")

# Si cambian los números, actualizamos la mochila y el archivo
if new_stopped_rate != st.session_state.rates["stopped"] or new_moving_rate != st.session_state.rates["moving"]:
    st.session_state.rates["stopped"] = new_stopped_rate
    st.session_state.rates["moving"] = new_moving_rate
    save_rates(st.session_state.rates)
    st.sidebar.success("¡Tarifas actualizadas!")

# ÁREA PRINCIPAL
col1, col2 = st.columns(2)

# Lógica del Tiempo: Calcular cuánto tiempo pasó desde el último clic
if st.session_state.trip_active:
    current_time = time.time()
    delta = current_time - st.session_state.last_time
    
    # Sumamos el tiempo que pasó al acumulador correcto
    if st.session_state.state == "stopped":
        st.session_state.total_stopped += delta
    else:
        st.session_state.total_moving += delta
    
    # "Reiniciamos" el reloj para el siguiente tramo
    st.session_state.last_time = current_time

# Calcular precio actual
current_fare = (st.session_state.total_stopped * st.session_state.rates["stopped"] + 
                st.session_state.total_moving * st.session_state.rates["moving"])

# MOSTRAR DATOS EN PANTALLA
with col1:
    st.metric(label="💶 Precio Actual", value=f"€{current_fare:.2f}")
    st.metric(label="🚦 Estado", value="🟢 Moviendo" if st.session_state.state == "moving" else "🛑 Parado")

with col2:
    st.write(f"⏱️ **Tiempo Parado:** {st.session_state.total_stopped:.1f} s")
    st.write(f"⏱️ **Tiempo Moviendo:** {st.session_state.total_moving:.1f} s")

st.divider()

# BOTONES DE CONTROL
if not st.session_state.trip_active:
    # Botón verde grande para empezar
    if st.button("🏁 EMPEZAR CARRERA", type="primary", use_container_width=True):
        st.session_state.trip_active = True
        st.session_state.state = "stopped"
        st.session_state.last_time = time.time()
        st.session_state.total_stopped = 0.0
        st.session_state.total_moving = 0.0
        st.rerun() # Recarga la página para mostrar cambios
else:
    # Controles cuando la carrera está activa
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("Actualizar / Ver Costo 👁️"):
            # Al hacer clic, Streamlit corre el código de arriba y actualiza el tiempo
            pass 
            
    with c2:
        if st.session_state.state == "stopped":
            if st.button("🟢 Acelerar (Mover)"):
                st.session_state.state = "moving"
                st.rerun()
        else:
            if st.button("🛑 Frenar (Parar)"):
                st.session_state.state = "stopped"
                st.rerun()
                
    with c3:
        if st.button("💵 COBRAR Y FINALIZAR", type="primary"):
            save_trip_to_history(st.session_state.total_stopped, 
                                 st.session_state.total_moving, 
                                 current_fare)
            st.session_state.trip_active = False
            st.success(f"Viaje terminado. Total a cobrar: €{current_fare:.2f}")
            time.sleep(3) # Espera un poco para que leas el mensaje
            st.rerun()

# MOSTRAR HISTORIAL
st.divider()
if st.checkbox("📜 Ver Historial de Viajes"):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            st.text(f.read())
    else:
        st.info("Aún no hay viajes en el historial.")