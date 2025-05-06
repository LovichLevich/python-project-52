### Hexlet tests and linter status:
[![Actions Status](https://github.com/LovichLevich/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/LovichLevich/python-project-52/actions)



# Менеджер задач

[Посмотреть на render.com]( https://python-project-52-lk27.onrender.com )

**Менеджер задач** – это веб-приложение, которое позволяет:

 - зарегистрироваться в приложении, используя предлагаемую регистрационную форму;
 - войти в систему, используя данные из формы;
 - видеть список всех зарегистрированных **_пользователей_** на соответствующей странице без авторизации;
 - изменять или удалять информацию о себе.
   Если пользователь является автором или исполнителем задания, его удаление недоступно;
 - Просматривать, добавлять, обновлять и удалять **_статусы и метки задач_** после входа в систему.
   Статусы и метки, соответствующие каким-либо задачам, не могут быть удалены;
 - Просматривать, добавлять, обновлять и удалять **_задачи_** после входа в систему.
    Удалять задачи может только их создатель.
    Также достуана выборка задач на соответствующей странице с указанием статусов, исполнителей и меток.


## Требования к установке
```
* Python 3.10.
```


## Установка

1. Склонировать репозиторий:
```
https://github.com/LovichLevich/python-project-52.git
```

2. Прейти в директорию проекта и установить его:
```
cd python-project-52
make install
```

3. Создать `.env` в корне директории:
```
DATABASE_URL= #Для локальной разработки используется sqlite3, для деплоя PostgreSQL  
SECRET_KEY= #Необходимо задать/сгенерировать для Django  
ROLLBAR_ACCESS_TOKEN= # Необходим для сервиса Rollbar Error Tracker
```


## Проверка кода проекта линтером _ruff_
```
ruff check task_manager
```


## Запуск
Локально:
```
make migrate
make dev
```

На render.com:
```
* Создать БД (PostgreSQL): https://docs.render.com/databases
* Build Command: make install db-clean install migrate
* Start Command: make start
```
