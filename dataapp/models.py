from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


from .managers import (
    CompanyManager,
    CompanyQuerySet,
    DealManager,
    CompanyStatisticManager,
    DirectionActualManager,
    # CompanyNewManager,
    # CompanyNewQuerySet
)


class User(models.Model):
    """ Список пользователей.
    Метод: user.get;
    Поля: id пользователя в BX24, имя, фамилия, отчество, url фотографии, должность """
    ALLOWED_EDIT_CHOICE = (
        ('0', 'Запрещено'),
        ('1', 'Ограниченно разрешено'),
        ('2', 'Разрешено'),
    )
    ID = models.PositiveIntegerField(primary_key=True, verbose_name='ID пользователя в BX24',
                                     unique=True, db_index=True)
    LAST_NAME = models.CharField(verbose_name='Фамилия', max_length=35, blank=True, null=True)
    NAME = models.CharField(verbose_name='Имя', max_length=35, blank=True, null=True)
    UF_DEPARTMENT = models.PositiveIntegerField(verbose_name='ID департамета', db_index=True)

    ACTIVE = models.BooleanField(verbose_name='Пользователь активен (не уволен)', default=True, db_index=True)
    URL = models.URLField(verbose_name='URL пользователя', max_length=150, blank=True, null=True)

    STATUS_DISPLAY = models.BooleanField(verbose_name='Вывод пользователя в статистике подразделения', default=True, db_index=True)
    ALLOWED_EDIT = models.CharField(verbose_name='Доступ к редактированию данных', max_length=1,
                                    choices=ALLOWED_EDIT_CHOICE, default="0")
    ALLOWED_SETTING = models.BooleanField(verbose_name='Доступ к настройкам приложения', default=False)
    ALLOWED_STATUS_DAY = models.BooleanField(verbose_name='Доступ к изменению статуса дня', default=False)
    ALLOWED_VERIFICATION_MSG = models.BooleanField(verbose_name='Доступ к верификации сообщений', default=False)

    def __str__(self):
        return '{} {}'.format(self.LAST_NAME or "-", self.NAME or "")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Direction(models.Model):
    """ Направления (СОУТ, Энергоаудит и т.д.)
    Методы: crm.dealcategory.list => [{ID: ..., NAME: ...}, ...];
            crm.deal.fields => UF_CRM_1610523951 => [{ID: ..., VALUE: ...}, ...] - для направления 43 (отдел продаж)
    """
    ID = models.PositiveIntegerField(primary_key=True, verbose_name='ID направления в BX24', unique=True, db_index=True)
    VALUE = models.CharField(verbose_name='Название направления', max_length=50)
    new = models.BooleanField(verbose_name='Новое напрвление', default=True, db_index=True)
    general_id_bx = models.IntegerField(verbose_name='ID направления в BX24 (для совместимости со старыми направлениями)')

    objects = models.Manager()
    direction_actual = DirectionActualManager()

    def __str__(self):
        return f"{self.ID} - {self.general_id_bx}. {self.VALUE}"

    class Meta:
        verbose_name = 'Направление сделки'
        verbose_name_plural = 'Направления сделок'


class Stage(models.Model):
    STATUS_DEAL_CHOICES = [
        ("PREPARATION", 'Подготовка к работе'),
        ("WORK", 'В работе'),
        ("WON", 'Успешна'),
        ("FAILURE", 'Провалена'),
    ]
    ID = models.PositiveIntegerField(primary_key=True, verbose_name='ID стадии в BX24', unique=True, db_index=True)
    STATUS_ID = models.CharField(verbose_name='Аббревиатура стадии сделки', max_length=35, db_index=True)
    NAME = models.CharField(verbose_name='Название стадии сделки', max_length=150)
    won = models.BooleanField(verbose_name='Сделка завершена успешно', default=False, db_index=True)
    status = models.CharField(max_length=11, choices=STATUS_DEAL_CHOICES, blank=True, null=True, db_index=True)
    direction = models.ForeignKey(Direction, verbose_name='Направление', on_delete=models.CASCADE, related_name='stage',
                                  blank=True, null=True, db_index=True)

    def __str__(self):
        return f"{self.STATUS_ID} - {self.NAME}"

    class Meta:
        verbose_name = 'Стадия сделки'
        verbose_name_plural = 'Стадии сделки'


