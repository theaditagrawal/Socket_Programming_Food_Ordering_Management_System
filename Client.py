import socket
import json
import sys
import tkinter as tk
from tkinter import Label, Button, StringVar, Listbox

class OrderGUI:
    def _init_(self, master):
        self.master = master
        self.master.title("Order Menu")

        self.menu_items = ["Paneer 65", "Samosa", "Pizza", "Biryani", "Burger"]  # Add your real food items here
        self.order = {}

        self.label_item = Label(master, text="Choose Item:")
        self.label_item.grid(row=0, column=0, padx=5, pady=5)

        self.listbox_items = Listbox(master, selectmode=tk.MULTIPLE, exportselection=0)
        for item in self.menu_items:
            self.listbox_items.insert(tk.END, item)
        self.listbox_items.grid(row=0, column=1, padx=5, pady=5)

        self.label_quantity = Label(master, text="Quantity:")
        self.label_quantity.grid(row=1, column=0, padx=5, pady=5)

        self.quantity_var = StringVar()
        self.quantity_var.set("1")  # Initial quantity value
        self.label_quantity_value = Label(master, textvariable=self.quantity_var)
        self.label_quantity_value.grid(row=1, column=1, padx=5, pady=5)

        self.increase_button = Button(master, text="▲", command=self.increase_quantity)
        self.increase_button.grid(row=1, column=2, padx=5, pady=5)

        self.decrease_button = Button(master, text="▼", command=self.decrease_quantity)
        self.decrease_button.grid(row=1, column=3, padx=5, pady=5)

        self.add_button = Button(master, text="Add Item", command=self.add_item)
        self.add_button.grid(row=2, column=0, columnspan=4, pady=10)

        self.done_button = Button(master, text="Done", command=self.send_order)
        self.done_button.grid(row=3, column=0, columnspan=4, pady=10)

        self.result_var = StringVar()
        self.result_label = Label(master, textvariable=self.result_var)
        self.result_label.grid(row=4, column=0, columnspan=4, pady=10)

    def increase_quantity(self):
        current_quantity = int(self.quantity_var.get())
        self.quantity_var.set(str(current_quantity + 1))

    def decrease_quantity(self):
        current_quantity = int(self.quantity_var.get())
        if current_quantity > 1:
            self.quantity_var.set(str(current_quantity - 1))

    def add_item(self):
        selected_items = [self.listbox_items.get(idx) for idx in self.listbox_items.curselection()]
        quantity = int(self.quantity_var.get())

        if selected_items:
            for item in selected_items:
                self.order[item] = quantity
            self.result_var.set(f"Added: {', '.join(selected_items)} x{quantity}")
        else:
            self.result_var.set("Invalid input. Please select item(s).")

    def send_order(self):
        if self.order:
            # Encode the order as JSON
            order_json = json.dumps(self.order)

            # Connect to the server and send the order
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(order_json.encode())

                # Receive and display the total bill
                data = s.recv(1024).decode()
                self.result_var.set(data)
                self.order = {}  # Reset the order after sending
        else:
            self.result_var.set("No items selected. Please add items before clicking 'Done'.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <port>")
        sys.exit(1)

    global HOST, PORT
    HOST = input("Enter server IP address: ")
    PORT = int(sys.argv[1])

    root = tk.Tk()
    app = OrderGUI(root)
    root.mainloop()

if _name_ == "_main_":
    main()
