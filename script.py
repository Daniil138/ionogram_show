#!/usr/bin/env python3
import argparse
from ionogram_visualizer import IonogramVisualizer, SimpleIonogramArrayBuilder
import ionread_python as ionread


def main():
    # Парсинг аргументов
    parser = argparse.ArgumentParser(description="Визуализация ионограммы из .dat файла.")
    parser.add_argument("file_path", type=str, help="Путь к входному .dat файлу")
    parser.add_argument("--alpha", type=float, default=1.0, help="Прозрачность (0.0 - 1.0)")
    parser.add_argument("--dpi", type=int, default=150, help="Разрешение изображения (DPI)")
    parser.add_argument("--scale", type=int, default=1, help="Разрешение размер изображения относительно исходного массива")
    parser.add_argument("--output", type=str, default="fullscreen_ionogram.png",
                        help="Путь для сохранения изображения")

    args = parser.parse_args()

    if not (0.0 <= args.alpha <= 1.0):
        parser.error("alpha должен быть в диапазоне [0.0, 1.0]")
    if args.dpi <= 0:
        parser.error("dpi должно быть положительным целым числом")

    try:
        # Загрузка данных
        ionogram = ionread.read_ionogram(args.file_path)

        # Получение массива 
        ionogram_array = SimpleIonogramArrayBuilder(ionogram).process().get_ndarray()

        # Визуализация
        visualizer = IonogramVisualizer()
        visualizer.show_ionogram(
            ionogram,
            ionogram_array,
            path=args.output,
            alphas=args.alpha,
            dpi=args.dpi
        )
        print(f"Изображение успешно сохранено: {args.output}")

    except Exception as e:
        parser.error(f"Ошибка при обработке файла: {e}")


if __name__ == "__main__":
    main()