from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    DecimalField,
    DateField,
    SubmitField,
    IntegerField
)
from wtforms.validators import DataRequired, Optional, Email


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class ClientForm(FlaskForm):
    client_type = SelectField(
        "Тип клиента",
        choices=[
            ("Физическое лицо", "Физическое лицо"),
            ("Юридическое лицо", "Юридическое лицо"),
            ("Муниципальный заказчик", "Муниципальный заказчик"),
            ("Индивидуальный предприниматель", "Индивидуальный предприниматель"),
            ("Поставщик", "Поставщик")
        ],
        validators=[DataRequired()]
    )

    name = StringField("Наименование / ФИО клиента", validators=[DataRequired()])
    inn = StringField("ИНН", validators=[Optional()])
    kpp = StringField("КПП", validators=[Optional()])
    ogrn = StringField("ОГРН", validators=[Optional()])
    phone = StringField("Телефон", validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Email()])
    address = StringField("Адрес", validators=[Optional()])
    representative = StringField("Представитель", validators=[Optional()])
    tags_text = StringField("Метки клиента", validators=[Optional()])
    note = TextAreaField("Примечание", validators=[Optional()])
    submit = SubmitField("Сохранить")


class ObjectForm(FlaskForm):
    name = StringField("Название объекта", validators=[DataRequired()])
    address = StringField("Адрес объекта", validators=[Optional()])
    district = StringField("Район", validators=[Optional()])
    work_type = StringField("Вид работ", validators=[Optional()])

    status = SelectField(
        "Статус",
        choices=[
            ("Планируется", "Планируется"),
            ("В работе", "В работе"),
            ("Завершен", "Завершен"),
            ("Приостановлен", "Приостановлен")
        ],
        validators=[DataRequired()]
    )

    start_date = DateField("Дата начала", validators=[Optional()])
    end_date = DateField("Дата окончания", validators=[Optional()])
    submit = SubmitField("Сохранить")


class ContractForm(FlaskForm):
    number = StringField("Номер договора", validators=[DataRequired()])
    title = StringField("Наименование договора", validators=[DataRequired()])

    contract_type = SelectField(
        "Тип договора",
        choices=[
            ("Договор подряда", "Договор подряда"),
            ("Договор поставки", "Договор поставки"),
            ("Муниципальный контракт", "Муниципальный контракт"),
            ("Коммерческое предложение", "Коммерческое предложение"),
            ("Иной документ", "Иной документ")
        ],
        validators=[DataRequired()]
    )

    contract_date = DateField("Дата договора", validators=[Optional()])
    start_date = DateField("Дата начала работ / поставки", validators=[Optional()])
    end_date = DateField("Дата окончания работ / поставки", validators=[Optional()])

    amount = DecimalField("Сумма договора", validators=[Optional()])
    vat_rate = StringField("НДС", validators=[Optional()])

    status = SelectField(
        "Статус",
        choices=[
            ("Планируется", "Планируется"),
            ("Действующий", "Действующий"),
            ("На исполнении", "На исполнении"),
            ("На приемке", "На приемке"),
            ("Исполнен", "Исполнен"),
            ("Просрочен", "Просрочен"),
            ("Расторгнут", "Расторгнут")
        ],
        validators=[DataRequired()]
    )

    client_id = SelectField("Клиент / заказчик", coerce=int, validators=[DataRequired()])
    object_id = SelectField("Объект", coerce=int, validators=[Optional()])

    contractor_name = StringField("Подрядчик / исполнитель", validators=[Optional()])
    supplier_name = StringField("Поставщик", validators=[Optional()])

    acceptance_place = StringField("Место приемки", validators=[Optional()])
    delivery_terms = TextAreaField("Условия поставки / выполнения работ", validators=[Optional()])
    acceptance_procedure = TextAreaField("Порядок сдачи-приемки", validators=[Optional()])

    warranty_months = IntegerField("Гарантийный срок, месяцев", validators=[Optional()])
    penalty_terms = TextAreaField("Санкции / неустойка", validators=[Optional()])

    description = TextAreaField("Описание", validators=[Optional()])
    document = FileField("Документ договора / акта / КП")

    submit = SubmitField("Сохранить")


class AcceptanceActForm(FlaskForm):
    act_number = StringField("Номер акта", validators=[DataRequired()])
    act_date = DateField("Дата акта", validators=[Optional()])

    act_type = SelectField(
        "Тип акта",
        choices=[
            ("Акт выполненных работ", "Акт выполненных работ"),
            ("КС-2", "КС-2"),
            ("КС-3", "КС-3"),
            ("Акт сдачи-приемки", "Акт сдачи-приемки")
        ],
        validators=[DataRequired()]
    )

    work_name = StringField("Наименование работ", validators=[Optional()])

    amount = DecimalField("Стоимость без НДС", validators=[Optional()])
    vat_amount = DecimalField("Сумма НДС", validators=[Optional()])
    total_amount = DecimalField("Итого с НДС", validators=[Optional()])

    acceptance_place = StringField("Место приемки", validators=[Optional()])

    acceptance_status = SelectField(
        "Статус приемки",
        choices=[
            ("Подготовлен", "Подготовлен"),
            ("На подписании", "На подписании"),
            ("Подписан", "Подписан"),
            ("Отклонен", "Отклонен")
        ],
        validators=[DataRequired()]
    )

    signed_by_customer = StringField("Подписант заказчика", validators=[Optional()])
    signed_by_contractor = StringField("Подписант подрядчика", validators=[Optional()])
    comment = TextAreaField("Комментарий", validators=[Optional()])

    submit = SubmitField("Сохранить акт")


