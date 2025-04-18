import tuilib
import requests

def main(stdscr):
    # Initialize login status
    logged_in = False
    username = ""
    
    while not logged_in:
        options = ["signup", "login", "exit"]
        chosen = tuilib.tui.list_selector(stdscr, options)

        if chosen == "signup":
            username = tuilib.tui.real_time_input(stdscr, "Enter a username: ")
            password = tuilib.tui.real_time_input(stdscr, "Enter your password: ")
            response = requests.post("https://python-app-backend-qezf.onrender.com/signup", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                stdscr.addstr("Signup successful!\n")
                stdscr.refresh()
                tuilib.tui.real_time_input(stdscr, "Press Enter to continue...")
                logged_in = True
            else:
                stdscr.addstr("Error: Username already taken.\n")
                stdscr.refresh()
                tuilib.tui.real_time_input(stdscr, "Press Enter to try again...")

        elif chosen == "login":
            username = tuilib.tui.real_time_input(stdscr, "Enter your username: ")
            password = tuilib.tui.real_time_input(stdscr, "Enter your password: ")
            response = requests.post("https://python-app-backend-qezf.onrender.com/login", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                stdscr.addstr("Login successful!\n")
                stdscr.refresh()
                tuilib.tui.real_time_input(stdscr, "Press Enter to continue...")
                logged_in = True
            else:
                stdscr.addstr("Error: Invalid credentials.\n")
                stdscr.refresh()
                tuilib.tui.real_time_input(stdscr, "Press Enter to try again...")

        elif chosen == "exit":
            return

    # After login, show further options
    while logged_in:
        choices = ["send original message", "send copied message", "buy", "view messages", "exit"]
        choice = tuilib.tui.list_selector(stdscr, choices)

        if choice == "send original message":
            message = tuilib.tui.real_time_input(stdscr, "Enter your original message: ")
            response = requests.post("https://python-app-backend-qezf.onrender.com/send/original", json={
                "username": username,
                "message": message
            })
            if response.status_code == 200:
                stdscr.addstr("Message sent!\n")
            else:
                stdscr.addstr(f"Error: {response.json().get('error', 'Unknown error')}\n")
            stdscr.refresh()
            tuilib.tui.real_time_input(stdscr, "Press Enter to continue...")

        elif choice == "send copied message":
            message = tuilib.tui.real_time_input(stdscr, "Enter the copied message: ")
            response = requests.post("https://python-app-backend-qezf.onrender.com/send/copy", json={
                "username": username,
                "message": message
            })
            if response.status_code == 200:
                stdscr.addstr("Message copied and points awarded!\n")
            else:
                stdscr.addstr(f"Error: {response.json().get('error', 'Unknown error')}\n")
            stdscr.refresh()
            tuilib.tui.real_time_input(stdscr, "Press Enter to continue...")

        elif choice == "buy":
            response = requests.post("https://python-app-backend-qezf.onrender.com/buy", json={
                "username": username
            })
            if response.status_code == 200:
                stdscr.addstr("Message slot purchased!\n")
            else:
                stdscr.addstr(f"Error: {response.json().get('message', 'Unknown error')}\n")
            stdscr.refresh()
            tuilib.tui.real_time_input(stdscr, "Press Enter to continue...")

        elif choice == "view messages":
            response = requests.get("https://python-app-backend-qezf.onrender.com/messages")
            if response.status_code == 200:
                messages = response.json()
                stdscr.clear()
                for idx, message in enumerate(messages):
                    stdscr.addstr(idx, 0, str(message))
                stdscr.refresh()
                tuilib.tui.real_time_input(stdscr, "Press Enter to continue...")
            else:
                stdscr.addstr("Error fetching messages.\n")
                stdscr.refresh()
                tuilib.tui.real_time_input(stdscr, "Press Enter to continue...")

        elif choice == "exit":
            return

# Run the main function
tuilib.tui.main(main)
