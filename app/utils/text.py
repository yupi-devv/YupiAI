import re

# Компилируем регулярные выражения для лучшей производительности
four_pattern = re.compile(r"#{4,} ")
three_pattern = re.compile(r"#{3,}")

def replace_and_format(text):
    # Заменяем символы и форматируем текст
    dd = text.replace('*', '_')
    d = dd.replace('**', '*')
    
    lines = d.split('\n')
    formatted_lines = []

    for line in lines:
        if four_pattern.search(line):
            line = four_pattern.sub("*", line) + '*'
        elif three_pattern.search(line):
            line = three_pattern.sub("•*", line) + '*•'
        formatted_lines.append(line)

    return '\n'.join(formatted_lines)

def split_text(text, max_length=4096):
    # Разделяем текст на абзацы
    paragraphs = re.split(r'\n{2,}', text)
    parts = []
    current_part = ""

    for paragraph in paragraphs:
        # Проверяем, если добавление следующего абзаца превышает лимит
        if len(current_part) + len(paragraph) + 2 > max_length:  # +2 для учета двух символов новой строки
            if current_part:  # Если текущая часть не пустая, добавляем ее
                parts.append(current_part.strip())
            current_part = paragraph  # Начинаем новый абзац
        else:
            current_part += "\n\n" + paragraph if current_part else paragraph

    # Добавляем последнюю часть, если она не пустая
    if current_part:
        parts.append(current_part.strip())

    return parts

async def answer_manipulate(text):
    formatted_text = replace_and_format(text)
    parts = split_text(formatted_text)
    return parts[0] if len(parts) == 1 else parts
