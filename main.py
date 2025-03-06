from PIL import Image, ImageDraw, ImageFont

def resize_image(image, max_size=100):
    """
    Уменьшает размер изображения, сохраняя пропорции и учитывая соотношение сторон символов.

    :param image: Исходное изображение.
    :param max_size: Максимальная ширина или высота выходного изображения.
    :return: Уменьшенное изображение.
    """
    width, height = image.size

    # Коррекция для соотношения сторон символов (символы выше, чем шире)
    aspect_ratio_correction = 0.75  # Символы в два раза выше, чем шире
    scale_factor = min(max_size / width, max_size / (height * aspect_ratio_correction))

    # Вычисляем новые размеры
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor * aspect_ratio_correction)

    return image.resize((new_width, new_height))


def image_to_ascii(image_path, max_size=100):
    """
    Преобразует изображение в ASCII-арт с корректным соотношением сторон.

    :param image_path: Путь к исходному изображению.
    :param max_size: Максимальная ширина или высота выходного ASCII-арта.
    :return: ASCII-арт, ширина, высота и уменьшенное изображение.
    """
    try:
        # Загружаем и уменьшаем изображение
        original_image = Image.open(image_path).convert("RGB")
        resized_image = resize_image(original_image, max_size)
        width, height = resized_image.size

        # Создаем строку всех печатаемых ASCII-символов
        ascii_chars = [chr(i) for i in range(32, 127)]

        # Преобразуем каждый пиксель в ASCII-символ
        ascii_art = []
        for y in range(height):
            row = ""
            for x in range(width):
                r, g, b = resized_image.getpixel((x, y))
                brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                ascii_index = int(brightness * (len(ascii_chars) - 1))
                row += ascii_chars[ascii_index]
            ascii_art.append(row)

        return ascii_art, width, height, resized_image

    except Exception as e:
        print(f"Ошибка при создании ASCII-арта: {e}")
        return None, None, None, None


def save_ascii_as_image(ascii_art, width, height, resized_image, output_path="ascii_art.png", font_size=15):
    """
    Сохраняет ASCII-арт в виде изображения с черным фоном и цветными символами.

    :param ascii_art: Список строк с ASCII-символами.
    :param width: Ширина изображения.
    :param height: Высота изображения.
    :param resized_image: Уменьшенное изображение для получения цветов пикселей.
    :param output_path: Путь для сохранения результата.
    :param font_size: Размер шрифта.
    """
    try:
        # Создаем изображение с черным фоном
        font = ImageFont.truetype("arial.ttf", font_size)
        line_height = font.getbbox("A")[3]  # Высота одной строки
        char_width = font.getbbox("A")[2]   # Ширина одного символа

        # Корректируем размеры изображения
        image_width = width * char_width
        image_height = height * line_height

        image = Image.new("RGB", (image_width, image_height), color="#131313")
        draw = ImageDraw.Draw(image)

        # Рисуем ASCII-символы на изображении
        y_position = 0
        for y, row in enumerate(ascii_art):
            x_position = 0
            for x, char in enumerate(row):
                # Получаем цвет пикселя из уменьшенного изображения
                r, g, b = resized_image.getpixel((x, y))
                draw.text((x_position, y_position), char, font=font, fill=(r, g, b))
                x_position += char_width
            y_position += line_height

        # Сохраняем изображение
        image.save(output_path)
        print(f"ASCII-арт успешно сохранен как изображение: {output_path}")

    except Exception as e:
        print(f"Ошибка при сохранении ASCII-арта как изображения: {e}")


if __name__ == "__main__":
    # Путь к вашему изображению
    image_path = r""

    # Генерация ASCII-арта
    max_size = 100  # Максимальная ширина или высота ASCII-арта
    ascii_art, width, height, resized_image = image_to_ascii(image_path, max_size)

    if ascii_art and width and height and resized_image:
        # Сохранение ASCII-арта в виде изображения
        save_ascii_as_image(ascii_art, width, height, resized_image, output_path="ascii_art.png", font_size=15)