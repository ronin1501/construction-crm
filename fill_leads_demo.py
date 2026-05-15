from datetime import date
from decimal import Decimal

from app import create_app
from app.extensions import db
from app.models import Client, ConstructionObject, Lead


app = create_app()


with app.app_context():
    db.create_all()

    if Lead.query.count() > 0:
        print("Заявки уже есть. Повторное заполнение не выполнено.")
        raise SystemExit

    client_1 = Client.query.filter(Client.name.ilike("%Римгорского%")).first()
    client_2 = Client.query.filter(Client.name.ilike("%Первомайского%")).first()
    client_3 = Client.query.filter(Client.name.ilike("%Учкекенского%")).first()
    client_4 = Client.query.filter(Client.name.ilike("%Алботова%")).first()
    client_5 = Client.query.filter(Client.name.ilike("%Архыз%")).first()

    object_1 = ConstructionObject.query.filter(ConstructionObject.name.ilike("%асфальтобетонного%")).first()
    object_2 = ConstructionObject.query.filter(ConstructionObject.name.ilike("%Учкекен%")).first()
    object_3 = ConstructionObject.query.filter(ConstructionObject.name.ilike("%Первомайское%")).first()

    leads = [
        Lead(
            title="Расчет стоимости восстановления асфальтобетонного покрытия",
            lead_date=date(2026, 4, 20),
            source="Муниципальный заказ",
            status="Коммерческое предложение",
            priority="Высокая",
            client_id=client_1.id if client_1 else None,
            object_id=object_1.id if object_1 else None,
            contact_person="Узденов Таулан Анзорович",
            phone="+7 (87877) 2-39-59",
            email="rimgorka@bk.ru",
            work_type="Дорожные работы",
            object_address="Районы Карачаево-Черкесской Республики",
            estimated_budget=Decimal("5400000.00"),
            responsible="Менеджер договорного отдела",
            comment="Необходимо подготовить коммерческое предложение и предварительный расчет стоимости работ."
        ),
        Lead(
            title="Обращение по благоустройству территории в селе Учкекен",
            lead_date=date(2024, 7, 10),
            source="Телефон",
            status="Договор",
            priority="Высокая",
            client_id=client_3.id if client_3 else None,
            object_id=object_2.id if object_2 else None,
            contact_person="Семенов Анзор Хаджи-Магомедович",
            phone="+7 (87877) 2-81-61",
            email="uchkeken-sp.ucoz.com",
            work_type="Благоустройство территории",
            object_address="КЧР, село Учкекен",
            estimated_budget=Decimal("9748905.04"),
            responsible="Специалист по муниципальным контрактам",
            comment="Заявка перешла в муниципальный контракт. Требуется контроль сроков и документов КС-2/КС-3."
        ),
        Lead(
            title="Запрос на ремонт дворовой территории",
            lead_date=date(2024, 5, 2),
            source="Личное обращение",
            status="Закрыта",
            priority="Обычная",
            client_id=client_2.id if client_2 else None,
            object_id=object_3.id if object_3 else None,
            contact_person="Байрамкулов Альберт Сагитович",
            phone="8 (87877) 2-38-37",
            email="pervomaiskoe.sel.pos@yandex.ru",
            work_type="Ремонт и благоустройство дворовой территории",
            object_address="КЧР, село Первомайское",
            estimated_budget=Decimal("3450000.00"),
            responsible="Менеджер по работе с заказчиками",
            comment="Работы выполнены, акт подписан, оплата получена."
        ),
        Lead(
            title="Частное обращение на ремонтные работы",
            lead_date=date(2026, 3, 14),
            source="Рекомендация",
            status="В обработке",
            priority="Обычная",
            client_id=client_4.id if client_4 else None,
            object_id=None,
            contact_person="Алботова Фатима Умаровна",
            phone="+7 928 398-37-57",
            email="a-gfatima@mail.ru",
            work_type="Ремонтные строительные работы",
            object_address="КЧР, Малокарачаевский район, село Первомайское",
            estimated_budget=Decimal("850000.00"),
            responsible="Менеджер",
            comment="Нужно уточнить объем работ и подготовить предварительную смету."
        ),
        Lead(
            title="Запрос на проектную документацию",
            lead_date=date(2025, 10, 15),
            source="Email",
            status="Договор",
            priority="Срочная",
            client_id=client_5.id if client_5 else None,
            object_id=None,
            contact_person="Семенов В.В.",
            phone="",
            email="",
            work_type="Проектно-сметная документация",
            object_address="г. Черкесск",
            estimated_budget=Decimal("1250000.00"),
            responsible="Проектный отдел",
            comment="По обращению оформлен договор подряда №02/10."
        ),
    ]

    db.session.add_all(leads)
    db.session.commit()

    print("Готово! Демонстрационные заявки добавлены.")