class Company(models.Model):
    ID = models.PositiveIntegerField(primary_key=True, verbose_name='ID компании в BX24', unique=True, db_index=True)
    TITLE = models.CharField(verbose_name="Название компании", max_length=300, blank=True, null=True, db_index=True)
    DATE_CREATE = models.DateTimeField(verbose_name='Дата создания', blank=True, null=True)
    ADDRESS = models.CharField(verbose_name='Адрес компании', max_length=300, blank=True, null=True)
    REVENUE = models.DecimalField(verbose_name='Годовой оборот', max_digits=15, decimal_places=2, default=0, blank=True, null=True, db_index=True)
    INDUSTRY = models.CharField(verbose_name='Сфера деятельности', max_length=25, blank=True, null=True, db_index=True)

    sector = models.CharField(verbose_name='Отрасль', max_length=150, blank=True, null=True, db_index=True)
    region = models.CharField(verbose_name='Регион', max_length=150, blank=True, null=True, db_index=True)
    source = models.CharField(verbose_name='Источник компании', max_length=150, blank=True, null=True, db_index=True)
    number_employees = models.IntegerField(verbose_name='Количество сотрудников', blank=True, null=True, db_index=True)
    district = models.CharField(verbose_name='Район области', max_length=150, blank=True, null=True)
    main_activity = models.CharField(verbose_name='Основной вид деятельности', max_length=500, blank=True, null=True)
    other_activities = models.CharField(verbose_name='Другие виды деятельности', max_length=2000, blank=True, null=True)
    profit = models.DecimalField(verbose_name='Чистая прибыль', max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    active = models.BooleanField(verbose_name='Компания активна (не удалена)', default=True, db_index=True)

    inn = models.CharField(verbose_name='ИНН компании', max_length=15, blank=True, null=True, db_index=True)
    requisite_region = models.CharField(verbose_name='Реквизит - район', max_length=150, blank=True, null=True, db_index=True)
    requisites_city = models.CharField(verbose_name='Реквизит - город', max_length=750, blank=True, null=True, db_index=True)
    requisites_province = models.CharField(verbose_name='Реквизит - область', max_length=150, blank=True, null=True, db_index=True)

    # Заполняется при добавлении активности
    date_last_communication = models.DateTimeField(verbose_name='Дата последней коммуникации', blank=True, null=True)
    # Заполняется при добавлении сделки
    summa_by_company_success = models.DecimalField(verbose_name='Сумма успешных сделок', max_digits=17, decimal_places=2, default=0, blank=True, null=True)
    summa_by_company_work = models.DecimalField(verbose_name='Сумма сделок в работе', max_digits=17, decimal_places=2, default=0, blank=True, null=True)

    ASSIGNED_BY_ID = models.ForeignKey(User, verbose_name='Ответственый в BX24', on_delete=models.SET_NULL,
                                       related_name='company', blank=True, null=True, db_index=True)

    objects = CompanyManager.from_queryset(CompanyQuerySet)()
    statistic = CompanyStatisticManager()

    def __str__(self):
        return f"{self.ID}. {self.TITLE or ' - '}"

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Deal(models.Model):
    ID = models.PositiveIntegerField(verbose_name='id сделки в BX24', unique=True, db_index=True)
    TITLE = models.CharField(verbose_name='Название сделки', max_length=350, blank=True, null=True)
    DATE_CREATE = models.DateTimeField(verbose_name='Дата создания сделки', blank=True, null=True)
    DATE_MODIFY = models.DateTimeField(verbose_name='Дата последнего изменения', blank=True, null=True)
    CLOSEDATE = models.DateTimeField(verbose_name='Дата завершения сделки', blank=True, null=True)
    date_last_communication = models.DateTimeField(verbose_name='Дата последней коммуникации', blank=True, null=True)
    CLOSED = models.BooleanField(verbose_name='Сделка завершена', default=False)

    opportunity = models.DecimalField(verbose_name='Сумма сделки', max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    balance_on_payments = models.DecimalField(verbose_name='Остаток по оплатам', max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    amount_paid = models.DecimalField(verbose_name='Всего оплат на сумму', max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    active = models.BooleanField(verbose_name='Сделка активна (не удалена)', default=True, db_index=True)

    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE, related_name='deal', blank=True, null=True, db_index=True)
    direction = models.ForeignKey(Direction, verbose_name='Направление', on_delete=models.CASCADE, related_name='deal', blank=True, null=True, db_index=True)
    stage = models.ForeignKey(Stage, verbose_name='Стадия', on_delete=models.CASCADE, related_name='deal', blank=True, null=True, db_index=True)

    objects = DealManager()

    def __str__(self):
        return f"{self.ID}. {self.TITLE or ' - '}"

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'


class Activity(models.Model):
    COMPLETED_CHOICE = (
        ('Y', 'Завернено'),
        ('N', 'Не завершено'),
    )
    DIRECTION_CHOICE = (
        ('0', '-'),
        ('1', 'Входящее'),
        ('2', 'Исходящее'),
    )
    TYPE_CHOICE = (
        ('1', 'Встреча'),
        ('2', 'Звонок'),
        ('3', 'Задача'),
        ('4', 'Письмо'),
    )
    OWNER_TYPE_CHOICE = (
        ('1', 'Лид'),
        ('2', 'Сделка'),
        ('3', 'Контакт'),
        ('4', 'Компания'),
    )
    STATUS_CHOICE = (
        ('0', '-'),
        ('1', '-'),
        ('2', 'Ожидается'),
        ('3', 'Завершено'),
        ('4', 'Завершено автоматически'),
    )

    ID = models.PositiveIntegerField(primary_key=True, verbose_name='ID дела в BX24', unique=True, db_index=True)
    COMPLETED = models.CharField(verbose_name='Заершено дело или нет', max_length=1, choices=COMPLETED_CHOICE)
    DIRECTION = models.CharField(verbose_name='Направление дела (входящее/исходящее)', max_length=1,
                                 choices=DIRECTION_CHOICE, db_index=True)
    TYPE_ID = models.CharField(verbose_name='Тип дела (встреча/звонрок/...)', max_length=1,
                               choices=TYPE_CHOICE, db_index=True)
    STATUS = models.CharField(verbose_name='Статус дела', max_length=1, choices=STATUS_CHOICE)
    OWNER_TYPE_ID = models.CharField(verbose_name='Тип сущности к которой привязан звонок', max_length=1,
                                     blank=True, null=True, choices=OWNER_TYPE_CHOICE)
    OWNER_ID = models.PositiveIntegerField(verbose_name='ID сущности к которой привязан звонок',
                                           blank=True, null=True)
    OWNER_NAME = models.CharField(verbose_name='Название сущности к которой привязан звонок', max_length=950,
                                  blank=True, null=True)
    CREATED = models.DateTimeField(verbose_name='Дата создания дела', blank=True, null=True, db_index=True)
    END_TIME = models.DateTimeField(verbose_name='Дата завершения дела', blank=True, null=True)
    active = models.BooleanField(verbose_name='Дело не удалено из Битрикс24', default=True, db_index=True)
    # Заполняется функцией post_save_phone - после сохранения записи звонка
    DURATION = models.PositiveIntegerField(verbose_name='Длительность звонка', blank=True, null=True, db_index=True)
    CALL_START_DATE = models.DateTimeField(verbose_name='Дата начала звонка', blank=True, null=True, db_index=True)

    COMPANY_ID = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.SET_NULL, related_name='activity', blank=True, null=True, db_index=True)
    RESPONSIBLE_ID = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL,
                                       related_name='activity', blank=True, null=True, db_index=True)

    def __str__(self):
        return str(self.ID) or "-"

    class Meta:
        verbose_name = 'Дело'
        verbose_name_plural = 'Дела'


class Phone(models.Model):
    CALL_TYPE_CHOICE = (
        ('1', 'Исходящий'),
        ('2', 'Входящий'),
        ('3', 'Входящий с перенаправлением'),
        ('4', 'Обратный звонок'),
    )
    CALL_ID = models.CharField(verbose_name='ID звонка в BX24', max_length=75, unique=True, db_index=True)
    CALL_TYPE = models.CharField(verbose_name='Тип звонка', max_length=1, choices=CALL_TYPE_CHOICE)
    PHONE_NUMBER = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True)
    CALL_DURATION = models.PositiveIntegerField(verbose_name='Длительность звонка', null=True, db_index=True)
    CALL_START_DATE = models.DateTimeField(verbose_name='Дата начала звонка', db_index=True)

    CRM_ACTIVITY_ID = models.ForeignKey(Activity, verbose_name='Дело', on_delete=models.SET_NULL,
                                        related_name='phone', blank=True, null=True, db_index=True)
    PORTAL_USER_ID = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL,
                                       related_name='phone', blank=True, null=True, db_index=True)
    # company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE, related_name='phone',
    #                             blank=True, null=True)

    def __str__(self):
        return self.CALL_ID or "-"

    class Meta:
        verbose_name = 'Звонок'
        verbose_name_plural = 'Звонки'


