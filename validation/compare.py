from ionogram_visualizer import  SimpleIonogramArrayBuilder
import ionread_python as ionread

import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.patches import Rectangle

# Загрузка данных
ionogram = ionread.read_ionogram('../test_data/01_02_07_20_00.dat')

# Создание массива ионограммы
builder = SimpleIonogramArrayBuilder(ionogram).process()
ionogram_array = builder.get_ndarray()
print("Размер исходного массива",ionogram_array.shape)
#Сохранение
plt.imsave(arr = ionogram_array, origin='lower', cmap='jet', fname="original_array.png")



# Загрузка изображений
img1 = plt.imread("result1.png")  # эталонное изображение
img2 = plt.imread("original_array.png")   # сгенерированное изображение

# Проверка размеров
print("Размер result1.png:", img1.shape)
print("Размер output.png:", img2.shape)

# Выбор области для сравнения (примерные координаты)
x, y = 100, 100  # начальная точка
width, height = 200, 200  # размер области

# Проверка, чтобы область не выходила за границы изображений
h1, w1 = img1.shape[0], img1.shape[1]
h2, w2 = img2.shape[0], img2.shape[1]
x = min(x, w1 - width, w2 - width)
y = min(y, h1 - height, h2 - height)

# Создание фигуры с 4 подграфиками
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Отображение полных изображений с выделенными областями
axes[0, 0].imshow(img1)
axes[0, 0].add_patch(Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='none'))
axes[0, 0].set_title('result1.png (оригинал)')

axes[0, 1].imshow(img2)
axes[0, 1].add_patch(Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='none'))
axes[0, 1].set_title('output.png (сгенерированное)')

# Отображение увеличенных областей
zoom_img1 = img1[y:y+height, x:x+width]
axes[1, 0].imshow(zoom_img1)
axes[1, 0].set_title(f'Увеличенная область (result1.png)\n[{x}:{x+width}, {y}:{y+height}]')

zoom_img2 = img2[y:y+height, x:x+width]
axes[1, 1].imshow(zoom_img2)
axes[1, 1].set_title(f'Увеличенная область (output.png)\n[{x}:{x+width}, {y}:{y+height}]')

plt.tight_layout()

# Сохранение в файл
plt.savefig("compare.png", dpi=300, bbox_inches='tight')
print("Сравнение сохранено в compare.png")

# plt.show()  # Раскомментируйте, если нужно также показать в интерфейсе