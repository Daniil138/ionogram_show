import ionread_python as ionread
import numpy as np
from abc import ABC, abstractmethod
from src.BaseIonogramArrayBuilder import BaseIonogramArrayBuilder



class SimpleIonogramArrayBuilder(BaseIonogramArrayBuilder):
    def __init__(self, ionogram: ionread.ionogram) -> None:
        super().__init__(ionogram)

    # @override
    def get_point_position(self, freq_MHz, delay_ms):
        '''
        Вычислить координаты точки на основе физических величин
        returns
            t_freq - доля на частотной шкале от 0 до 1
            freq_coord - номер позиции в массиве
        '''
        ionogram = self.ionogram
        ion_arr = self.__ion_arr__

        min_freq = ionogram.passport.start_freq
        max_freq = ionogram.passport.end_freq

        f = freq_MHz * 1000
        t_freq = (f - min_freq) / (max_freq - min_freq)
        freq_coord = round(ion_arr.shape[1] * t_freq)

        max_height = max(ionogram.data, key=lambda x: x.dist)
        min_delay = ionogram.passport.latency
        max_delay = (max_height.dist) / 300
        t_delay = (delay_ms - min_delay) / (max_delay - min_delay)

        # Теперь вычислим координату (Примерную)
        delay_coord = round(ion_arr.shape[0] * t_delay)

        return t_freq, freq_coord, t_delay, delay_coord

    def process(self):
        ionogram = self.ionogram

        min_height_num = min(ionogram.data, key=lambda x: x.num_dist)
        max_height = max(ionogram.data, key=lambda x: x.num_dist)

        min_freq = ionogram.passport.start_freq
        max_freq = ionogram.passport.end_freq

        h = list(range(min_height_num.num_dist, int(
            max_height.num_dist) + 1, 1))  # h начинается с 1

        f = list(range(min_freq + ionogram.passport.step_freq, max_freq +
                       ionogram.passport.step_freq, ionogram.passport.step_freq))

        width = len(f)
        height = len(h)
        ion_arr = np.full((height, width), 0)

        for bin in ionogram.data:
            # Определим координату по высоте
            h_coor = h.index(bin.num_dist)

            # Определим координату по частоте
            f_coor = f.index(bin.freq)

            ion_arr[h_coor, f_coor] = bin.ampl

        # Зануляем служебную информацию, не относящуюся непосредственно к ионограмме
        ion_arr[0, :] = 0
        self.__ion_arr__ = ion_arr
        return self