class DocumentUploadForm(FlaskForm):
    document_type = SelectField(
        "Тип документа",
        choices=[
            ("Договор", "Договор"),
            ("Акт КС-2", "Акт КС-2"),
            ("Справка КС-3", "Справка КС-3"),
            ("Коммерческое предложение", "Коммерческое предложение"),
            ("Смета", "Смета"),
            ("Прочий документ", "Прочий документ")
        ],
        validators=[DataRequired()]
    )

    file = FileField("Файл PDF/DOCX", validators=[DataRequired()])
    submit = SubmitField("Загрузить документ")


class LeadForm(FlaskForm):
    title = StringField("Тема обращения", validators=[DataRequired()])
    lead_date = DateField("Дата обращения", validators=[DataRequired()])

    source = SelectField(
        "Источник обращения",
        choices=[
            ("Сайт", "Сайт"),
            ("Телефон", "Телефон"),
            ("Email", "Email"),
            ("Личное обращение", "Личное обращение"),
            ("Рекомендация", "Рекомендация"),
            ("Муниципальный заказ", "Муниципальный заказ"),
            ("Повторное обращение", "Повторное обращение"),
            ("Иное", "Иное")
        ],
        validators=[DataRequired()]
    )

    status = SelectField(
        "Статус заявки",
        choices=[
            ("Новая", "Новая"),
            ("В обработке", "В обработке"),
            ("Расчет сметы", "Расчет сметы"),
            ("Коммерческое предложение", "Коммерческое предложение"),
            ("Договор", "Договор"),
            ("Отказ", "Отказ"),
            ("Закрыта", "Закрыта")
        ],
        validators=[DataRequired()]
    )

    priority = SelectField(
        "Приоритет",
        choices=[
            ("Низкая", "Низкая"),
            ("Обычная", "Обычная"),
            ("Высокая", "Высокая"),
            ("Срочная", "Срочная")
        ],
        validators=[DataRequired()]
    )

    client_id = SelectField("Связанный клиент", coerce=int, validators=[Optional()])
    object_id = SelectField("Связанный объект", coerce=int, validators=[Optional()])
    contract_id = SelectField("Связанный договор", coerce=int, validators=[Optional()])

    contact_person = StringField("Контактное лицо", validators=[Optional()])
    phone = StringField("Телефон", validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Email()])

    work_type = StringField("Вид работ", validators=[Optional()])
    object_address = StringField("Адрес объекта / предполагаемое место работ", validators=[Optional()])
    estimated_budget = DecimalField("Предварительный бюджет", validators=[Optional()])

    responsible = StringField("Ответственный сотрудник", validators=[Optional()])
    comment = TextAreaField("Комментарий", validators=[Optional()])

    submit = SubmitField("Сохранить заявку")


class TaskForm(FlaskForm):
    title = StringField("Задача", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[Optional()])

    task_type = SelectField(
        "Тип задачи",
        choices=[
            ("Звонок клиенту", "Звонок клиенту"),
            ("Документы", "Документы"),
            ("Оплата", "Оплата"),
            ("Сроки работ", "Сроки работ"),
            ("Встреча", "Встреча"),
            ("Задача", "Задача")
        ],
        validators=[DataRequired()]
    )

    priority = SelectField(
        "Приоритет",
        choices=[
            ("Низкая", "Низкая"),
            ("Обычная", "Обычная"),
            ("Высокая", "Высокая"),
            ("Срочная", "Срочная")
        ],
        validators=[DataRequired()]
    )

    status = SelectField(
        "Статус",
        choices=[
            ("Новая", "Новая"),
            ("В работе", "В работе"),
            ("Выполнена", "Выполнена"),
            ("Просрочена", "Просрочена"),
            ("Отменена", "Отменена")
        ],
        validators=[DataRequired()]
    )

    due_date = DateField("Срок выполнения", validators=[Optional()])
    responsible = StringField("Ответственный сотрудник", validators=[Optional()])

    client_id = SelectField("Клиент", coerce=int, validators=[Optional()])
    contract_id = SelectField("Договор", coerce=int, validators=[Optional()])
    lead_id = SelectField("Заявка", coerce=int, validators=[Optional()])

    submit = SubmitField("Сохранить задачу")