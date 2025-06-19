import ionread_python as ionread
import numpy as np
from abc import ABC, abstractmethod
from typing import Union
import numpy as np
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


def show_ionogram(
    ionogram: Union['ionread.Ionogram', None], 
    ion_arr: np.ndarray, 
    path: str = None,
    grid_alpha: float = 0.5,
    tick_alpha: float = 0.9,
    label_alpha: float = 1.0,
    title_alpha: float = 1.0,
    dpi: int = 100,
    colorbar: bool = True
):
    '''
    Отображает ионограмму со шкалами, нарисованными непосредственно на изображении
    
    Параметры:
    ----------
    ionogram : Объект ионограммы
    ion_arr : Массив данных ионограммы
    path : Путь для сохранения
    grid_alpha : Прозрачность сетки (0-1)
    tick_alpha : Прозрачность подписей шкал (0-1)
    label_alpha : Прозрачность названий осей (0-1)
    title_alpha : Прозрачность заголовка (0-1)
    dpi : Разрешение изображения
    colorbar : Отображать цветовую шкалу
    '''
    # Настройка стиля
    plt.style.use('default')
    plt.rcParams.update({
        'font.size': 12,
        'text.color': 'white',
        'figure.dpi': dpi,
        'savefig.dpi': dpi,
        'figure.facecolor': 'black',
        'axes.facecolor': 'black'
    })

    # Создание фигуры
    fig = plt.figure(figsize=(10, 8), facecolor='black')
    ax = fig.add_axes([0, 0, 1, 1])  # Оси на всю фигуру
    
    # Получение границ данных
    min_height = min(ionogram.data, key=lambda x: x.num_dist).dist - 1
    max_height = max(ionogram.data, key=lambda x: x.dist).dist
    min_freq = ionogram.passport.start_freq
    max_freq = ionogram.passport.end_freq
    
    # Отображение с указанием реальных границ
    im = ax.imshow(
        ion_arr,
        origin='lower',
        cmap='jet',
        aspect='auto',
        extent=[min_freq, max_freq, min_height, max_height]
    )
    
    # Удаление стандартных элементов осей
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Рисование сетки
    ax.grid(True, color='white', linestyle='--', alpha=grid_alpha)
    
    # Ручная отрисовка подписей шкал
    # Для оси Y (задержки)
    y_ticks = np.linspace(min_height, max_height, 10)[1:-1]
    for y in y_ticks:
        ax.text(
            min_freq + (max_freq - min_freq) * 0.01,  # X-позиция (левый край + отступ)
            y,                                       # Y-позиция
            f'{y:.2f}',                              # Форматированное значение
            color='white', 
            va='center',                             # Вертикальное выравнивание
            alpha=tick_alpha,
            fontsize=10
        )
    
    # Для оси X (частоты)
    x_ticks = np.linspace(min_freq, max_freq, 10)[1:-1]
    for x in x_ticks:
        ax.text(
            x,                                       # X-позиция
            min_height + (max_height - min_height) * 0.01,  # Y-позиция (низ + отступ)
            f'{x/1000:.1f}',                         # Конвертация в МГц
            color='white',
            ha='center',                             # Горизонтальное выравнивание
            va='bottom',
            alpha=tick_alpha,
            fontsize=10,
            rotation=0                              # Наклон подписей
        )
    
    # Подписи осей
    ax.text(
        min_freq + (max_freq - min_freq) * 0.01,     # X-позиция
        max_height * 0.95,                           # Y-позиция (верх - отступ)
        'Задержка, мс', 
        color='white', 
        alpha=label_alpha,
        fontsize=14,
        va='top'
    )
    
    ax.text(
        (min_freq + max_freq) / 2,                   # Центр по X
        min_height - (max_height - min_height) * 0.05+50,  # Под графиком
        'Частота, МГц',
        color='white',
        alpha=label_alpha,
        fontsize=14,
        ha='center'
    )
    
    # Заголовок
    # title = f'{ionogram.passport.transmitter}-{ionogram.passport.receiver}\n' \
    #         f'{ionogram.passport.session_date} {ionogram.passport.session_time}'
    # ax.set_title(title, size=18, alpha=title_alpha, pad=20, color='white')
    
    # Цветовая шкала
    if colorbar:
        cax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cax)
        cbar.ax.tick_params(colors='white', labelsize=10)
        cbar.outline.set_edgecolor('white')
    
    # Сохранение с прозрачным фоном
    if path is not None:
        plt.savefig(path, bbox_inches='tight', pad_inches=0, transparent=True, dpi=dpi)
    
    plt.close()
    
ionogram = ionread.read_ionogram(
    'test_data/01_02_07_20_00.dat')
# Выводим паспорт (метаданные) ионограммы
ionogram.passport
# Из объекта ионограммы получаем двумерную матрицу (numpy - массив)
ionogram_array_builder = SimpleIonogramArrayBuilder(
    ionogram=ionogram).process()
ionogram_array = ionogram_array_builder.get_ndarray()
# Показываем ионограмму
show_ionogram(
    ionogram,
    ionogram_array,
    path="fullscreen_ionogram.png",
    grid_alpha=1.0,
    tick_alpha=1.0,
    dpi=150
)