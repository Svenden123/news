import json
import xml.etree.ElementTree as ET
import sys
from collections import Counter


MIN_WORD_LENGTH = 7 # минимальная длина слова
ITEMS_TO_DISPLAY = 10 # кол-во самых частых слов, которые будут выводиться на экран
PUNCTUATION = '.,!?' # знаки препинания, которые будут удаляться из предложений


def read_json(file_name):
    '''Чтение JSON файла'''
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def parse_json(data):
    '''Извлечение новостей из JSON файла'''
    items = data['rss']['channel']['items']
    return [item['description'] for item in items]


def read_xml(file_name):
    '''Чтение XML файла'''
    return ET.parse(file_name)


def parse_xml(tree):
    '''Извлечение нвостей из XML файла'''
    items = tree.findall('./channel/item/description')
    return [item.text for item in items]


def remove_punctuation(s):
    '''Заменяет знаки препинания на пробелы'''
    for char in PUNCTUATION:
        s = s.replace(char, ' ')    
    return s


def get_long_words(news):
    '''Принимает список новостей, и возвращает список слов длиннее минимального значения'''    
    long_words = []
    for item in news:
        # убираем знаки препинания и разбиваем строку по пробелам
        all_words = remove_punctuation(item).split()

        # убираем слова короче минимально значения
        # title() - чтобы привести слова к единому формату (иначе 'слово' и 'Слово' считались бы разными словами)
        words = [word.title() for word in all_words if len(word) >= MIN_WORD_LENGTH]
        long_words.extend(words)
    return long_words


def process(file_name, reader, parser):
    '''Здесь происходит основной процесс обработки'''
    data = reader(file_name) # чтение файла
    news = parser(data) # извлечение новостей
    words = get_long_words(news) # получаем список слов длиннее минимального значения
    counter = Counter(words) # подсчёт кол-ва слов
    print(*counter.most_common(ITEMS_TO_DISPLAY), sep='\n') # вывод самых частых слов


def main(file_name):
    extension = file_name.split('.')[-1].lower() # расширение файла

    # в зависиости от расширения назначаем функции чтения и парсинга
    if extension == 'json':
        reader = read_json
        parser = parse_json
    elif extension == 'xml':
        reader = read_xml
        parser = parse_xml
    else:
        print('Неподдерживаемый формат файла')
        return
    process(file_name, reader, parser)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Формат запуска: python news.py <имя_файла>')
        sys.exit(1)
    main(sys.argv[1])