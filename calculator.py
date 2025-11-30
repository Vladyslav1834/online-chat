import pygame
import sys

# Ініціалізація pygame - обов'язково викликати перед використанням
pygame.init()

# Константи для кольорів (RGB формат: червоний, зелений, синій)
WHITE = (255, 255, 255)  # Білий колір для фону
BLACK = (0, 0, 0)  # Чорний колір для тексту
GRAY = (128, 128, 128)  # Сірий колір для кнопок
LIGHT_GRAY = (200, 200, 200)  # Світло-сірий для підсвічування
BLUE = (70, 130, 180)  # Синій колір для операцій
DARK_BLUE = (50, 100, 150)  # Темно-синій для натиснутих кнопок операцій
RED = (220, 20, 60)  # Червоний колір для кнопки очищення

# Константи розмірів вікна та елементів
WINDOW_WIDTH = 300  # Ширина вікна калькулятора
WINDOW_HEIGHT = 400  # Висота вікна калькулятора
BUTTON_WIDTH = 70  # Ширина кожної кнопки
BUTTON_HEIGHT = 50  # Висота кожної кнопки
DISPLAY_HEIGHT = 60  # Висота дисплея для відображення чисел

# Створення вікна з заданими розмірами
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Калькулятор")  # Заголовок вікна

# Створення шрифтів для різних елементів
font_large = pygame.font.Font(None, 36)  # Великий шрифт для дисплея
font_medium = pygame.font.Font(None, 24)  # Середній шрифт для кнопок


class Calculator:
    def __init__(self):
        """Ініціалізація калькулятора з початковими значеннями"""
        self.display_text = "0"  # Текст що відображається на дисплеї
        self.first_number = 0  # Перше число для операції
        self.operation = None  # Поточна операція (+, -, *, /)
        self.waiting_for_number = False  # Чи чекаємо введення нового числа

    def add_digit(self, digit):
        """Додавання цифри до дисплея"""
        if self.waiting_for_number:
            # Якщо чекаємо нове число, замінюємо дисплей
            self.display_text = str(digit)
            self.waiting_for_number = False
        else:
            # Інакше додаємо цифру до існуючого числа
            if self.display_text == "0":
                self.display_text = str(digit)
            else:
                self.display_text += str(digit)

    def set_operation(self, op):
        """Встановлення операції (+, -, *, /)"""
        if self.operation and not self.waiting_for_number:
            # Якщо вже є операція і число введено, виконуємо попередню операцію
            self.calculate()

        self.first_number = float(self.display_text)
        self.operation = op
        self.waiting_for_number = True

    def calculate(self):
        """Виконання математичної операції"""
        if self.operation is None:
            return

        try:
            second_number = float(self.display_text)

            # Виконання операції залежно від вибраного символу
            if self.operation == "+":
                result = self.first_number + second_number
            elif self.operation == "-":
                result = self.first_number - second_number
            elif self.operation == "*":
                result = self.first_number * second_number
            elif self.operation == "/":
                if second_number == 0:
                    # Обробка ділення на нуль
                    self.display_text = "Помилка: ділення на 0"
                    self.operation = None
                    return
                result = self.first_number / second_number

            # Форматування результату (прибираємо зайві нулі після коми)
            if result.is_integer():
                self.display_text = str(int(result))
            else:
                self.display_text = str(round(result, 8))

        except ValueError:
            # Обробка помилок введення
            self.display_text = "Помилка"

        self.operation = None
        self.waiting_for_number = True

    def clear(self):
        """Очищення калькулятора до початкового стану"""
        self.display_text = "0"
        self.first_number = 0
        self.operation = None
        self.waiting_for_number = False


class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, text_color=BLACK):
        """Створення кнопки з заданими параметрами"""
        self.rect = pygame.Rect(x, y, width, height)  # Прямокутник кнопки
        self.text = text  # Текст на кнопці
        self.color = color  # Колір кнопки
        self.text_color = text_color  # Колір тексту
        self.is_pressed = False  # Чи натиснута кнопка

    def draw(self, screen):
        """Малювання кнопки на екрані"""
        # Вибір кольору залежно від стану кнопки
        current_color = LIGHT_GRAY if self.is_pressed else self.color

        # Малювання прямокутника кнопки
        pygame.draw.rect(screen, current_color, self.rect)
        # Малювання рамки навколо кнопки
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Створення тексту та його розміщення по центру кнопки
        text_surface = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """Перевірка чи клікнули по кнопці"""
        return self.rect.collidepoint(pos)


