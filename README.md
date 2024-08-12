# Доска объявлений

---

Приложение позволяет зарегистированным пользователям создавать объявления с товарами    на продажу. Так же пользователи могут оставлять отзывы к разным товарам.

### Статусы и их возможности

---

1. **Незарегистрированный пользователь** может:
    - получить общий список объявлений
2. **Зарегистрированный пользователь** может:
    - получать список или отдельные объявления
    - создавать новые объявления
    - редактировать или удалять *свои* объявления
    - получать список или отдельные отзывы
    - оставлять новые отзывы
    - редактировать или удалять *свои* отзывы
3. **Администратор** (пользователь добавляется в группу администраторов через админку)
    - в дополнение к правам зарегистированного пользователя может удалять и редактировать любые объявления и отзывы

### Модели

---

1. Пользователь (User). Стандартная модель расширена следующими полями:
    - *email* - почта, **используется в качестве логина**
    - *phone* - телефон для связи
    - *role* - роль пользователя (доступны user и admin, поле скрыто от пользователя при создании и редактировании)
    - *image* - аватарка пользователя

2. Объявление (Ad)
    - *title* - название товара
    - *price* - цена
    - *description* - описание
    - *author* - пользователь, который создал объявление
    - *created_at* - дата и время создания объявления

3. Отзыв (Review)
    - *text* - текст отзыва
    - *ad* - объявление, под которым оставлен отзыв
    - *author* - пользователь, оставивший отзыв
    - *created_at* - дата и время создания отзыва

### Сброс и восстановление пароля

Зарегистированный пользователь может сбросить пароль и создать новый через электронную почту. 

Для этого пользователь должен отправить свой email POST-запросом на адрес ***/users/reset_password/***

```
{
"email": "example@mail.ru"
}
```
После этого ему на почту придет письмо с url адресом, который содержит данные для создания нового пароля (uid и token) - ***http://{host}/uid:{uid}/token:{token}/***

Далее по адресу ***/users/reset_password_confirm/*** пользователь должен сделать POST-запрос с данными из письма и новым паролем

```
{
"uid": "uid",
"token": "token",
"new_password": "some_new_password"
}
```

### Docker compose

Для запуска контейнера приложения с подключенной базой PostgreSQL нужно использовать команду 

`docker compose up -d --build`