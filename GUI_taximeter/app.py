import streamlit as st
import time
import json
import os
import logging

# ------------------- LOGGING SETUP --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="taximeter_gui.log",
    filemode="a",
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)
# ------------------------------------------------------

# ----------------- SETTINGS FILES ---------------------
RATES_FILE = "rates.json"
HISTORY_FILE = "history.txt"
# ------------------------------------------------------

# --------- RATE MANAGEMENT AND HISTORY SAVING ---------
def load_rates():
    if os.path.exists(RATES_FILE):
        logging.info("Loading rates from rates.json (GUI)")
        with open(RATES_FILE, "r") as f:
            return json.load(f)
    logging.warning("rates.json not found — using default rates (GUI)")
    return {"stopped": 0.02, "moving": 0.05}


def save_rates(rates):
    logging.info(f"Saving updated rates in GUI: {rates}")
    with open(RATES_FILE, "w") as f:
        json.dump(rates, f)


def save_trip_to_history(stopped_time, moving_time, total_fare):
    logging.info(
        f"Saving GUI trip -> stopped={stopped_time:.1f}s, "
        f"moving={moving_time:.1f}s, fare=€{total_fare:.2f}"
    )

    with open(HISTORY_FILE, "a") as f:
        f.write(
            f"{time.ctime()} | Parado: {stopped_time:.1f}s | "
            f"Moviendo: {moving_time:.1f}s | Total: €{total_fare:.2f}\n"
        )
# ------------------------------------------------------

# ------------ SESSION STATE INITIALIZATION ------------
if 'trip_active' not in st.session_state:
    st.session_state.trip_active = False
if 'state' not in st.session_state:
    st.session_state.state = "stopped"
if 'last_time' not in st.session_state:
    st.session_state.last_time = 0.0
if 'total_stopped' not in st.session_state:
    st.session_state.total_stopped = 0.0
if 'total_moving' not in st.session_state:
    st.session_state.total_moving = 0.0
if 'rates' not in st.session_state:
    st.session_state.rates = load_rates()
# ------------------------------------------------------

# ---------------- USER INTERFACE ----------------------

st.title("🚖 Taxímetro Digital Interactivo")

## SIDEBAR ##
st.sidebar.header("⚙️ Configuración")
st.sidebar.write("Ajusta los precios por segundo:")

new_stopped_rate = st.sidebar.number_input(
    "Precio Parado (€/s)",
    value=st.session_state.rates["stopped"],
    format="%.3f"
)

new_moving_rate = st.sidebar.number_input(
    "Precio Moviendo (€/s)",
    value=st.session_state.rates["moving"],
    format="%.3f"
)

# If values change, update the main session and file
if new_stopped_rate != st.session_state.rates["stopped"] or new_moving_rate != st.session_state.rates["moving"]:
    logging.info(
        f"User updated GUI rates → stopped={new_stopped_rate}, moving={new_moving_rate}"
    )
    st.session_state.rates["stopped"] = new_stopped_rate
    st.session_state.rates["moving"] = new_moving_rate
    save_rates(st.session_state.rates)
    st.sidebar.success("¡Tarifas actualizadas!")
# ------------------------------------------------------

# ----------- TIME AND FARE CALCULATION ----------------

if st.session_state.trip_active:
    current_time = time.time()
    delta = current_time - st.session_state.last_time

    if st.session_state.state == "stopped":
        st.session_state.total_stopped += delta
    else:
        st.session_state.total_moving += delta

    st.session_state.last_time = current_time

current_fare = (
    st.session_state.total_stopped * st.session_state.rates["stopped"] +
    st.session_state.total_moving * st.session_state.rates["moving"]
)

# ------------------- DISPLAY INFORMATION --------------
col1, col2 = st.columns(2)

with col1:
    st.metric(label="💶 Precio Actual", value=f"€{current_fare:.2f}")
    st.metric(
        label="🚦 Estado",
        value="🟢 Moviendo" if st.session_state.state == "moving" else "🛑 Parado"
    )

with col2:
    st.write(f"⏱️ **Tiempo Parado:** {st.session_state.total_stopped:.1f} s")
    st.write(f"⏱️ **Tiempo Moviendo:** {st.session_state.total_moving:.1f} s")

st.divider()
# ------------------------------------------------------

# --------------- CONTROL BUTTONS ----------------------

if not st.session_state.trip_active:
    if st.button("🏁 EMPEZAR CARRERA", type="primary", use_container_width=True):
        logging.info("GUI trip started")
        st.session_state.trip_active = True
        st.session_state.state = "stopped"
        st.session_state.last_time = time.time()
        st.session_state.total_stopped = 0.0
        st.session_state.total_moving = 0.0
        st.rerun()

else:
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Actualizar / Ver Costo 👁️"):
            logging.info("User requested GUI fare refresh")
            pass

    with c2:
        if st.session_state.state == "stopped":
            if st.button("🟢 Acelerar (Mover)"):
                logging.info("GUI → state changed: stopped → moving")
                st.session_state.state = "moving"
                st.rerun()
        else:
            if st.button("🛑 Frenar (Parar)"):
                logging.info("GUI → state changed: moving → stopped")
                st.session_state.state = "stopped"
                st.rerun()

    with c3:
        if st.button("💵 COBRAR Y FINALIZAR", type="primary"):
            logging.info(
                f"GUI trip finishing → stopped={st.session_state.total_stopped:.1f}s, "
                f"moving={st.session_state.total_moving:.1f}s, fare=€{current_fare:.2f}"
            )

            save_trip_to_history(
                st.session_state.total_stopped,
                st.session_state.total_moving,
                current_fare
            )

            st.session_state.trip_active = False
            st.success(f"Viaje terminado. Total a cobrar: €{current_fare:.2f}")
            time.sleep(7)
            st.rerun()
# ------------------------------------------------------

# ----------------- HISTORY VIEW -----------------------

st.divider()
if st.checkbox("📜 Ver Historial de Viajes"):
    logging.info("User opened GUI trip history")
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            st.text(f.read())
    else:
        st.info("Aún no hay viajes en el historial.")
# ------------------------------------------------------