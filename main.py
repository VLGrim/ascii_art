from PIL import Image, ImageDraw, ImageFont

def image_to_ascii(image_path):
    
    try:
        # Загрузка изображения и размеры
        original_image = Image.open(image_path).convert("RGB")
        width, height = original_image.size

        # Строка всех печатаемых ASCII-символов
        ascii_chars = [chr(i) for i in range(32, 127)]

        # Пиксель в ASCII-символ
        ascii_art = []
        for y in range(height):
            row = ""
            for x in range(width):
                r, g, b = original_image.getpixel((x, y))
                brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                ascii_index = int(brightness * (len(ascii_chars) - 1))
                row += ascii_chars[ascii_index]
            ascii_art.append(row)

        return ascii_art, width, height, original_image

    except Exception as e:
        print(f"Ошибка при создании ASCII-арта: {e}")
        return None, None, None, None


def save_ascii_as_image(ascii_art, width, height, original_image, output_path="ascii_art.png", font_size=10):
    
    try:
        # Создаем изображение с черным фоном
        font = ImageFont.truetype("arial.ttf", font_size)
        line_height = font.getbbox("A")[3]  # Высота одной строки
        image_width = width * font_size
        image_height = height * line_height

        image = Image.new("RGB", (image_width, image_height), color="black")
        draw = ImageDraw.Draw(image)

        # ASCII-символы на изображении
        y_position = 0
        for y, row in enumerate(ascii_art):
            x_position = 0
            for x, char in enumerate(row):
                # Цвет ориг пикселя
                r, g, b = original_image.getpixel((x, y))
                draw.text((x_position, y_position), char, font=font, fill=(r, g, b))
                x_position += font_size
            y_position += line_height

        
        image.save(output_path)
        print(f"ASCII-арт успешно сохранен как изображение: {output_path}")

    except Exception as e:
        print(f"Ошибка при сохранении ASCII-арта как изображения: {e}")


if __name__ == "__main__":
    #путь к фотке
    image_path = r"C:\Users\User\Desktop\_\ascii\PyMain\photo_2025-02-27_21-27-15.jpg"

    
    ascii_art, width, height, original_image = image_to_ascii(image_path)

    if ascii_art and width and height and original_image:
        
        save_ascii_as_image(ascii_art, width, height, original_image, output_path="ascii_art.png", font_size=10)