def create_buttons():
    """Створення всіх кнопок калькулятора"""
    buttons = []

    # Створення кнопок цифр (0-9)
    # Розміщення цифр у стандартному порядку калькулятора
    digit_positions = [
        (10, 310),  # 0
        (10, 260),  # 1
        (90, 260),  # 2
        (170, 260),  # 3
        (10, 210),  # 4
        (90, 210),  # 5
        (170, 210),  # 6
        (10, 160),  # 7
        (90, 160),  # 8
        (170, 160),  # 9
    ]

    for i in range(10):
        x, y = digit_positions[i]
        buttons.append(Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, str(i)))

    # Створення кнопок операцій
    # Розміщення операцій справа від цифр
    operations = [
        (250, 160, "+", BLUE),  # Додавання
        (250, 210, "-", BLUE),  # Віднімання
        (250, 260, "*", BLUE),  # Множення
        (250, 310, "/", BLUE),  # Ділення
    ]

    for x, y, op, color in operations:
        buttons.append(Button(x, y, BUTTON_WIDTH - 20, BUTTON_HEIGHT, op, color, WHITE))

    # Кнопка дорівнює
    buttons.append(Button(90, 310, BUTTON_WIDTH, BUTTON_HEIGHT, "=", BLUE, WHITE))

    # Кнопка очищення
    buttons.append(Button(170, 310, BUTTON_WIDTH, BUTTON_HEIGHT, "C", RED, WHITE))

    return buttons


def draw_display(screen, text):
    """Малювання дисплея калькулятора"""
    # Створення прямокутника для дисплея
    display_rect = pygame.Rect(10, 10, WINDOW_WIDTH - 20, DISPLAY_HEIGHT)

    # Заливка дисплея білим кольором
    pygame.draw.rect(screen, WHITE, display_rect)
    # Малювання рамки навколо дисплея
    pygame.draw.rect(screen, BLACK, display_rect, 2)

    # Створення тексту для відображення
    text_surface = font_large.render(text, True, BLACK)
    # Розміщення тексту справа на дисплеї (як в реальних калькуляторах)
    text_rect = text_surface.get_rect()
    text_rect.right = display_rect.right - 10
    text_rect.centery = display_rect.centery

    # Відображення тексту на екрані
    screen.blit(text_surface, text_rect)


def main():
    """Головна функція програми"""
    clock = pygame.time.Clock()  # Об'єкт для контролю FPS
    calculator = Calculator()  # Створення об'єкта калькулятора
    buttons = create_buttons()  # Створення всіх кнопок

    running = True
    while running:
        # Обробка подій (натискання клавіш, клік миші тощо)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Закриття програми при натисканні X
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Обробка натискання миші
                if event.button == 1:  # Ліва кнопка миші
                    mouse_pos = event.pos

                    # Перевірка натискання кожної кнопки
                    for button in buttons:
                        if button.is_clicked(mouse_pos):
                            button.is_pressed = True

                            # Обробка різних типів кнопок
                            if button.text.isdigit():
                                # Кнопка цифри
                                calculator.add_digit(int(button.text))
                            elif button.text in ["+", "-", "*", "/"]:
                                # Кнопка операції
                                calculator.set_operation(button.text)
                            elif button.text == "=":
                                # Кнопка дорівнює
                                calculator.calculate()
                            elif button.text == "C":
                                # Кнопка очищення
                                calculator.clear()

            elif event.type == pygame.MOUSEBUTTONUP:
                # Скидання стану натискання всіх кнопок
                for button in buttons:
                    button.is_pressed = False

        # Очищення екрану білим кольором
        screen.fill(WHITE)

        # Малювання дисплея з поточним текстом
        draw_display(screen, calculator.display_text)

        # Малювання всіх кнопок
        for button in buttons:
            button.draw(screen)

        # Оновлення дисплея для відображення змін
        pygame.display.flip()

        # Обмеження FPS до 60 кадрів на секунду
        clock.tick(60)

    # Завершення pygame при виході з програми
    pygame.quit()
    sys.exit()


# Запуск програми
if __name__ == "__main__":
    main()