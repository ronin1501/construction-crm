import os
from datetime import date, timedelta
from decimal import Decimal

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import (
    User,
    Client,
    ConstructionObject,
    Contract,
    WorkStage,
    Payment,
    Document,
    AcceptanceAct,
    Lead,
    Task,
    ActivityLog,
)


app = create_app()


def create_sample_document(filename, content):
    upload_folder = app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    path = os.path.join(upload_folder, filename)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return os.path.getsize(path)


def add_log(action_type, description, user=None, client=None, contract=None, lead=None, task=None):
    log = ActivityLog(
        action_type=action_type,
        description=description,
        user_id=user.id if user else None,
        client_id=client.id if client else None,
        contract_id=contract.id if contract else None,
        lead_id=lead.id if lead else None,
        task_id=task.id if task else None,
    )
    db.session.add(log)


with app.app_context():
    today = date.today()

    print("Удаление старых таблиц...")
    db.drop_all()

    print("Создание новых таблиц...")
    db.create_all()

    print("Создание администратора...")
    admin = User(
        username="admin",
        password_hash=generate_password_hash("admin123")
    )
    db.session.add(admin)
    db.session.commit()

    print("Добавление клиентов и контрагентов...")

    client_1 = Client(
        client_type="Муниципальный заказчик",
        name="Администрация Римгорского сельского поселения",
        phone="+7 (87877) 2-39-59",
        email="rimgorka@bk.ru",
        address="КЧР, Малокарачаевский район, село Римгорское, улица Умара Алиева, 7а",
        representative="Узденов Таулан Анзорович",
        tags_text="Муниципальный заказчик, Благоустройство, Постоянный клиент",
        note="Муниципальный заказчик работ по благоустройству территории."
    )

    client_2 = Client(
        client_type="Муниципальный заказчик",
        name="Администрация Первомайского сельского поселения",
        phone="8 (87877) 2-38-37",
        email="pervomaiskoe.sel.pos@yandex.ru",
        address="КЧР, Малокарачаевский район, село Первомайское, улица Шоссейная, 73",
        representative="Байрамкулов Альберт Сагитович",
        tags_text="Муниципальный заказчик, Дворовые территории",
        note="Заказчик работ по ремонту дворовых территорий."
    )

    client_3 = Client(
        client_type="Муниципальный заказчик",
        name="Администрация Учкекенского сельского поселения",
        phone="+7 (87877) 2-81-61",
        email="uchkeken-sp.ucoz.com",
        address="КЧР, Малокарачаевский район, село Учкекен, улица Ижаева, 2",
        representative="Семенов Анзор Хаджи-Магомедович",
        tags_text="Муниципальный заказчик, Акты на контроле",
        note="Заказчик работ по благоустройству и строительству."
    )

    client_4 = Client(
        client_type="Индивидуальный предприниматель",
        name="ИП Алботова Фатима Умаровна",
        phone="+7 928 398-37-57",
        email="a-gfatima@mail.ru",
        address="КЧР, Малокарачаевский район, село Первомайское, улица Мостовая, 39",
        representative="Алботова Фатима Умаровна",
        tags_text="Частный заказчик, Нужна смета",
        note="Частный заказчик строительных и ремонтных работ."
    )

    client_5 = Client(
        client_type="Юридическое лицо",
        name="ООО «Архыз Оригинал»",
        address="Карачаево-Черкесская Республика, г. Черкесск",
        representative="Семенов В.В.",
        tags_text="Юридическое лицо, Проектные работы",
        note="Заказчик проектных работ по технологическому присоединению."
    )

    supplier_1 = Client(
        client_type="Поставщик",
        name="ООО «Барсуковская ПМК»",
        inn="2610801140",
        kpp="261001001",
        ogrn="1142651011799",
        phone="8 (86550) 911-12",
        email="bpmk26@mail.ru",
        address="Ставропольский край, Кочубеевский район, ст. Барсуковская, ул. Островная, 11",
        representative="Рябченко Анатолий Алексеевич",
        tags_text="Поставщик, Бетонные смеси",
        note="Поставщик бетонных смесей."
    )

    db.session.add_all([client_1, client_2, client_3, client_4, client_5, supplier_1])
    db.session.commit()

    for client in [client_1, client_2, client_3, client_4, client_5, supplier_1]:
        add_log("Создание клиента", f"Добавлен клиент «{client.name}».", user=admin, client=client)

    print("Добавление строительных объектов...")

    object_1 = ConstructionObject(
        name="Благоустройство общественной территории",
        address="КЧР, село Римгорское, улица Парниковая, 5",
        district="Малокарачаевский район",
        work_type="Благоустройство территории",
        status="Завершен",
        start_date=date(2024, 4, 1),
        end_date=date(2024, 7, 30)
    )

    object_2 = ConstructionObject(
        name="Благоустройство территории между МКД 81, 87, 89, 93",
        address="КЧР, село Первомайское",
        district="Малокарачаевский район",
        work_type="Благоустройство дворовой территории",
        status="Завершен",
        start_date=date(2024, 5, 10),
        end_date=date(2024, 9, 15)
    )

    object_3 = ConstructionObject(
        name="Ремонт дворовой территории",
        address="КЧР, село Первомайское, улица Шоссейная, 87",
        district="Малокарачаевский район",
        work_type="Ремонт дворовой территории",
        status="Завершен",
        start_date=date(2024, 6, 1),
        end_date=date(2024, 8, 25)
    )

    object_4 = ConstructionObject(
        name="Благоустройство села Учкекен",
        address="КЧР, село Учкекен",
        district="Малокарачаевский район",
        work_type="Благоустройство, устройство детской площадки",
        status="Завершен",
        start_date=date(2024, 7, 23),
        end_date=date(2024, 12, 3)
    )

    object_5 = ConstructionObject(
        name="Восстановление асфальтобетонного покрытия дорог и тротуаров",
        address="Районы Карачаево-Черкесской Республики",
        district="КЧР",
        work_type="Дорожные работы",
        status="Планируется",
        start_date=date(2026, 5, 1),
        end_date=date(2026, 7, 30)
    )

    object_6 = ConstructionObject(
        name="Технологическое присоединение энергопринимающих устройств",
        address="Карачаево-Черкесская Республика, г. Черкесск",
        district="г. Черкесск",
        work_type="Проектно-сметная и рабочая документация",
        status="В работе",
        start_date=date(2025, 10, 29),
        end_date=date(2026, 2, 28)
    )

    db.session.add_all([object_1, object_2, object_3, object_4, object_5, object_6])
    db.session.commit()

    print("Добавление договоров...")

    contract_1 = Contract(
        number="02/10",
        title="Договор подряда на выполнение проектных работ",
        contract_type="Договор подряда",
        contract_date=date(2025, 10, 29),
        start_date=date(2025, 10, 29),
        end_date=date(2026, 2, 28),
        amount=Decimal("1250000.00"),
        vat_rate="20%",
        status="Действующий",
        contractor_name="ООО «Дорожник»",
        acceptance_place="г. Черкесск",
        delivery_terms="Подрядчик выполняет проектно-сметную и рабочую документацию по техническому заданию заказчика.",
        acceptance_procedure="Результат работ передается заказчику комплектом документации в бумажном и электронном виде.",
        warranty_months=12,
        penalty_terms="Ответственность сторон определяется условиями договора и действующим законодательством Российской Федерации.",
        description="Разработка проектной документации по объекту технологического присоединения.",
        client_id=client_5.id,
        object_id=object_6.id
    )

    contract_2 = Contract(
        number="03-П/2024",
        title="Договор поставки бетонных смесей",
        contract_type="Договор поставки",
        contract_date=date(2024, 5, 23),
        start_date=date(2024, 5, 23),
        end_date=date(2024, 12, 31),
        amount=Decimal("680000.00"),
        vat_rate="20%",
        status="Исполнен",
        contractor_name="ООО «Дорожник»",
        supplier_name="ООО «Барсуковская ПМК»",
        acceptance_place="Объект покупателя",
        delivery_terms="Доставка товара осуществляется транспортом поставщика. Товар передается покупателю в срок, согласованный сторонами.",
        acceptance_procedure="Приемка товара производится полномочным представителем покупателя в присутствии представителя поставщика. Факт передачи подтверждается УПД, накладной или транспортной накладной.",
        warranty_months=0,
        penalty_terms="При просрочке оплаты может начисляться неустойка. При необоснованном отказе от приемки покупатель несет расходы, связанные с простоем, доставкой и возвратом товара.",
        description="Поставка бетонной смеси М200 В15 с учетом доставки на объект.",
        client_id=supplier_1.id,
        object_id=object_2.id
    )

    contract_3 = Contract(
        number="0179300003924000003",
        title="Муниципальный контракт на благоустройство села Учкекен",
        contract_type="Муниципальный контракт",
        contract_date=date(2024, 7, 23),
        start_date=date(2024, 7, 23),
        end_date=date(2024, 12, 3),
        amount=Decimal("9748905.04"),
        vat_rate="20%",
        status="Исполнен",
        contractor_name="ООО «Дорожник»",
        acceptance_place="КЧР, село Учкекен",
        delivery_terms="Подрядчик выполняет работы по благоустройству объекта в соответствии с условиями муниципального контракта, техническим заданием и сметной документацией.",
        acceptance_procedure="Приемка результата выполненных работ осуществляется заказчиком. Результат оформляется актом выполненных работ КС-2 и справкой КС-3.",
        warranty_months=36,
        penalty_terms="За нарушение сроков исполнения обязательств предусмотрены штрафы и неустойки согласно условиям муниципального контракта.",
        description="Выполнение работ по благоустройству села Учкекен.",
        client_id=client_3.id,
        object_id=object_4.id
    )

    contract_4 = Contract(
        number="БЛ-05/2024",
        title="Благоустройство территории Первомайского сельского поселения",
        contract_type="Договор подряда",
        contract_date=date(2024, 5, 10),
        start_date=date(2024, 5, 10),
        end_date=date(2024, 9, 15),
        amount=Decimal("3450000.00"),
        vat_rate="20%",
        status="Исполнен",
        contractor_name="ООО «Дорожник»",
        acceptance_place="КЧР, село Первомайское",
        delivery_terms="Выполнение комплекса работ по благоустройству дворовой территории.",
        acceptance_procedure="Работы принимаются заказчиком после фактического выполнения и оформления акта.",
        warranty_months=24,
        penalty_terms="Санкции применяются при нарушении сроков и ненадлежащем качестве работ.",
        description="Благоустройство территории между многоквартирными домами.",
        client_id=client_2.id,
        object_id=object_2.id
    )

    contract_5 = Contract(
        number="КП-24/04",
        title="Коммерческое предложение на восстановление асфальтобетонного покрытия",
        contract_type="Коммерческое предложение",
        contract_date=date(2026, 4, 24),
        start_date=date(2026, 5, 1),
        end_date=date(2026, 7, 30),
        amount=Decimal("5400000.00"),
        vat_rate="22%",
        status="Планируется",
        contractor_name="ООО «Дорожник»",
        acceptance_place="Районы Карачаево-Черкесской Республики",
        delivery_terms="Восстановление асфальтобетонного покрытия дорог и тротуаров на территории районов КЧР.",
        acceptance_procedure="Коммерческое предложение действует до 30.07.2026. После согласования условий может быть оформлен договор или муниципальный контракт.",
        warranty_months=12,
        penalty_terms="Санкции определяются после заключения договора.",
        description="Предварительное коммерческое предложение на дорожные работы.",
        client_id=client_1.id,
        object_id=object_5.id
    )

    db.session.add_all([contract_1, contract_2, contract_3, contract_4, contract_5])
    db.session.commit()

    for contract in [contract_1, contract_2, contract_3, contract_4, contract_5]:
        add_log("Создание договора", f"Добавлен договор №{contract.number}.", user=admin, client=contract.client, contract=contract)

    print("Добавление заявок / обращений...")

    lead_1 = Lead(
        request_date=today - timedelta(days=6),
        source="Телефон",
        status="Расчет сметы",
        contact_person="Алботова Фатима Умаровна",
        phone="+7 928 398-37-57",
        email="a-gfatima@mail.ru",
        work_type="Ремонт и благоустройство территории",
        object_address="КЧР, Малокарачаевский район, село Первомайское",
        estimated_budget=Decimal("900000.00"),
        responsible_person="Менеджер по работе с клиентами",
        planned_contact_date=today + timedelta(days=1),
        comment="Клиент запросил предварительный расчет стоимости работ.",
        client_id=client_4.id,
        object_id=object_3.id
    )

    lead_2 = Lead(
        request_date=today - timedelta(days=3),
        source="Муниципальный запрос",
        status="Коммерческое предложение",
        contact_person="Представитель администрации Римгорского сельского поселения",
        phone="+7 (87877) 2-39-59",
        email="rimgorka@bk.ru",
        work_type="Восстановление асфальтобетонного покрытия",
        object_address="Районы Карачаево-Черкесской Республики",
        estimated_budget=Decimal("5400000.00"),
        responsible_person="Главный инженер",
        planned_contact_date=today + timedelta(days=2),
        comment="Подготовлено коммерческое предложение КП-24/04.",
        client_id=client_1.id,
        object_id=object_5.id,
        contract_id=contract_5.id
    )

    lead_3 = Lead(
        request_date=today,
        source="Email",
        status="Новая",
        contact_person="Семенов В.В.",
        phone="",
        email="info@arkhyz-original.ru",
        work_type="Проектно-сметная документация",
        object_address="г. Черкесск",
        estimated_budget=Decimal("1250000.00"),
        responsible_person="Инженер ПТО",
        planned_contact_date=today,
        comment="Необходимо уточнить исходные данные по объекту.",
        client_id=client_5.id,
        object_id=object_6.id,
        contract_id=contract_1.id
    )

    db.session.add_all([lead_1, lead_2, lead_3])
    db.session.commit()

    for lead in [lead_1, lead_2, lead_3]:
        add_log("Создание заявки", f"Создана заявка #{lead.id}: {lead.contact_person}.", user=admin, client=lead.client, contract=lead.contract, lead=lead)

    print("Добавление этапов работ...")

    stages = [
        WorkStage(
            stage_number=1,
            title="Подготовка к строительству",
            planned_start=date(2024, 7, 23),
            planned_end=date(2024, 8, 5),
            actual_start=date(2024, 7, 23),
            actual_end=date(2024, 8, 5),
            status="Завершен",
            comment="Выполнены подготовительные мероприятия.",
            contract_id=contract_3.id
        ),
        WorkStage(
            stage_number=2,
            title="Строительно-монтажные работы",
            planned_start=date(2024, 8, 6),
            planned_end=date(2024, 11, 25),
            actual_start=date(2024, 8, 6),
            actual_end=date(2024, 11, 25),
            status="Завершен",
            comment="Основной объем работ выполнен.",
            contract_id=contract_3.id
        ),
        WorkStage(
            stage_number=3,
            title="Оформление исполнительной документации",
            planned_start=date(2024, 11, 26),
            planned_end=date(2024, 12, 3),
            actual_start=date(2024, 11, 26),
            actual_end=date(2024, 12, 3),
            status="Завершен",
            comment="Оформлены КС-2 и КС-3.",
            contract_id=contract_3.id
        ),
    ]

    db.session.add_all(stages)

    print("Добавление платежей...")

    payments = [
        Payment(
            payment_date=date(2024, 12, 10),
            amount=Decimal("9748905.04"),
            payment_type="Безналичный расчет",
            status="Оплачено",
            purpose="Оплата по муниципальному контракту за выполненные работы",
            contract_id=contract_3.id
        ),
        Payment(
            payment_date=date(2024, 6, 15),
            amount=Decimal("680000.00"),
            payment_type="Безналичный расчет",
            status="Оплачено",
            purpose="Оплата поставки бетонной смеси",
            contract_id=contract_2.id
        ),
        Payment(
            payment_date=today - timedelta(days=7),
            amount=Decimal("750000.00"),
            payment_type="Окончательный расчет",
            status="Ожидается",
            purpose="Окончательный расчет после сдачи проектной документации",
            contract_id=contract_1.id
        ),
        Payment(
            payment_date=today + timedelta(days=12),
            amount=Decimal("2700000.00"),
            payment_type="Плановый платеж",
            status="Ожидается",
            purpose="Ожидаемая оплата по коммерческому предложению после заключения договора",
            contract_id=contract_5.id
        ),
    ]

    db.session.add_all(payments)

    print("Добавление актов выполненных работ...")

    act_1 = AcceptanceAct(
        act_number="2",
        act_date=date(2024, 12, 3),
        act_type="КС-3",
        work_name="Благоустройство села Учкекен в 2024 г.",
        amount=Decimal("8124087.53"),
        vat_amount=Decimal("1624817.51"),
        total_amount=Decimal("9748905.04"),
        acceptance_place="КЧР, село Учкекен",
        acceptance_status="Подписан",
        signed_by_customer="Глава Учкекенского сельского поселения",
        signed_by_contractor="Директор ООО «Дорожник»",
        comment="Справка о стоимости выполненных работ и затрат по форме КС-3.",
        contract_id=contract_3.id
    )

    act_2 = AcceptanceAct(
        act_number="КС-2/03-12",
        act_date=date(2024, 12, 3),
        act_type="КС-2",
        work_name="Акт о приемке выполненных работ по благоустройству села Учкекен",
        amount=Decimal("8124087.53"),
        vat_amount=Decimal("1624817.51"),
        total_amount=Decimal("9748905.04"),
        acceptance_place="КЧР, село Учкекен",
        acceptance_status="Подписан",
        signed_by_customer="Глава Учкекенского сельского поселения",
        signed_by_contractor="Директор ООО «Дорожник»",
        comment="Акт о приемке выполненных работ по форме КС-2.",
        contract_id=contract_3.id
    )

    act_3 = AcceptanceAct(
        act_number="ПР-02/10",
        act_date=today + timedelta(days=10),
        act_type="Акт сдачи-приемки",
        work_name="Передача проектно-сметной и рабочей документации",
        amount=Decimal("1041666.67"),
        vat_amount=Decimal("208333.33"),
        total_amount=Decimal("1250000.00"),
        acceptance_place="г. Черкесск",
        acceptance_status="На подписании",
        signed_by_customer="Представитель ООО «Архыз Оригинал»",
        signed_by_contractor="Директор ООО «Дорожник»",
        comment="Акт подготовлен для подписания после проверки документации.",
        contract_id=contract_1.id
    )

    db.session.add_all([act_1, act_2, act_3])
    db.session.commit()

    for act in [act_1, act_2, act_3]:
        add_log("Создание акта", f"Добавлен {act.act_type} №{act.act_number}.", user=admin, contract=act.contract)

    print("Добавление задач и напоминаний...")

    task_1 = Task(
        title="Связаться с клиентом по заявке на расчет сметы",
        description="Уточнить объем работ и направить предварительный расчет стоимости.",
        task_type="Звонок",
        priority="Высокий",
        status="В работе",
        due_date=today,
        responsible_person="Менеджер по работе с клиентами",
        client_id=client_4.id,
        lead_id=lead_1.id
    )

    task_2 = Task(
        title="Проверить поступление окончательного платежа",
        description="Платеж по договору №02/10 ожидается, срок уже прошел.",
        task_type="Оплата",
        priority="Срочный",
        status="В работе",
        due_date=today - timedelta(days=2),
        responsible_person="Бухгалтер",
        client_id=client_5.id,
        contract_id=contract_1.id
    )

    task_3 = Task(
        title="Передать акт ПР-02/10 на подпись заказчику",
        description="Подготовить комплект документов для сдачи-приемки проектных работ.",
        task_type="Документы",
        priority="Высокий",
        status="Новая",
        due_date=today + timedelta(days=3),
        responsible_person="Инженер ПТО",
        client_id=client_5.id,
        contract_id=contract_1.id
    )

    task_4 = Task(
        title="Подготовить договор по КП-24/04",
        description="После согласования коммерческого предложения оформить проект договора.",
        task_type="Документы",
        priority="Средний",
        status="Новая",
        due_date=today + timedelta(days=8),
        responsible_person="Юрист",
        client_id=client_1.id,
        contract_id=contract_5.id,
        lead_id=lead_2.id
    )

    db.session.add_all([task_1, task_2, task_3, task_4])
    db.session.commit()

    for task in [task_1, task_2, task_3, task_4]:
        add_log("Создание задачи", f"Создана задача #{task.id}: {task.title}.", user=admin, client=task.client, contract=task.contract, lead=task.lead, task=task)

    print("Добавление документов...")

    file_1_size = create_sample_document(
        "dogovor_02-10_podryad.txt",
        "Договор подряда № 02/10 на выполнение проектных работ."
    )

    file_2_size = create_sample_document(
        "dogovor_03-p-2024_postavka.txt",
        "Договор поставки бетонных смесей № 03-П/2024."
    )

    file_3_size = create_sample_document(
        "municipal_contract_0179300003924000003.txt",
        "Муниципальный контракт № 0179300003924000003 на благоустройство села Учкекен."
    )

    file_4_size = create_sample_document(
        "ks-2_03-12-2024.txt",
        "Акт о приемке выполненных работ КС-2 от 03.12.2024."
    )

    file_5_size = create_sample_document(
        "ks-3_03-12-2024.txt",
        "Справка о стоимости выполненных работ и затрат КС-3 от 03.12.2024."
    )

    file_6_size = create_sample_document(
        "kp_24-04_asfalt.txt",
        "Коммерческое предложение № 24/04 на восстановление асфальтобетонного покрытия."
    )

    documents = [
        Document(
            filename="dogovor_02-10_podryad.txt",
            original_filename="Договор 2-10 подряда проектных работ.pdf",
            document_type="Договор",
            file_extension="txt",
            file_size=file_1_size,
            extracted_text="Договор подряда № 02/10 на выполнение проектных работ.",
            contract_id=contract_1.id
        ),
        Document(
            filename="dogovor_03-p-2024_postavka.txt",
            original_filename="ДОГОВОР ПОСТАВКИ 23.05.2024.pdf",
            document_type="Договор",
            file_extension="txt",
            file_size=file_2_size,
            extracted_text="Договор поставки бетонных смесей № 03-П/2024.",
            contract_id=contract_2.id
        ),
        Document(
            filename="municipal_contract_0179300003924000003.txt",
            original_filename="Контракт от 23.07.2024.pdf",
            document_type="Договор",
            file_extension="txt",
            file_size=file_3_size,
            extracted_text="Муниципальный контракт на благоустройство села Учкекен.",
            contract_id=contract_3.id
        ),
        Document(
            filename="ks-2_03-12-2024.txt",
            original_filename="КС-2 расшир.на 9748905,04 от 03.12.2024.pdf",
            document_type="Акт КС-2",
            file_extension="txt",
            file_size=file_4_size,
            extracted_text="Акт о приемке выполненных работ КС-2 от 03.12.2024.",
            contract_id=contract_3.id
        ),
        Document(
            filename="ks-3_03-12-2024.txt",
            original_filename="КС-3 №2 от 03.12.2024.pdf",
            document_type="Справка КС-3",
            file_extension="txt",
            file_size=file_5_size,
            extracted_text="Справка о стоимости выполненных работ и затрат КС-3 от 03.12.2024.",
            contract_id=contract_3.id
        ),
        Document(
            filename="kp_24-04_asfalt.txt",
            original_filename="кп асфальт.pdf",
            document_type="Коммерческое предложение",
            file_extension="txt",
            file_size=file_6_size,
            extracted_text="Коммерческое предложение на восстановление асфальтобетонного покрытия.",
            contract_id=contract_5.id
        ),
    ]

    db.session.add_all(documents)
    db.session.commit()

    for document in documents:
        add_log("Загрузка документа", f"Добавлен документ «{document.original_filename}».", user=admin, contract=document.contract)

    db.session.commit()

    print("Готово!")
    print("База данных создана и заполнена демонстрационными данными.")
    print("Логин: admin")
    print("Пароль: admin123")
