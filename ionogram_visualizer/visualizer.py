import numpy as np
from matplotlib import pyplot as plt
from typing import Optional, Union
import ionread_python as ionread

class IonogramVisualizer:
    """
    Класс для визуализации ионограмм с настраиваемыми параметрами отображения.
    """
    
    def __init__(self, style_settings: Optional[dict] = None):
        """
        Инициализация визуализатора с настройками стиля.
        
        :param style_settings: Словарь с настройками стиля matplotlib
        """
        self.default_style = {
            'font.size': 12,
            'text.color': 'white',
            'figure.facecolor': 'black',
            'axes.facecolor': 'black'
        }
        self.style_settings = style_settings or self.default_style
        
    def show_ionogram(
        self,
        ionogram: Union['ionread.Ionogram', None],
        ion_arr: np.ndarray,
        path: Optional[str] = None,
        grid_alpha: float = 0.5,
        tick_alpha: float = 0.9,
        label_alpha: float = 1.0,
        title_alpha: float = 1.0,
        dpi: int = 100,
        colorbar: bool = True,
        figsize: tuple = (10, 8)
    ) -> None:
        """
        Отображает ионограмму с настраиваемыми параметрами.
        
        :param ionogram: Объект ионограммы из ionread
        :param ion_arr: Массив данных ионограммы
        :param path: Путь для сохранения изображения
        :param grid_alpha: Прозрачность сетки (0-1)
        :param tick_alpha: Прозрачность подписей шкал (0-1)
        :param label_alpha: Прозрачность названий осей (0-1)
        :param title_alpha: Прозрачность заголовка (0-1)
        :param dpi: Разрешение изображения
        :param colorbar: Отображать цветовую шкалу
        :param figsize: Размер фигуры (ширина, высота)
        """
        # Применение стиля
        plt.style.use('default')
        plt.rcParams.update(self.style_settings)
        plt.rcParams.update({
            'figure.dpi': dpi,
            'savefig.dpi': dpi
        })

        # Создание фигуры
        fig = plt.figure(figsize=figsize, facecolor='black')
        ax = fig.add_axes([0, 0, 1, 1])
        
        # Получение границ данных
        min_height = min(ionogram.data, key=lambda x: x.num_dist).dist - 1
        max_height = max(ionogram.data, key=lambda x: x.dist).dist
        min_freq = ionogram.passport.start_freq
        max_freq = ionogram.passport.end_freq
        
        # Отображение данных
        im = ax.imshow(
            ion_arr,
            origin='lower',
            cmap='jet',
            aspect='auto',
            extent=[min_freq, max_freq, min_height, max_height]
        )
        
        # Настройка осей
        self._configure_axes(ax, min_freq, max_freq, min_height, max_height, 
                           grid_alpha, tick_alpha, label_alpha)
        
        # Цветовая шкала
        if colorbar:
            self._add_colorbar(fig, im)
        
        # Сохранение или отображение
        if path:
            plt.savefig(path, bbox_inches='tight', pad_inches=0, transparent=True, dpi=dpi)
        plt.close()
    
    def _configure_axes(
        self,
        ax,
        min_freq: float,
        max_freq: float,
        min_height: float,
        max_height: float,
        grid_alpha: float,
        tick_alpha: float,
        label_alpha: float
    ) -> None:
        """Настраивает оси и подписи."""
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Сетка
        ax.grid(True, color='white', linestyle='--', alpha=grid_alpha)
        
        # Подписи шкал
        y_ticks = np.linspace(min_height, max_height, 10)[1:-1]
        for y in y_ticks:
            ax.text(
                min_freq + (max_freq - min_freq) * 0.01,
                y,
                f'{y:.2f}',
                color='white', 
                va='center',
                alpha=tick_alpha,
                fontsize=10
            )
        
        x_ticks = np.linspace(min_freq, max_freq, 10)[1:-1]
        for x in x_ticks:
            ax.text(
                x,
                min_height + (max_height - min_height) * 0.01,
                f'{x/1000:.1f}',
                color='white',
                ha='center',
                va='bottom',
                alpha=tick_alpha,
                fontsize=10
            )
        
        # Подписи осей
        ax.text(
            min_freq + (max_freq - min_freq) * 0.01,
            max_height * 0.95,
            'Задержка, мс', 
            color='white', 
            alpha=label_alpha,
            fontsize=14,
            va='top'
        )
        
        ax.text(
            (min_freq + max_freq) / 2,
            min_height - (max_height - min_height) * 0.05 + 50,
            'Частота, МГц',
            color='white',
            alpha=label_alpha,
            fontsize=14,
            ha='center'
        )
    
    def _add_colorbar(self, fig, im) -> None:
        """Добавляет цветовую шкалу."""
        cax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(im, cax=cax)
        cbar.ax.tick_params(colors='white', labelsize=10)
        cbar.outline.set_edgecolor('white')