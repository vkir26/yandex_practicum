"""
Фитнес-трекер, который обрабатывает данные для трёх видов тренировок:
бега, спортивной ходьбы и плавания.
"""


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # для множителя средней скорости
    CALORIES_MEAN_SPEED_SHIFT = 1.79  # для сдвига средней скорости

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (self.MIN_IN_H * self.duration)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # Коэффициент для расчёта калорий. Для множителя веса спортсмена
    K_1 = 0.035
    # Множитель частного квадрата средней скорости и роста спортсмена
    K_2 = 0.029
    # Для перевода значений из км/ч в м/с
    KMH_IN_MSEC = 0.278
    # Для перевода значений из сантиметров в метры
    CM_IN_M = 100

    def __init__(self, action: int, duration: float, weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        # Числовым коэффициентам тоже нужны имена, не стоит забывать про это.
        # Но это не касается, например, значения степени.
        m_sec = self.get_mean_speed() * self.KMH_IN_MSEC  # км/ч в м/с
        height_in_m = self.height / self.CM_IN_M  # Получаем рост в метрах
        h_in_min = self.MIN_IN_H * self.duration  # Переводим часы в минуты
        return (
            self.K_1 * self.weight + (m_sec**2 / height_in_m) * self.K_2 * self.weight
        ) * h_in_min


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # Один гребок при плавании
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    commands = {
        "SWM": Swimming,  # Плавание
        "RUN": Running,  # Бег
        "WLK": SportsWalking,  # Спортивная ходьба
    }

    return commands[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = InfoMessage
    print(info.get_message(training.show_training_info()))


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
