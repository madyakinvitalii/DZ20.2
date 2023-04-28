from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self, capacity):
        self.items = {}
        self.capacity = capacity

    @abstractmethod
    def add(self, name, quantity):
        pass

    @abstractmethod
    def remove(self, name, quantity):
        pass

    def get_free_space(self):
        return self.capacity - sum(self.items.values())

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items)


class Store(Storage):
    def __init__(self, capacity=100):
        super().__init__(capacity)

    def add(self, name, quantity):
        free_space = self.get_free_space()
        if free_space >= quantity:
            self.items[name] = self.items.get(name, 0) + quantity
        else:
            self.items[name] = self.items.get(name, 0) + free_space

    def remove(self, name, quantity):
        if name in self.items:
            self.items[name] = max(0, self.items[name] - quantity)


class Shop(Storage):
    def __init__(self, capacity=20):
        super().__init__(capacity)

    def add(self, name, quantity):
        if len(self.items) >= 5 or self.get_free_space() < quantity:
            return
        self.items[name] = self.items.get(name, 0) + quantity

    def remove(self, name, quantity):
        if name in self.items:
            self.items[name] = max(0, self.items[name] - quantity)
            if self.items[name] == 0:
                del self.items[name]


class Request:
    def __init__(self, request_str, storage_list):
        self.request_str = request_str
        self.storage_list = storage_list
        self.amount = None
        self.product = None
        self.from_storage = None
        self.to_storage = None
        self.parse_request_str()

    def parse_request_str(self):
        words = self.request_str.split()
        if len(words) != 8 or words[4] != "из":
            print("Неправильный запрос")
            return
        if not words[2].isdigit():
            print("Неправильное количество")
            return
        self.amount = int(words[2])
        self.product = words[3]
        self.from_storage = self.get_storage_by_name(words[5])
        self.to_storage = self.get_storage_by_name(words[7])

        if not self.from_storage:
            print(f"Хранилище '{words[5]}' не найдено1")
            return
        if not self.to_storage:
            print(f"Хранилище '{words[7]}' не найдено2")
            return

    def get_storage_by_name(self, name):
        for storage in self.storage_list:
            if storage.name.lower() == name.lower():
                return storage
        return None


def main():
    store1 = Store(100)
    store1.name = "склад"
    store1.add('печеньки', 10)
    shop1 = Shop(20)
    shop1.name = "магазин"
    storage_list = [store1, shop1]
    while True:
        try:
            user_input = input("Введите запрос (например, 'Курьер забирает 3 печеньки из склад в магазин'): ")
            request = Request(user_input, storage_list)

            if request.from_storage is None:
                print(f"Хранилище '{request.from_storage}' не найдено3")
                continue
            if request.to_storage is None:
                print(f"Хранилище '{request.to_storage}' не найдено4")
                continue

            if request.from_storage.get_items().get(request.product, 0) >= request.amount:
                request.from_storage.remove(request.product, request.amount)
                request.to_storage.add(request.product, request.amount)
                print(
                    f"Курьер забрал {request.amount} {request.product} со склада и доставил их в {request.to_storage.name}")
            else:
                print("Не хватает на складе, попробуйте заказать меньше")

            print("В складе хранится:")
            for name, quantity in storage_list[0].get_items().items():
                print(f"{quantity} {name}")

            print("В магазине хранится:")
            for name, quantity in storage_list[1].get_items().items():
                print(f"{quantity} {name}")

        except KeyboardInterrupt:
            print("Выход из программы.")
            break


main()
