import streamlit as st
import time
import json
import os

# SETTINGS FILES
RATES_FILE = "rates.json"
HISTORY_FILE = "history.txt"

# HELPER FUNCTIONS (our tools)

def load_rates():
    ''' If the file exists, read it. If not, use default values. '''
    if os.path.exists(RATES_FILE):
        with open(RATES_FILE, "r") as f:
            return json.load(f)
    return {"stopped": 0.02, "moving": 0.05}

def save_rates(rates):
    ''' Save the prices into the file '''
    with open(RATES_FILE, "w") as f:
        json.dump(rates, f)

def save_trip_to_history(stopped_time, moving_time, total_fare):
    ''' Write the trip entry into the history file '''
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{time.ctime()} | Parado: {stopped_time:.1f}s | "
                f"Moviendo: {moving_time:.1f}s | Total: €{total_fare:.2f}\n")

# SESSION STATE - MAIN SESSION
# Here we store data so it doesn't reset when buttons are pressed.

if 'trip_active' not in st.session_state:
    st.session_state.trip_active = False  #Is the taxi currently in a trip?
if 'state' not in st.session_state:
    st.session_state.state = "stopped"    #Stopped or moving?
if 'last_time' not in st.session_state:
    st.session_state.last_time = 0.0      #Last time we checked the clock
if 'total_stopped' not in st.session_state:
    st.session_state.total_stopped = 0.0  #Total accumulated stopped time
if 'total_moving' not in st.session_state:
    st.session_state.total_moving = 0.0   #Total accumulated moving time
if 'rates' not in st.session_state:
    st.session_state.rates = load_rates() #Load rates into the session

# GRAPHICAL INTERFACE (What you see on screen)

st.title("🚖 Taxímetro Digital Interactivo")

# SIDEBAR (Settings)
st.sidebar.header("⚙️ Configuración")
st.sidebar.write("Ajusta los precios por segundo:")

# Use number_input to easily modify prices
new_stopped_rate = st.sidebar.number_input("Precio Parado (€/s)", value=st.session_state.rates["stopped"], format="%.3f")
new_moving_rate = st.sidebar.number_input("Precio Moviendo (€/s)", value=st.session_state.rates["moving"], format="%.3f")

# If values change, update the main session and the file
if new_stopped_rate != st.session_state.rates["stopped"] or new_moving_rate != st.session_state.rates["moving"]:
    st.session_state.rates["stopped"] = new_stopped_rate
    st.session_state.rates["moving"] = new_moving_rate
    save_rates(st.session_state.rates)
    st.sidebar.success("¡Tarifas actualizadas!")

# MAIN AREA
col1, col2 = st.columns(2)

#Time Logic: Calculate how much time passed since the last click
if st.session_state.trip_active:
    current_time = time.time()
    delta = current_time - st.session_state.last_time
    
    #Add elapsed time to the correct accumulator
    if st.session_state.state == "stopped":
        st.session_state.total_stopped += delta
    else:
        st.session_state.total_moving += delta
    
    #"Reset" the clock for the next segment
    st.session_state.last_time = current_time

# Calculate current fare
current_fare = (st.session_state.total_stopped * st.session_state.rates["stopped"] + 
                st.session_state.total_moving * st.session_state.rates["moving"])

# DISPLAY DATA ON SCREEN
with col1:
    st.metric(label="💶 Precio Actual", value=f"€{current_fare:.2f}")
    st.metric(label="🚦 Estado", value="🟢 Moviendo" if st.session_state.state == "moving" else "🛑 Parado")

with col2:
    st.write(f"⏱️ **Tiempo Parado:** {st.session_state.total_stopped:.1f} s")
    st.write(f"⏱️ **Tiempo Moviendo:** {st.session_state.total_moving:.1f} s")

st.divider()

# CONTROL BUTTONS
if not st.session_state.trip_active:
    #Big green button to start the trip
    if st.button("🏁 EMPEZAR CARRERA", type="primary", use_container_width=True):
        st.session_state.trip_active = True
        st.session_state.state = "stopped"
        st.session_state.last_time = time.time()
        st.session_state.total_stopped = 0.0
        st.session_state.total_moving = 0.0
        st.rerun() #Reload page to reflect changes
else:
    # Controls when the trip is active
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("Actualizar / Ver Costo 👁️"):
            # When clicked, Streamlit reruns the code above and updates the time
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
            time.sleep(7) # Small delay so the user can read the message
            st.rerun()

# SHOW TRIP HISTORY
st.divider()
if st.checkbox("📜 Ver Historial de Viajes"):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            st.text(f.read())
    else:
        st.info("Aún no hay viajes en el historial.")