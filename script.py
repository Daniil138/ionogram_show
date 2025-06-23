#!/usr/bin/env python3
import argparse
from ionogram_visualizer import IonogramVisualizer, SimpleIonogramArrayBuilder
import ionread_python as ionread


def main():
    parser = argparse.ArgumentParser(description="Визуализация ионограммы из .dat файла.")
    parser.add_argument("file_path", type=str, help="Путь к входному .dat файлу")
    parser.add_argument("--grid_alpha", type=float, default=1.0, help="Прозрачность сетки (0.0 - 1.0)")
    parser.add_argument("--tick_alpha", type=float, default=1.0, help="Прозрачность меток (0.0 - 1.0)")
    parser.add_argument("--dpi", type=int, default=150, help="Разрешение изображения (DPI)")
    parser.add_argument("--output", type=str, default="fullscreen_ionogram.png",
                        help="Путь для сохранения изображения")

    args = parser.parse_args()

    # Проверка корректности значений
    if not (0.0 <= args.grid_alpha <= 1.0):
        parser.error("grid_alpha должен быть в диапазоне [0.0, 1.0]")
    if not (0.0 <= args.tick_alpha <= 1.0):
        parser.error("tick_alpha должен быть в диапазоне [0.0, 1.0]")
    if args.dpi <= 0:
        parser.error("dpi должно быть положительным целым числом")

    try:
        # Загрузка данных
        ionogram = ionread.read_ionogram(args.file_path)

        # Создание массива ионограммы
        ionogram_array = SimpleIonogramArrayBuilder(ionogram).process().get_ndarray()

        # Визуализация
        visualizer = IonogramVisualizer()
        visualizer.show_ionogram(
            ionogram,
            ionogram_array,
            path=args.output,
            grid_alpha=args.grid_alpha,
            tick_alpha=args.tick_alpha,
            dpi=args.dpi
        )
        print(f"Изображение успешно сохранено: {args.output}")

    except Exception as e:
        parser.error(f"Ошибка при обработке файла: {e}")


if __name__ == "__main__":
    main()