from abc import ABC, abstractmethod


class Shape(ABC):  # Абстрактный класс Shape
    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...


class Circle(Shape):  # Конкретный класс Circle
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Square(Shape):  # Конкретный класс Square
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side ** 2

    def perimeter(self) -> float:
        return 4 * self.side


def print_shape_info(shape: Shape) -> None:  # Аннотация типа
    print(f"Area: {shape.area()}")
    print(f"Perimeter: {shape.perimeter()}")


# Использование
circle = Circle(5)
square = Square(3)

print_shape_info(circle)  # Работает, так как Circle — подкласс Shape
print_shape_info(square)  # Работает, так как Square — подкласс Shape
