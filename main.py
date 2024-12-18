from transport.client import Client
from transport.airplaine import Airplane
from transport.train import Train
from transport.transport_company import TransportCompany

def main():
    company = TransportCompany("Компания")

    while True:
        print("\nМеню: \n1. Добавить клиента \n2. Добавить самолет \n3. Добавить поезд \n4. Распределить грузы \n5. Показать транспорт и загрузку \n6. Вывести всех клиентов \n7. Вывести весь транспорт \n8. Выйти")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            try:
                name = input("Введите имя клиента: ")
                weight = float(input("Введите вес груза (кг): "))
                is_vip_input = input("Клиент VIP? (да/нет): ").strip().lower()
                is_vip = is_vip_input == "да"

                client = Client(name, weight, is_vip)
                company.add_client(client)
                print("Клиент добавлен.")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            try:
                capacity = float(input("Введите грузоподъемность самолета (т): "))
                if capacity <= 0:
                    raise ValueError("Грузоподъемность должна быть положительной.")
                max_altitude = float(input("Введите максимальную высоту полета (м): "))
                vehicle = Airplane(max_altitude, capacity)
                company.add_vehicle(vehicle)
                print("Самолет добавлен.")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            try:
                capacity = float(input("Введите грузоподъемность поезда (т): "))
                if capacity <= 0:
                    raise ValueError("Грузоподъемность должна быть положительной.")
                number_of_cars = int(input("Введите количество вагонов: "))
                if number_of_cars <= 0:
                    raise ValueError("Количество вагонов должно быть положительным целым числом.")
                vehicle = Train(number_of_cars, capacity)
                company.add_vehicle(vehicle)
                print("Поезд добавлен.")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "4":
            company.optimize_cargo_distribution()
            print("Грузы распределены.")

        elif choice == "5":
            for vehicle in company.list_vehicles():
                print(vehicle)
                for client in vehicle.clients_list:
                    print(f"  - {client}")

        elif choice == "6":
            for client in company.list_clients():
                print(client)

        elif choice == "7":
            for vehicle in company.list_vehicles():
                print(vehicle)

        elif choice == "8":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод, попробуйте снова.")


main()