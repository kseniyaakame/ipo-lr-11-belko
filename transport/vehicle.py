from transport.client import Client

class Vehicle:
    vehicle_counter = 1

    def __init__(self, capacity):
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом.")
        
        self.vehicle_id = Vehicle.vehicle_counter
        Vehicle.vehicle_counter += 1
        self.capacity = capacity 
        self.current_load = 0
        self.clients_list = []

    def load_cargo(self, client):
        if not isinstance(client, Client):
            raise TypeError("Объект должен быть экземпляром класса Client.")
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Невозможно загрузить груз: превышение грузоподъемности.")

        self.clients_list.append(client)
        self.current_load += client.cargo_weight

    def __str__(self):
        return (f"ID транспорта: {self.vehicle_id}, Грузоподъемность: {self.capacity}, "
                f"Текущая загрузка: {self.current_load}")