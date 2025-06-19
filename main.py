import ionread_python as ionread
import numpy as np
from abc import ABC, abstractmethod
from typing import Union
from matplotlib import pyplot as plt

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


def show_ionogram(ionogram: Union[ionread.Ionogram, None], ion_arr, path: str = None):
    '''
    Отобразить предсказания ионограммы поверх оригинала
    '''

    plt.rcParams.update({'font.size': 12})

    plt.rcParams["figure.figsize"] = (8, 8)
    plt.rcParams['axes.facecolor'] = 'white'
    fig, ax = plt.subplots()

    im = ax.imshow(ion_arr, origin='lower', cmap='jet')

    fig.colorbar(im, ax=ax)

    min_height_num = min(ionogram.data, key=lambda x: x.num_dist)
    max_height = max(ionogram.data, key=lambda x: x.dist)

    min_freq = ionogram.passport.start_freq
    max_freq = ionogram.passport.end_freq

    d_ticks = np.linspace(0, ion_arr.shape[0], 20)

    d_ticks_labels = [f'{dn / 300:.2f}' for dn in np.linspace(
        min_height_num.dist - 1, max_height.dist, len(d_ticks))]

    f_ticks = np.linspace(0, ion_arr.shape[1], 10)

    f_ticks_labels = [
        f'{fn / 1000:.1f}' for fn in np.linspace(min_freq, max_freq, len(f_ticks))]

    ax.set_yticks(d_ticks)
    ax.set_yticklabels(d_ticks_labels, size=12)

    ax.set_xticks(f_ticks)
    ax.set_xticklabels(f_ticks_labels, size=12, rotation=45)

    ax.set_facecolor("white")

    ax.grid(which='major', color='gray', linestyle='--')

    ax.grid(which='minor', color='gray', linestyle='--')

    ax.set_xlabel('Частота, МГц', labelpad=20,
                  size=14, color='black')
    ax.set_ylabel('Задержка, мс', labelpad=20,
                  size=14, color='black')

    first_line = f'{ionogram.passport.transmitter}-{ionogram.passport.receiver}'
    second_line = f'{ionogram.passport.session_date} {ionogram.passport.session_time}'

    ax.set_title(f'{first_line} \n {second_line}', size=18)

    if (path != None):
        plt.savefig(path, bbox_inches='tight')

    plt.show()

ionogram = ionread.read_ionogram(
    'ionogram_show/test_data/01_02_07_20_00.dat')
ionogram.passport
ionogram_array_builder = SimpleIonogramArrayBuilder(
    ionogram=ionogram).process()
ionogram_array = ionogram_array_builder.get_ndarray()
show_ionogram(ionogram, ionogram_array,"")