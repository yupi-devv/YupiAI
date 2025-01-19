import json


async def append_to_json_file(data, filename):
    with open(filename, 'a+') as file:
        file.seek(0, 0)  # Перемещаемся в начало файла

        try:
            content = json.load(file)  # Пытаемся загрузить существующий контент
        except ValueError:  # Файл пустой или поврежден
            content = []

        content.append(data)  # Добавляем новые данные

        file.seek(0, 0)  # Возвращаемся в начало файла
        file.truncate()  # Очищаем файл
        json.dump(content, file, indent=4, ensure_ascii=False)  # Записываем обновленный контент
