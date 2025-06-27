from ionogram_visualizer import  SimpleIonogramArrayBuilder
import ionread_python as ionread
import numpy as np
from matplotlib import pyplot as plt
from typing import Optional, Union
import ionread_python as ionread
from matplotlib.colors import ListedColormap

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
            'font.size': 10,
            'text.color': 'black',
            'figure.facecolor': 'black',
            'axes.facecolor': 'black'
        }
        self.style_settings = style_settings or self.default_style
    
        
    def show_ionogram(
        self,
        ionogram: Union['ionread.Ionogram', None],
        ion_arr: np.ndarray,
        path: Optional[str] = None,
        alphas: float = 0.5,
        dpi: int = 100,
        colorbar: bool = True,
        scale:int = 1
    ) -> None:
        """
        Отображает ионограмму с настраиваемыми параметрами.
        
        :param ionogram: Объект ионограммы из ionread
        :param ion_arr: Массив данных ионограммы
        :param path: Путь для сохранения изображения
        :param alphas: Прозрачность элементов (0-1)
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
        width_px = ion_arr.shape[0]
        height_px = ion_arr.shape[1]

        width_in = width_px / dpi
        height_in = height_px / dpi
        figsize=(height_in*scale,width_in*scale)

        # Создание фигуры с белым фоном
        fig = plt.figure(figsize=figsize, facecolor='white')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('white')  # Устанавливаем белый фон для области данных
        
        # Получение границ данных
        min_height = min(ionogram.data, key=lambda x: x.num_dist).dist 
        max_height = max(ionogram.data, key=lambda x: x.dist).dist
        min_freq = ionogram.passport.start_freq
        max_freq = ionogram.passport.end_freq

        # Создаем модифицированную цветовую карту с белым для низких значений
        jet = plt.get_cmap('jet', 256)
        newcolors = jet(np.linspace(0, 1, 256))
        # Делаем первые N значений белыми (можно настроить в зависимости от ваших данных)
        newcolors[0, :] = np.array([1, 1, 1, 1])  # белый цвет с полной непрозрачностью
        white_jet = ListedColormap(newcolors)

        # Отображение данных с белым фоном для низких значений
        im = ax.imshow(
            ion_arr,
            origin='lower',
            cmap=white_jet,
            aspect='auto',
            extent=[min_freq, max_freq, min_height, max_height]  # Отсекаем самые низкие значения
        )
        
        # Настройка осей
        self._configure_axes(ax, min_freq, max_freq, min_height, max_height, alphas)
        
        # Цветовая шкала
        if colorbar:
            self._add_colorbar(fig, im, alphas)

        # Заголовок
        first_line = f'{ionogram.passport.transmitter}-{ionogram.passport.receiver}'
        second_line = f'{ionogram.passport.session_date} {ionogram.passport.session_time}'
        title = f'{first_line}\n{second_line}'
        ax.text(0.5, 0.97, title, transform=ax.transAxes, fontsize=20, color='black', ha='center', va='top', alpha=alphas)
        
        # Сохранение или отображение
        if path:
            plt.savefig(path, bbox_inches='tight', pad_inches=0, facecolor='white', dpi=dpi)
        plt.close()

        
    
    def _configure_axes(
        self,
        ax,
        min_freq: float,
        max_freq: float,
        min_height: float,
        max_height: float,
        alphas: float
    ) -> None:
        """Настраивает оси и подписи."""
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Сетка
        freq_ticks = np.linspace(min_freq, max_freq, 10)
        for freq in freq_ticks:
            ax.axvline(
                x=freq, 
                color='black', 
                linestyle='--', 
                linewidth=0.5, 
                alpha=alphas,
                zorder=3  
            )

        # Горизонтальные линии (высоты)
        height_ticks = np.linspace(min_height, max_height, 20)
        for height in height_ticks:
            ax.axhline(
                y=height, 
                color='black', 
                linestyle='--', 
                linewidth=0.5, 
                alpha=alphas,
                zorder=3
            )
    
        
        # Подписи шкал
        y_ticks = np.linspace(min_height, max_height, 20)[1:-1]
        for y in y_ticks:
            ax.text(
                min_freq + (max_freq - min_freq) * 0.01,
                y,
                f'{y/300:.2f}',
                color='black', 
                va='center',
                alpha=alphas,
                fontsize=10
            )
        
        x_ticks = np.linspace(min_freq, max_freq, 10)[1:-1]
        for x in x_ticks:
            ax.text(
                x,
                min_height + (max_height - min_height) * 0.01,
                f'{x/1000:.1f}',
                color='black',
                ha='center',
                va='bottom',
                alpha=alphas,
                fontsize=10
            )
        #Подписи осей
        ax.text(0.5, 0.1, 'Частота, МГц', transform=ax.transAxes,
                fontsize=12, color='black', ha='center', va='top', alpha=alphas)

        ax.text(0.08, 0.5, 'Задержка, мс', transform=ax.transAxes,
                fontsize=12, color='black', ha='right', va='center', rotation=90, alpha=alphas)
    
    def _add_colorbar(self, fig, im, alphas) -> None:
        """Добавляет цветовую шкалу с настраиваемой прозрачностью всех элементов."""
        # Создаем ось для colorbar
        cax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
        
        # Добавляем colorbar
        cbar = fig.colorbar(im, cax=cax)
        
        # Настройка прозрачности фона и границ
        cbar.ax.set_facecolor((0, 0, 0, 0)) 
        cbar.outline.set_edgecolor('black')   
        cbar.outline.set_alpha(alphas)        
        
       
        cbar.solids.set_alpha(alphas)        
        
    
        cbar.ax.tick_params(
            colors='black',         
            width=1,              
            labelsize=10        
        )
        for label in cbar.ax.get_yticklabels():
            label.set_alpha(alphas) 
       
        for tick in cbar.ax.yaxis.get_major_ticks():
            tick.tick1line.set_alpha(alphas)  
            tick.tick2line.set_alpha(alphas)  
            
        # Дополнительные настройки прозрачности
        cbar.ax.patch.set_alpha(0)          
        for spine in cbar.ax.spines.values():
            spine.set_alpha(alphas)
            