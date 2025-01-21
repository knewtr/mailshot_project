from django.db import models


class Recipient(models.Model):
    email = models.CharField(
        max_length=30, unique=True, verbose_name="Электронная почта"
    )
    name = models.CharField(max_length=100, verbose_name="ФИО получателя")
    comment = models.TextField(verbose_name="Комментарий")

    class Meta:
        verbose_name = "получатель"
        verbose_name_plural = "получатели"

    def __str__(self):
        return self.email


class Message(models.Model):
    theme = models.CharField(max_length=50, verbose_name="Тема письма")
    content = models.TextField(verbose_name="Тело письма")

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

    def __str__(self):
        return self.theme


class Mailshot(models.Model):
    STATUS = (
        ("1", "Завершена"),
        ("2", "Создана"),
        ("3", "Запущена"),
    )
    first_mailshot = models.DateTimeField(verbose_name="Первая отправка")
    last_mailshot = models.DateTimeField(verbose_name="Окончание отправки")
    status = models.CharField(max_length=50, choices=STATUS, verbose_name="Статус")
    message = models.ForeignKey("Message", on_delete=models.CASCADE)
    receivers = models.ManyToManyField("Recipient")

    # def __str__(self):
    #     return


class Attempt(models.Model):
    STATUS = (
        ("1", "Успешно"),
        ("2", "Не успешно"),
    )

    try_time = models.DateTimeField(verbose_name="Время попытки")
    status = models.CharField(max_length=20, choices=STATUS, verbose_name="Статус")
    response = models.TextField(verbose_name="Ответ сервера")
    mailshot = models.ForeignKey("Mailshot", on_delete=models.CASCADE)

    def __str__(self):
        return self.status
