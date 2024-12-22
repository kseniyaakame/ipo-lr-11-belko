
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json

class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление клиентами и транспортом")
        self.clients = []
        self.vehicles = []
        self.vehicle_id_counter = 1  

        self.create_menu()
        self.create_main_window()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Экспорт результата", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        menubar.add_command(label="О программе", command=self.show_about)
        self.root.config(menu=menubar)

    def create_main_window(self):
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Button layout
        button_texts = ["Добавить клиента", "Добавить транспорт", "Удалить клиента", "Удалить транспорт", "Распределить грузы"]
        button_commands = [self.add_client, self.add_vehicle, self.delete_client, self.delete_vehicle, self.distribute_loads]

        for text, command in zip(button_texts, button_commands):
            tk.Button(control_frame, text=text, command=command, width=20).pack(side=tk.LEFT, padx=5)

        table_frame = tk.Frame(self.root, padx=10, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Client table
        self.client_table = ttk.Treeview(table_frame, columns=("Имя", "Вес", "VIP"), show="headings")
        self.client_table.heading("Имя", text="Имя клиента")
        self.client_table.heading("Вес", text="Вес груза")
        self.client_table.heading("VIP", text="VIP статус")
        self.client_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vehicle table
        self.vehicle_table = ttk.Treeview(table_frame, columns=("ID", "Тип", "Грузоподъемность"), show="headings")
        self.vehicle_table.heading("ID", text="ID")
        self.vehicle_table.heading("Тип", text="Тип транспорта")
        self.vehicle_table.heading("Грузоподъемность", text="Грузоподъемность")
        self.vehicle_table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.client_table.bind("<Double-1>", self.on_double_click_client) 
        self.vehicle_table.bind("<Double-1>", self.on_double_click_vehicle)

        # Status label
        self.status_label = tk.Label(self.root, text="Готово", bd=1, relief=tk.SUNKEN, anchor="w", bg="lightgrey")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def add_client(self):
        def save_client():
            name = name_entry.get()
            weight = weight_entry.get()
            vip = vip_var.get()

            if not name.isalpha() or len(name) < 2:
                messagebox.showerror("Ошибка ввода", "Имя клиента должно содержать только буквы и минимум 2 символа.")
                return

            try:
                weight = int(weight)
                if weight <= 0 or weight > 10000:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка ввода", "Вес груза должен быть положительным числом до 10000.")
                return

            self.clients.append({"Имя": name, "Вес": weight, "VIP": "Да" if vip else "Нет"})
            self.client_table.insert("", "end", values=(name, weight, "Да" if vip else "Нет"))
            self.status_label.config(text="Клиент добавлен")
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить клиента")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Имя клиента:").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Вес груза:").pack(pady=5)
        weight_entry = tk.Entry(add_window)
        weight_entry.pack(pady=5)

        vip_var = tk.BooleanVar()
        tk.Checkbutton(add_window, text="VIP статус", variable=vip_var).pack(pady=5)

        tk.Button(add_window, text="Сохранить", command=save_client).pack(pady=5)
        tk.Button(add_window, text="Отмена", command=add_window.destroy).pack(pady=5)

    def add_vehicle(self):
        def save_vehicle():
            vehicle_type = type_var.get()
            capacity = capacity_entry.get()

            try:
                capacity = int(capacity)
                if capacity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка ввода", "Грузоподъемность должна быть положительным числом.")
                return

            vehicle_id = self.vehicle_id_counter
            self.vehicle_id_counter += 1  

            self.vehicles.append({"ID": vehicle_id, "Тип": vehicle_type, "Грузоподъемность": capacity})
            self.vehicle_table.insert("", "end", values=(vehicle_id, vehicle_type, capacity))
            self.status_label.config(text="Транспорт добавлен")
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить транспорт")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Тип транспорта:").pack(pady=5)
        type_var = tk.StringVar(value="Самолет")
        type_menu = ttk.Combobox(add_window, textvariable=type_var, values=["Самолет", "Поезд"])
        type_menu.pack(pady=5)

        tk.Label(add_window, text="Грузоподъемность (кг):").pack(pady=5)
        capacity_entry = tk.Entry(add_window)
        capacity_entry.pack(pady=5)

        tk.Button(add_window, text="Сохранить", command=save_vehicle).pack(pady=5)
        tk.Button(add_window, text="Отмена", command=add_window.destroy).pack(pady=5)

    def edit_client(self, item, values): 
        def save_edited_client(): 
            name = name_entry.get() 
            weight = weight_entry.get() 
            vip = vip_var.get() 
            
            if not name.isalpha() or len(name) < 2: 
                messagebox.showerror("Ошибка ввода", "Имя клиента должно содержать только буквы и минимум 2 символа.") 
                return 
            try: 
                weight = int(weight) 
                if weight <= 0 or weight > 10000: 
                    raise ValueError 
            except ValueError: 
                messagebox.showerror("Ошибка ввода", "Вес груза должен быть положительным числом до 10000.") 
                return 
            
            index = self.client_table.index(item) 
            self.clients[index] = {"Имя": name, "Вес": weight, "VIP": "Да" if vip else "Нет"} 
            self.client_table.item(item, values=(name, weight, "Да" if vip else "Нет")) 
            self.status_label.config(text="Клиент отредактирован") 
            edit_window.destroy() 

        edit_window = tk.Toplevel(self.root) 
        edit_window.title("Редактировать клиента") 
        edit_window.geometry("300x200") 

        tk.Label(edit_window, text="Имя клиента:").pack(pady=5) 
        name_entry = tk.Entry(edit_window) 
        name_entry.insert(0, values[0]) 
        name_entry.pack(pady=5) 

        tk.Label(edit_window, text="Вес груза (кг):").pack(pady=5) 
        weight_entry = tk.Entry(edit_window) 
        weight_entry.insert(0, values[1]) 
        weight_entry.pack(pady=5) 

        vip_var = tk.BooleanVar(value=True if values[2] == "Да" else False) 
        tk.Checkbutton(edit_window, text="VIP статус", variable=vip_var).pack(pady=5) 

        tk.Button(edit_window, text="Сохранить", command=save_edited_client).pack(pady=5) 
        tk.Button(edit_window, text="Отмена", command=edit_window.destroy).pack(pady=5)

    def edit_vehicle(self, item, values): 
        def save_edited_vehicle(): 
            vehicle_id = id_label["text"] 
            vehicle_type = type_var.get() 
            capacity = capacity_entry.get() 
            try: 
                capacity = int(capacity) 
                if capacity <= 0: 
                    raise ValueError("Грузоподъемность должна быть положительным числом.") 
            except ValueError: 
                messagebox.showerror("Ошибка ввода", "Грузоподъемность должна быть положительным числом.") 
                return 
            index = self.vehicle_table.index(item) 
            self.vehicles[index] = {"ID": vehicle_id, "Тип": vehicle_type, "Грузоподъемность": capacity} 
            self.vehicle_table.item(item, values=(vehicle_id, vehicle_type, capacity)) 
            self.status_label.config(text="Транспорт отредактирован") 
            edit_window.destroy() 

        edit_window = tk.Toplevel(self.root) 
        edit_window.title("Редактировать транспорт") 
        edit_window.geometry("300x200") 
        
        tk.Label(edit_window, text="ID транспорта:").pack(pady=5) 
        id_label = tk.Label(edit_window, text=values[0]) 
        id_label.pack(pady=5) 
        
        tk.Label(edit_window, text="Тип транспорта:").pack(pady=5) 
        type_var = tk.StringVar(value=values[1]) 
        type_menu = ttk.Combobox(edit_window, textvariable=type_var, values=["Самолет", "Поезд"]) 
        type_menu.pack(pady=5) 
        
        tk.Label(edit_window, text="Грузоподъемность (кг):").pack(pady=5)
        capacity_entry = tk.Entry(edit_window) 
        capacity_entry.insert(0, values[2]) 
        capacity_entry.pack(pady=5) 
        
        tk.Button(edit_window, text="Сохранить", command=save_edited_vehicle).pack(pady=5) 
        tk.Button(edit_window, text="Отмена", command=edit_window.destroy).pack(pady=5)

    def delete_client(self):
        selected_item = self.client_table.selection()
        if selected_item:
            index = self.client_table.index(selected_item)
            self.client_table.delete(selected_item)
            del self.clients[index]
            self.status_label.config(text="Клиент удален")
        else:
            messagebox.showwarning("Удаление клиента", "Пожалуйста, выберите клиента для удаления.")

    def delete_vehicle(self):
        selected_item = self.vehicle_table.selection()
        if selected_item:
            index = self.vehicle_table.index(selected_item)
            self.vehicle_table.delete(selected_item)
            del self.vehicles[index]
            self.status_label.config(text="Транспорт удален")
        else:
            messagebox.showwarning("Удаление транспорта", "Пожалуйста, выберите транспорт для удаления.")

    def on_double_click_client(self, event):
        selected_item = self.client_table.selection()
        if selected_item:
            item_values = self.client_table.item(selected_item[0], "values")
            self.edit_client(selected_item[0], item_values)

    def on_double_click_vehicle(self, event):
        selected_item = self.vehicle_table.selection()
        if selected_item:
            item_values = self.vehicle_table.item(selected_item[0], "values")
            self.edit_vehicle(selected_item[0], item_values)

    def distribute_loads(self):
        self.status_label.config(text="Начинаем распределение грузов...")

        for vehicle in self.vehicles:
            vehicle["Текущая загрузка"] = 0
            vehicle["Клиенты"] = []

        sorted_clients = sorted(self.clients, key=lambda x: (x["VIP"] == "Нет", -x["Вес"]))

        for client in sorted_clients:
            for vehicle in self.vehicles:
                if vehicle["Грузоподъемность"] >= vehicle["Текущая загрузка"] + client["Вес"]:
                    vehicle["Клиенты"].append(client["Имя"])
                    vehicle["Текущая загрузка"] += client["Вес"]
                    break

        result_window = tk.Toplevel(self.root)
        result_window.title("Результаты распределения грузов")
        result_window.geometry("400x300")

        result_table = ttk.Treeview(result_window, columns=("ID", "Тип", "Грузоподъемность", "Текущая загрузка", "Клиенты"), show="headings")
        result_table.heading("ID", text="ID")
        result_table.heading("Тип", text="Тип транспорта")
        result_table.heading("Грузоподъемность", text="Грузоподъемность (кг)")
        result_table.heading("Текущая загрузка", text="Текущая загрузка (кг)")
        result_table.heading("Клиенты", text=" Клиенты")
        result_table.pack(fill=tk.BOTH, expand=True)

        for vehicle in self.vehicles:
            clients = ", ".join(vehicle["Клиенты"])
            result_table.insert("", "end", values=(vehicle["ID"], vehicle["Тип"], vehicle["Грузоподъемность"], vehicle["Текущая загрузка"], clients))

        self.status_label.config(text="Распределение грузов выполнено")
        messagebox.showinfo("Распределение", "Распределение грузов выполнено")

    def export_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON файлы", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                data = {"Клиенты": self.clients, "Транспорт": self.vehicles}
                json.dump(data, file, ensure_ascii=False, indent=4)
            self.status_label.config(text="Результаты экспортированы")

    def show_about(self):
        messagebox.showinfo("О программе", "Лабораторная работа №12\nВариант: 5\nРазработчик: Белько К.М.")

root = tk.Tk()
app = TransportApp(root)
root.mainloop()