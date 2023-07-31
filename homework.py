from dataclasses import dataclass, asdict
from typing import Union, Optional


@dataclass
class InfoMessage:
    """
    Info message about the training.

    Attributes
    ----------
    training_type: str
        workout type.
    duration: float
        workout duration.
    distance: float
        traveled distance.
    speed: float
        mean speed.
    calories: float
        spent calories.

    Methods
    -------
    get_message() -> str:
        return info about training results.
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Return info message."""
        message_template: str = ('Тип тренировки: {training_type}; '
                                 'Длительность: {duration:.3f} ч.; '
                                 'Дистанция: {distance:.3f} км; '
                                 'Ср. скорость: {speed:.3f} км/ч; '
                                 'Потрачено ккал: {calories:.3f}.')
        return message_template.format(**asdict(self))


class Training:
    """
    Training base class.

    Attributes
    ----------
    action: int
        number of steps or strokes.
    duration: float
        workout duration.
    weight: float
        person's weight.

    Methods
    -------
    get_distance() -> float:
        get the distance in km.
    get_mean_speed() -> float:
        get mean speed during the traning.
    get_spent_calories() -> float:
        get the number of burned calories.*
    show_training_info(class_name, duration, speed, calories) -> str:
        create obj Infomessage with info about the training.

    * Method get_spent_calories() has to be redefined in inherited classes.

    Parameters
    ----------
    LEN_STEP: float
        step length in meters.
    M_IN_KM: int
        conversion factor meters to kilometers.
    H_IN_M: int
        conversion factor hours to minutes.
    """

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """Class Training attributes."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get the distance in km."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get mean speed during the traning."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Get the number of burned calories."""
        raise NotImplementedError('Define get_spent_calories() '
                                  f'in {type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """Create InfoMessage with info about the training."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """
    Training: run.

    Class inherits all the main attributes,
    methods, parameters of the Training class.

    Additional parameters
    ---------------------
    CALORIES_MEAN_SPEED_MULTIPLIER: int
        mean speed coefficient for spent calories calculation.
    CALORIES_MEAN_SPEED_SHIFT: float
        mean speed shift for calories calculation.

    Overridden methods
    ------------------
    get_spent_calories()
    """

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Get the number of burned calories."""
        calories: float = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
            * self.duration * self.H_IN_M
        )
        return calories


class SportsWalking(Training):
    """
    Training: race walking.

    Class inherits all the main attributes,
    methods, parameters of the Training class.

    Additional attributes
    ---------------------
    height: float
        person's height in cantimeters.

    Overridden methods
    ------------------
    get_spent_calories()

    Additional parameters
    ---------------------
    CALORIES_WEIGHT_MULTIPLIER_1: float
        weight multiplier for spent calories calculation.
    CALORIES_WEIGHT_MULTIPLIER_2: float
        weight multiplier for spent calories calculation.
    KM_PER_H_IN_M_PER_S: float
        conversion factor km/h to m/s.
    CM_IN_M: int
        conversion factor cantimeters to meters.
    """

    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029
    KM_PER_H_IN_M_PER_S: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        """Class SportsWalking attributes."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Get the number of burned calories."""
        calories: float = (
            (self.CALORIES_WEIGHT_MULTIPLIER_1 * self.weight
             + ((self.get_mean_speed() * self.KM_PER_H_IN_M_PER_S)**2
                / (self.height / self.CM_IN_M))
                * self.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight)
            * self.duration * self.H_IN_M
        )
        return calories


class Swimming(Training):
    """
    Training: swimming.

    Class inherits all the main attributes,
    methods, parameters of the Training class.

    Additional attributes
    ---------------------
    length_pool: float
        pool length in meters.
    count_pool: int
        number of pool crossing.

    Overridden methods
    ------------------
    get_mean_speed()
    get_spent_calories()

    Additional parameters
    ---------------------
    LEN_STEP: float
        stroke length.
    CALORIES_MEAN_SPEED_ADDITION: float
        mean speed shift for calories calculation.
    CALORIES_MEAN_SPEED_MULTIPLIER: int
        mean speed coefficient for spent calories calculation.
    """

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_ADDITION: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        """Class Swimming attributes."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Get mean speed during the traning."""
        speed: float = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return speed

    def get_spent_calories(self) -> float:
        """Get the number of burned calories."""
        calories: float = (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_ADDITION)
            * self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight * self.duration
        )
        return calories


def check_data(workout_type: str,
               data: list[Union[int, float]]) -> Optional[str]:
    """Check data in package."""
    result: Optional[str] = None
    if workout_type == 'SWM' and len(data) != 5:
        result = 'Некорректное количество аргументов.'
    elif workout_type == 'RUN' and len(data) != 3:
        result = 'Некорректное количество аргументов.'
    elif workout_type == 'WLK' and len(data) != 4:
        result = 'Некорректное количество аргументов.'
    elif not (35 < data[2] < 610):
        result = 'Неверно указанный вес.'
    elif workout_type == 'SWM' and not (1 < data[3] < 1013):
        result = ('Неверно указана длина бассейна. '
                  'Необходимо указать длину в м.')
    elif workout_type == 'WLK' and not (50 < data[3] < 251):
        result = 'Неверно указан рост. Необходимо указать рост в см.'
    elif workout_type not in workouts:
        result = 'Неверно указан шифр тренировки.'

    return result


def read_package(workout_type: str, data: list) -> Training:
    """Read data from sensors."""
    return workouts[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


workouts: dict[str, type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}

if __name__ == '__main__':
    packages: list[tuple[str, list[Union[int, float]]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('PLT', [12000, 1, 60]),
        ('SWM', [230, 1, 70, 0.25, 38]),
        ('RUN', [23000, 1.15, 655]),
        ('WLK', [4000, 2, 60, 1.65]),
        ('SWM', [340, 4, 60, 3000]),
    ]

    for workout_type, data in packages:
        check_data_result: Optional[str] = check_data(workout_type, data)
        if check_data_result:
            raise ValueError(check_data_result)

        training: Training = read_package(workout_type, data)
        main(training)
