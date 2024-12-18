from .vehicle import Vehicle

class Airplane(Vehicle):
    def __init__(self, capacity, max_altitude):
        super().__init__(capacity)
        if not isinstance(max_altitude, (int, float)) or max_altitude <= 0:
            raise ValueError("Максимальная высота полета должна быть положительным числом.")

        self.max_altitude = max_altitude

    def __str__(self):
        return (f"ID самолета: {self.vehicle_id}, Грузоподъемность: {self.capacity}, "
                f"Максимальная высота полета: {self.max_altitude}, Текущая загрузка: {self.current_load}")