class ProductionCalendar(models.Model):
    DAY_TYPE_CHOICE = (
        ('week', 'Не рабочий день'),
        ('work', 'Рабочий день'),
    )
    date_calendar = models.DateField(verbose_name='Дата', unique=True)
    status = models.CharField(verbose_name='Статус дня (рабочий/нерабочий)', max_length=4, choices=DAY_TYPE_CHOICE,
                              default="work")

    def __str__(self):
        return f"{self.date_calendar.day}.{self.date_calendar.month}.{self.date_calendar.year}"

    class Meta:
        verbose_name = 'День из роизводственного календаря'
        verbose_name_plural = 'Производственный календарь'


class CallsPlan(models.Model):
    calendar = models.ForeignKey(ProductionCalendar, verbose_name='Дата из производственного календаря',
                                 on_delete=models.CASCADE, related_name='call_plan')
    employee = models.ForeignKey(User, verbose_name='Работник', on_delete=models.CASCADE, related_name='call_plan')
    count_calls = models.IntegerField(verbose_name='Количество звонков', blank=True, null=True)
    plan_completed = models.BooleanField(verbose_name='План на день выполнен', default=False)

    def __str__(self):
        return f"{self.employee.LAST_NAME} {self.employee.NAME} - " \
               f"{self.calendar.date_calendar.day}.{self.calendar.date_calendar.month}.{self.calendar.date_calendar.year}"

    class Meta:
        unique_together = ('calendar', 'employee')
        verbose_name = 'План по звонкам на день (NEW)'
        verbose_name_plural = 'План по звонкам (NEW)'


