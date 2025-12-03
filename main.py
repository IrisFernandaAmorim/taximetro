import time
import json
import os

# --------------------------------------------------------------------
# DEFAULT CONFIGURATION
# --------------------------------------------------------------------

# Default rates (cost per second)
DEFAULT_RATES = {
    "stopped": 0.02,   # €0.02 per second when taxi is not moving
    "moving": 0.05     # €0.05 per second when taxi is moving
}

RATES_FILE = "rates.json"
HISTORY_FILE = "history.txt"


# --------------------------------------------------------------------
# RATE MANAGEMENT
# --------------------------------------------------------------------

def load_rates():
    """
    Load pricing rates from a JSON file.
    If the file does not exist, return the default rates.
    """
    if os.path.exists(RATES_FILE):
        with open(RATES_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_RATES.copy()


def save_rates(rates):
    """
    Save updated rates into the JSON file.
    """
    with open(RATES_FILE, "w") as f:
        json.dump(rates, f)


# --------------------------------------------------------------------
# FARE CALCULATION & HISTORY SAVING
# --------------------------------------------------------------------

def calculate_fare(seconds_stopped, seconds_moving, rates):
    """
    Calculate the total fare in euros based on:
    - stopped time  * stopped rate
    - moving time   * moving rate
    """
    return (seconds_stopped * rates["stopped"]
            + seconds_moving * rates["moving"])


def save_trip_to_history(stopped_time, moving_time, total_fare):
    """
    Append a finished trip summary to the history file.
    """
    with open(HISTORY_FILE, "a") as f:
        f.write(
            f"{time.ctime()} | "
            f"Stopped: {stopped_time:.1f}s | "
            f"Moving: {moving_time:.1f}s | "
            f"Total: €{total_fare:.2f}\n"
        )


# --------------------------------------------------------------------
# CORE PROGRAM (CLI TAXIMETER)
# --------------------------------------------------------------------

def taximeter():
    print("Welcome to the F5 Digital Taximeter!")
    print("Commands: start, stop, move, finish, show, rates, history, exit\n")

    # Internal state variables
    trip_active = False
    stopped_time = 0
    moving_time = 0
    state = None           # Possible values: "stopped", "moving"
    state_start_time = 0   # Timestamp for current state
    rates = load_rates()   # Load user-configured or default rates

    while True:
        command = input("> ").strip().lower()

        # --------------------------------------------------------
        # START TRIP
        # --------------------------------------------------------
        if command == "start":
            if trip_active:
                print("A trip is already in progress.")
                continue

            trip_active = True
            stopped_time = 0
            moving_time = 0
            state = "stopped"               # taxi always starts stopped
            state_start_time = time.time()  # start counting time

            print("Trip started. Current state: 'stopped'.")

        # --------------------------------------------------------
        # CHANGE STATE (stop/move)
        # --------------------------------------------------------
        elif command in ("stop", "move"):
            if not trip_active:
                print("No active trip. Start a trip first.")
                continue

            # How long we were in the previous state?
            duration = time.time() - state_start_time

            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration

            # Change the state now
            state = "stopped" if command == "stop" else "moving"
            state_start_time = time.time()

            print(f"State changed to '{state}'.")

        # --------------------------------------------------------
        # SHOW PARTIAL FARE WITHOUT ENDING TRIP
        # --------------------------------------------------------
        elif command == "show":
            if not trip_active:
                print("No active trip.")
                continue

            # Temporary calculation including the current running state
            current_duration = time.time() - state_start_time

            temp_stopped = stopped_time + (current_duration if state == "stopped" else 0)
            temp_moving = moving_time + (current_duration if state == "moving" else 0)

            partial_fare = calculate_fare(temp_stopped, temp_moving, rates)
            print(f"Current fare: €{partial_fare:.2f}")

        # --------------------------------------------------------
        # FINISH TRIP
        # --------------------------------------------------------
        elif command == "finish":
            if not trip_active:
                print("No active trip to finish.")
                continue

            # Add any remaining time in the last active state
            duration = time.time() - state_start_time
            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration

            # Calculate final fare
            total_fare = calculate_fare(stopped_time, moving_time, rates)

            print("\n--- Trip Summary ---")
            print(f"Stopped time : {stopped_time:.1f} seconds")
            print(f"Moving time  : {moving_time:.1f} seconds")
            print(f"Total fare   : €{total_fare:.2f}")
            print("--------------------\n")

            # Save the trip into history
            save_trip_to_history(stopped_time, moving_time, total_fare)

            # Reset for next trip
            trip_active = False
            state = None

        # --------------------------------------------------------
        # MODIFY RATES
        # --------------------------------------------------------
        elif command == "rates":
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
                print("Invalid input. Rates not updated.")

        # --------------------------------------------------------
        # SHOW HISTORY
        # --------------------------------------------------------
        elif command == "history":
            if not os.path.exists(HISTORY_FILE):
                print("No trip history yet.")
            else:
                with open(HISTORY_FILE, "r") as f:
                    print("\n--- Trip History ---")
                    print(f.read())
                    print("---------------------\n")

        # --------------------------------------------------------
        # EXIT PROGRAM
        # --------------------------------------------------------
        elif command == "exit":
            print("Exiting program. Goodbye!")
            break

        # --------------------------------------------------------
        # UNKNOWN COMMAND
        # --------------------------------------------------------
        else:
            print("Unknown command. Use: start, stop, move, finish, show, rates, history, exit")


# --------------------------------------------------------------------
# MAIN ENTRY POINT
# --------------------------------------------------------------------

if __name__ == "__main__":
    taximeter()
