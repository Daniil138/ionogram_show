import ionread_python as ionread
import numpy as np
from abc import ABC, abstractmethod




class BaseIonogramArrayBuilder(ABC):
    def __init__(self, ionogram: ionread.ionogram) -> None:
        super().__init__()

        self.ionogram = ionogram

    @abstractmethod
    def process(self):
        '''
        Расчитать матрицу  матрицу ионограммы и остальные служебные поля
        '''
        self.__ion_arr__ = None
        return self

    def get_ndarray(self) -> np.ndarray:
        """Получить ионограмму в виде массива
        Вызвайте этот метод после process

        Returns:
            np.ndarray: ионограмма в виде массива
        """
        return self.__ion_arr__

    @abstractmethod
    def get_point_position(self, freq_MHz, delay_ms):
        pass

    def get_point_physical_values(self, t_freq, t_delay):
        '''
        Вычислить физические величины, на которых проявляется ПИВ

        params
            t_freq - координата по частоте (от 0 до 1)
            t_delay - координата по задержке (от 0 до 1)

        returns
            freqMHz - частота в МГц
            delay_ms - задержка в мс
        '''
        ionogram = self.ionogram

        min_freq = ionogram.passport.start_freq
        max_freq = ionogram.passport.end_freq

        max_height = max(ionogram.data, key=lambda x: x.dist)
        min_delay = ionogram.passport.latency
        max_delay = (max_height.dist * 2) / 300

        t_freq = min_freq + ((max_freq - min_freq) * t_freq)
        t_delay = min_delay + ((max_delay - min_delay) * t_delay)

        return t_freq, t_delay
