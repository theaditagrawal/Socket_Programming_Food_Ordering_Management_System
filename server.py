import socket
import json
import threading
import sys

if len(sys.argv) != 3:
    print("Usage: python server.py <ip_address> <port>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

menu = {
    "Paneer 65": 10.00,
    "Samosa": 5.00,
    "Pizza": 12.00,
    "Biryani": 15.00,
    "Burger": 8.00
}

def handle_client(conn, addr):
    print('Connected by', addr)
    while True:
        try:
            # Receive and decode the order
            data = conn.recv(1024).decode()
            if not data:
                break

            order = json.loads(data)

            # Calculate total bill
            total_bill = 0.0
            for item, quantity in order.items():
                if item not in menu:
                    conn.sendall(f"Item '{item}' not found in the menu\n".encode())
                    continue
                total_bill += menu[item] * quantity

            # Check if total bill crosses a certain threshold for cashback
            cashback_threshold = 50.0  
            cashback_message = ""

            if total_bill > cashback_threshold:
                cashback = 20.0
                total_bill -= cashback
                cashback_message = f"\nCongratulations! You earned a ₹20 cashback."

            # Send total bill
            bill_message = f"Total bill: ₹{total_bill:.2f}{cashback_message}\n"
            print(" ", bill_message)
            conn.sendall(bill_message.encode())

        except json.JSONDecodeError:
            conn.sendall(f"Invalid order format\n".encode())

    conn.close()  # Close the connection after the entire communication

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print('Server listening on', (HOST, PORT))

    while True:
        # Accept new connections in a separate thread
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

print('Closing socket')
