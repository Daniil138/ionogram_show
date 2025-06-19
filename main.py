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