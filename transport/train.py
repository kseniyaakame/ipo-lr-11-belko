from .vehicle import Vehicle

class Train(Vehicle):
    def __init__(self, number_of_cars, capacity):
        super().__init__(capacity)
        if not isinstance(number_of_cars, int) or number_of_cars <= 0:
            raise ValueError("Количество вагонов должно быть положительным целым числом.")
        
        self.number_of_cars = number_of_cars

    def __str__(self):
        return (f"ID поезда: {self.vehicle_id}, Грузоподъемность: {self.capacity}, "
                f"Количество вагонов: {self.number_of_cars}, Текущая загрузка: {self.current_load} ")