import os

from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    # + логинимся в патреон
    # TODO: загружаем последний id из файла базы данных
    # + смотрим id последнего поста
    # +     если id поста <= тому что в файле - новых постов нету, останавливаемся
    # + проверяем, есть ли последний id из файла на этой странице (запрос )
    # +     если нет, загружаем ещё одну пачку постов и повторяем проверку
    # + собираем все карточки постов в список
    # + Парсим все посты
    # TODO: отсекаем все посты с id, меньшим или равным id из файла
    # TODO: оставшиеся посты сортируем по возрастанию id и добавляем в файл базы данных