class Comment(models.Model):
    recipient = models.ForeignKey(User, verbose_name='Получатель', on_delete=models.CASCADE, related_name='recipient', db_index=True)
    commentator = models.ForeignKey(User, verbose_name='Комментатор', on_delete=models.CASCADE, related_name='commentator')
    date_comment = models.DateField(verbose_name='Дата комментария', db_index=True)
    date_comment_add = models.DateTimeField(verbose_name='Дата добавления комментария', db_index=True)
    comment = models.TextField(verbose_name='Комментарий')

    verified = models.BooleanField(verbose_name='Комментарий подтвержден', default=False)
    verified_by_user = models.ForeignKey(User, verbose_name='Пользователь который подтвердил комментарий',
                                         on_delete=models.CASCADE, related_name='verified_by_user', blank=True, null=True)
    date_verified = models.DateTimeField(verbose_name='Дата подтверждения', blank=True, null=True)

    def __str__(self):
        return f"{self.recipient.LAST_NAME} {self.recipient.NAME}: {self.date_comment}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


@receiver(post_save, sender=Deal)
def post_save_deal(instance, **kwargs):
    # Добавление в компанию суммы успешных сделок и сделок в работе
    company_obj_ = instance.company
    if company_obj_:
        deal_aggregate_obj_ = Deal.objects.only("company", "opportunity", "stage__status").filter(
            company=company_obj_.pk
        ).aggregate(
            summa_success=models.Sum("opportunity", filter=models.Q(stage__status="SUCCESSFUL")),
            summa_work=models.Sum("opportunity", filter=models.Q(stage__status="WORK"))
        )
        # print("deal_aggregate_obj_ = ", deal_aggregate_obj_)
        company_obj_.summa_by_company_success = deal_aggregate_obj_["summa_success"]
        company_obj_.summa_by_company_work = deal_aggregate_obj_["summa_work"]
        company_obj_.save()


@receiver(post_save, sender=Activity)
def post_save_activity(instance, **kwargs):
    # Добавление даты последней коммуникации с компанией
    if instance.COMPANY_ID:
        company_obj_ = Company.objects.filter(ID=instance.COMPANY_ID).first()
        if company_obj_:
            if not company_obj_.date_last_communication or company_obj_.date_last_communication < instance.CALL_START_DATE:
                company_obj_.date_last_communication = instance.CALL_START_DATE
                company_obj_.save()
    # phone_obj_ = Phone.objects.filter(CRM_ACTIVITY_ID=instance.ID).first()
    # if not phone_obj_ or not phone_obj_.CRM_ACTIVITY_ID:
    #     phone_obj_.CRM_ACTIVITY_ID
    #     phone_obj_.save()


@receiver(post_save, sender=Phone)
def post_save_phone(instance, **kwargs):
    activity_obj_ = instance.CRM_ACTIVITY_ID
    # Добавление к активности длительности и время начала разговора
    if activity_obj_:
        activity_obj_.DURATION = instance.CALL_DURATION
        activity_obj_.CALL_START_DATE = instance.CALL_START_DATE
        activity_obj_.save()

