# Корректировщик успеваемости в электронном дневнике
Кастомная управляющая команда для исправления оценок, удаления замечаний и добавления комплиментов от учителя в электронном дневнике.
Работает с [электронным дневником](https://github.com/devmanorg/e-diary/tree/master), написанном на [Django](https://www.djangoproject.com/).

## Как исправить плохие оценки?
1. Зайти на сервер в папку с проектом
2. Склонировать данный репозиторий в папку ```datacenter/management/commands```
  ```
  git clone https://github.com/KozhevnikovM/devman-django-diary.git datacenter/management/commands
  ```
3. Выполнить команду
  ```
  python manage.py improve_grace "Иванов Иван"
  ```
  Ожидаемый вывод:
  ```
  Исправлено XX оценок
  Удалено YY замечаний
  ```
4. Для добавления случайно похвалы от учителя, запустить ```improve_grace``` с ключом ```--subject``` и названием урока:
  ```
  python manage.py improve_grace "Иванов Иван" --subject "Музыка"
  ```
  Ожидаемый вывод:
  ```
  Учитель Павлова Анна Ивановна похвалил Иванов Иван Иванович 1A: Ты многое сделал, я это вижу!
  ```
5. Замести следы вмешательства, удалить папку с командой:
  ```
  rm -rf datacenter/management
  ```
## Как развернуть тестовый проект локально:
1. Склонировать [Электронный дневник школы](https://github.com/devmanorg/e-diary/tree/master) к себе на компьютер
2. Скачать и распаковать [тестовую базу данных](https://dvmn.org/filer/canonical/1562234129/166/)
3. Устанвить и прописать переменные окружения в соответствии с [инструкцией](https://github.com/devmanorg/e-diary/tree/master#%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA)
4. Склонировать данный репозиторий в папку ```datacenter/management/commands```
  ```
  git clone https://github.com/KozhevnikovM/devman-django-diary.git datacenter/management/commands
  ```
 
 ## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
  
