import time
import json
import os
import logging

# ------------------- LOGGING SETUP --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="taximeter.log",        # Save logs in this file
    filemode="a",
)

# Also print logs to console
#console = logging.StreamHandler()
#console.setLevel(logging.INFO)
#logging.getLogger().addHandler(console)
# ------------------------------------------------------


# --------------- DEFAULT CONFIGURATION ----------------
DEFAULT_RATES = {
    "stopped": 0.02,   # €0.02 per second when taxi is stopped
    "moving": 0.05     # €0.05 per second when taxi is moving
}

RATES_FILE = "rates.json"
HISTORY_FILE = "history.txt"
# ------------------------------------------------------

# ------------------ RATE MANAGEMENT -------------------
def load_rates():
    if os.path.exists(RATES_FILE):
        logging.info("Loading rates from rates.json")
        with open(RATES_FILE, "r") as f:
            return json.load(f)
    logging.warning("rates.json not found — using default rates")
    return DEFAULT_RATES.copy()


def save_rates(rates):
    logging.info(f"Saving updated rates into JSON file: {rates}")
    with open(RATES_FILE, "w") as f:
        json.dump(rates, f)
# -------------------------------------------------------

# -------- FARE CALCULATION AND HISTORY SAVING ----------
def calculate_fare(seconds_stopped, seconds_moving, rates):
    logging.debug(
        f"Calculating fare | stopped={seconds_stopped:.1f}s | "
        f"moving={seconds_moving:.1f}s | rates={rates}"
    )
    return (seconds_stopped * rates["stopped"] + seconds_moving * rates["moving"])


def save_trip_to_history(stopped_time, moving_time, total_fare):
    """
    Append a finished trip summary to the history file.
    """
    logging.info(
        f"Saving trip: stopped={stopped_time:.1f}s, "
        f"moving={moving_time:.1f}s, fare=€{total_fare:.2f}"
    )
    with open(HISTORY_FILE, "a") as f:
        f.write(
            f"{time.ctime()} | "
            f"Stopped: {stopped_time:.1f}s | "
            f"Moving: {moving_time:.1f}s | "
            f"Total: €{total_fare:.2f}\n"
        )
# ------------------------------------------------------

