# ionogram_show
Библиотека для отрисовки ионограмм в картинки подходящие для разметки датасетов.
## Пример исппользования 
```python
from ionogram_visualizer import IonogramVisualizer, SimpleIonogramArrayBuilder
import ionread_python as ionread

# Загрузка данных
ionogram = ionread.read_ionogram('test_data/01_02_07_20_00.dat')

# Создание массива ионограммы
builder = SimpleIonogramArrayBuilder(ionogram).process()
ionogram_array = builder.get_ndarray()

# Визуализация
visualizer = IonogramVisualizer()
visualizer.show_ionogram(
    ionogram,
    ionogram_array,
    path="fullscreen_ionogram.png",
    grid_alpha=1.0,
    tick_alpha=1.0,
    dpi=150
)
```
## Как использовать файл со скриптом 
```
python script.py test_data/01_02_07_20_00.dat --grid_alpha 0.5 --tick_alpha 0.8 --dpi 300 --output result.png
```

- file_path — Путь к входному .dat файлу с данными ионограммы
- --grid_alpha GRID_ALPHA — Прозрачность сетки (0.0 — прозрачная, 1.0 — непрозрачная)
- --tick_alpha TICK_ALPHA — Прозрачность подписей осей и меток
- --dpi DPI — Разрешение изображения в DPI (точек на дюйм)
- --output OUTPUT — Путь для сохранения изображения (по умолчанию: fullscreen_ionogram.png)