# --------- CORE PROGRAM (CLI TAXIMETER) ---------------
def taximeter():
    print("="*60)
    print("🚕 Welcome to the Interactive Digital Taximeter! 🚕")
    print("="*60)

    print("\nThis system simulates a digital taximeter based on travel time.")
    print("Use the commands below to manage the taxi trip.\n")

    print("### 🛠️  Available Commands and Their Functions ###")
    print("-" * 40)

    commands_description = [
        ("🏁 start", "Initiate a new trip. The taximeter starts in the 'stopped' state."),
        ("🟢 move", "Changes the taxi state to 'moving' (moving time starts counting)."),
        ("🛑 stop", "Changes the taxi state to 'stopped' (stopped time starts counting)."),
        ("👁️  show", "Displays the current partial fare without ending the trip."),
        ("💵 finish", "Calculates and displays the final fare, ends the trip, and saves history."),
        ("⚙️  rates", "Views or configures the calculation rates (stopped/moving)."),
        ("📜 history", "Displays the history of completed trips."),
        ("❌ exit", "Closes the taximeter program.")
    ]

    for command, description in commands_description:
        print(f" {command:<8}: {description}")

    print("-" * 40)
    print("\n**Please type a command to begin (E.g.: start):**\n")

    # Internal state variables
    trip_active = False
    stopped_time = 0
    moving_time = 0
    state = None           # Possible values: "stopped", "moving"
    state_start_time = 0   # Timestamp for current state
    rates = load_rates()   # Load user-configured or default rates

    while True:
        command = input("> ").strip().lower()
        logging.info(f"User entered command: {command}")

        # START TRIP
        if command == "start":
            if trip_active:
                print("🛣️  A trip is already in progress.")
                logging.warning("Attempted to start a trip while one is already active.")
                continue

            trip_active = True
            stopped_time = 0
            moving_time = 0
            state = "stopped"
            state_start_time = time.time()

            logging.info("Trip started.")
            print("🏁 Trip started. Current state: '🛑 stopped'.")


        # CHANGE STATE (stop/move)
        elif command in ("stop", "move"):
            if not trip_active:
                print("⚠️  No active trip. Start a trip first.")
                logging.warning("Attempted to change state without active trip.")
                continue

            duration = time.time() - state_start_time

            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration

            new_state = "stopped" if command == "stop" else "moving"
            logging.info(f"State changed from {state} to {new_state}")

            state = new_state
            state_start_time = time.time()

            emoji_state = "🛑 stopped" if state == "stopped" else "🟢 moving"
            print(f"State changed to '{emoji_state}'.")


        # SHOW PARTIAL FARE WITHOUT ENDING TRIP
        elif command == "show":
            if not trip_active:
                print("⚠️ No active trip.")
                logging.warning("Attempted to show fare without active trip.")
                continue

            current_duration = time.time() - state_start_time

            temp_stopped = stopped_time + (current_duration if state == "stopped" else 0)
            temp_moving = moving_time + (current_duration if state == "moving" else 0)

            partial_fare = calculate_fare(temp_stopped, temp_moving, rates)
            logging.info(f"Showing partial fare: €{partial_fare:.2f}")
            print(f"Current fare: €{partial_fare:.2f}")


        # FINISH TRIP
        elif command == "finish":
            if not trip_active:
                print("⚠️  No active trip to finish.")
                logging.warning(" Attempted to finish trip without active trip.")
                continue

            duration = time.time() - state_start_time
            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration

            total_fare = calculate_fare(stopped_time, moving_time, rates)

            logging.info(
                f"Trip finished | stopped={stopped_time:.1f}s | "
                f"moving={moving_time:.1f}s | fare=€{total_fare:.2f}"
            )

            print("\n--- Trip Summary ---")
            print(f"Stopped time : {stopped_time:.1f} seconds")
            print(f"Moving time  : {moving_time:.1f} seconds")
            print(f"Total fare   : €{total_fare:.2f}")
            print("--------------------\n")

            save_trip_to_history(stopped_time, moving_time, total_fare)

            trip_active = False
            state = None


        # MODIFY RATES
        elif command == "rates":
            logging.info("Viewing or updating rates")

            print(f"Current rates:")
            print(f"   Stopped: €{rates['stopped']} per second")
            print(f"   Moving : €{rates['moving']} per second\n")

            try:
                new_stopped = input("New stopped rate (ENTER to keep): ")
                new_moving = input("New moving rate (ENTER to keep): ")

                if new_stopped:
                    rates["stopped"] = float(new_stopped)
                if new_moving:
                    rates["moving"] = float(new_moving)

                save_rates(rates)
                print("Rates updated successfully!")

            except ValueError:
                logging.error("Invalid rate input")
                print("Invalid input. Rates not updated.")


        # SHOW HISTORY
        elif command == "history":
            logging.info("Displaying trip history")

            if not os.path.exists(HISTORY_FILE):
                print("No trip history yet.")
            else:
                with open(HISTORY_FILE, "r") as f:
                    print("\n--- Trip History ---")
                    print(f.read())
                    print("---------------------\n")


        # EXIT PROGRAM
        elif command == "exit":
            logging.info("Program exited by user")
            print("👋 Exiting the Interactive Digital Taximeter. Goodbye! 🚪")
            break


        # UNKNOWN COMMAND
        else:
            logging.warning(f"Unknown command: {command}")
            print("❗ Unknown command. Use: start, stop, move, finish, show, rates, history, exit")


# MAIN ENTRY POINT
if __name__ == "__main__":
    taximeter()
