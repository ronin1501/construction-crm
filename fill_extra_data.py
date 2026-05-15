from datetime import date
from decimal import Decimal

from app import create_app
from app.extensions import db
from app.models import Contract, AcceptanceAct


app = create_app()


def find_contract(numbers):
    for number in numbers:
        contract = Contract.query.filter_by(number=number).first()
        if contract:
            return contract
    return None


def add_or_update_act(
    contract,
    act_number,
    act_date,
    act_type,
    work_name,
    amount,
    vat_amount,
    total_amount,
    acceptance_place,
    acceptance_status,
    signed_by_customer,
    signed_by_contractor,
    comment
):
    act = AcceptanceAct.query.filter_by(
        contract_id=contract.id,
        act_number=act_number,
        act_type=act_type
    ).first()

    if not act:
        act = AcceptanceAct(
            contract_id=contract.id,
            act_number=act_number,
            act_type=act_type
        )
        db.session.add(act)

    act.act_date = act_date
    act.work_name = work_name
    act.amount = amount
    act.vat_amount = vat_amount
    act.total_amount = total_amount
    act.acceptance_place = acceptance_place
    act.acceptance_status = acceptance_status
    act.signed_by_customer = signed_by_customer
    act.signed_by_contractor = signed_by_contractor
    act.comment = comment

    return act


with app.app_context():
    print("Заполнение сроков, сдачи-приемки и актов...")

    # 1. Договор подряда проектных работ № 02/10
    contract_project = find_contract(["02/10"])

    if contract_project:
        contract_project.start_date = date(2025, 10, 29)
        contract_project.end_date = date(2026, 2, 28)
        contract_project.status = "Действующий"
        contract_project.contractor_name = "ООО «Дорожник»"
        contract_project.supplier_name = None
        contract_project.acceptance_place = "г. Черкесск, объект заказчика"
        contract_project.delivery_terms = (
            "Подрядчик выполняет проектно-сметную и рабочую документацию "
            "в соответствии с техническим заданием заказчика, исходными данными "
            "и условиями договора."
        )
        contract_project.acceptance_procedure = (
            "Результат работ передается заказчику комплектом проектной документации "
            "на бумажном носителе и в электронном виде. При отсутствии мотивированных "
            "замечаний документация считается принятой заказчиком."
        )
        contract_project.warranty_months = 12
        contract_project.penalty_terms = (
            "При нарушении сроков выполнения работ или ненадлежащем исполнении обязательств "
            "стороны несут ответственность согласно условиям договора и законодательству РФ."
        )

        add_or_update_act(
            contract=contract_project,
            act_number="ПР-02/10",
            act_date=date(2026, 2, 28),
            act_type="Акт сдачи-приемки",
            work_name="Передача проектно-сметной и рабочей документации",
            amount=Decimal("1041666.67"),
            vat_amount=Decimal("208333.33"),
            total_amount=Decimal("1250000.00"),
            acceptance_place="г. Черкесск",
            acceptance_status="На подписании",
            signed_by_customer="Представитель ООО «Архыз Оригинал»",
            signed_by_contractor="Директор ООО «Дорожник»",
            comment=(
                "Акт предназначен для оформления передачи результата проектных работ "
                "по договору № 02/10."
            )
        )

    # 2. Договор поставки бетонных смесей № 03-П/2024
    contract_supply = find_contract(["03-П/2024", "03-П/2024 "])

    if contract_supply:
        contract_supply.start_date = date(2024, 5, 23)
        contract_supply.end_date = date(2024, 12, 31)
        contract_supply.status = "Исполнен"
        contract_supply.contractor_name = "ООО «Дорожник»"
        contract_supply.supplier_name = "ООО «Барсуковская ПМК»"
        contract_supply.acceptance_place = "Объект покупателя"
        contract_supply.delivery_terms = (
            "Поставка бетонной смеси осуществляется транспортом поставщика. "
            "Товар передается покупателю в срок, определенный сторонами, "
            "либо иным документом, позволяющим идентифицировать дату передачи товара."
        )
        contract_supply.acceptance_procedure = (
            "Приемка товара производится полномочным представителем покупателя "
            "в присутствии представителя поставщика. Факт передачи подтверждается "
            "УПД, накладной или транспортной накладной."
        )
        contract_supply.warranty_months = 0
        contract_supply.penalty_terms = (
            "При просрочке оплаты товара поставщик вправе приостановить поставку. "
            "При необоснованном отказе от приемки покупатель несет расходы, "
            "связанные с простоем, доставкой и возвратом товара."
        )

        add_or_update_act(
            contract=contract_supply,
            act_number="УПД-03-П/2024",
            act_date=date(2024, 6, 8),
            act_type="Акт сдачи-приемки",
            work_name="Поставка бетонной смеси М200 В15",
            amount=Decimal("566666.67"),
            vat_amount=Decimal("113333.33"),
            total_amount=Decimal("680000.00"),
            acceptance_place="Объект покупателя",
            acceptance_status="Подписан",
            signed_by_customer="Директор ООО «Дорожник» Борлаков О.И.",
            signed_by_contractor="Генеральный директор ООО «Барсуковская ПМК» Рябченко А.А.",
            comment=(
                "Факт передачи товара подтверждается передаточным документом, "
                "накладной или УПД."
            )
        )

    # 3. Муниципальный контракт по благоустройству села Учкекен
    contract_municipal = find_contract([
        "0179300003924000003",
        "МК-23/07/2024",
        "МК-23/07/2024 "
    ])

    if contract_municipal:
        contract_municipal.start_date = date(2024, 7, 23)
        contract_municipal.end_date = date(2024, 12, 3)
        contract_municipal.status = "Исполнен"
        contract_municipal.contractor_name = "ООО «Дорожник»"
        contract_municipal.supplier_name = None
        contract_municipal.acceptance_place = "КЧР, село Учкекен"
        contract_municipal.delivery_terms = (
            "Подрядчик выполняет работы по благоустройству территории "
            "в соответствии с муниципальным контрактом, техническим заданием "
            "и сметной документацией."
        )
        contract_municipal.acceptance_procedure = (
            "Сдача результата выполненных работ оформляется актом КС-2 "
            "и справкой КС-3. Приемка производится заказчиком после проверки "
            "объема, качества и стоимости выполненных работ."
        )
        contract_municipal.warranty_months = 36
        contract_municipal.penalty_terms = (
            "За нарушение сроков выполнения работ, ненадлежащее качество "
            "или нарушение условий контракта применяются штрафы и неустойки."
        )

        add_or_update_act(
            contract=contract_municipal,
            act_number="КС-2/03-12-2024",
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
            comment="Акт о приемке выполненных работ по форме КС-2 от 03.12.2024."
        )

        add_or_update_act(
            contract=contract_municipal,
            act_number="2",
            act_date=date(2024, 12, 3),
            act_type="КС-3",
            work_name="Справка о стоимости выполненных работ и затрат",
            amount=Decimal("8124087.53"),
            vat_amount=Decimal("1624817.51"),
            total_amount=Decimal("9748905.04"),
            acceptance_place="КЧР, село Учкекен",
            acceptance_status="Подписан",
            signed_by_customer="Глава Учкекенского сельского поселения",
            signed_by_contractor="Директор ООО «Дорожник»",
            comment="Справка КС-3 №2 от 03.12.2024 на сумму 9 748 905,04 руб."
        )

    # 4. Договор по благоустройству Первомайского сельского поселения
    contract_first = find_contract(["БЛ-05/2024"])

    if contract_first:
        contract_first.start_date = date(2024, 5, 10)
        contract_first.end_date = date(2024, 9, 15)
        contract_first.status = "Исполнен"
        contract_first.contractor_name = "ООО «Дорожник»"
        contract_first.supplier_name = None
        contract_first.acceptance_place = "КЧР, село Первомайское"
        contract_first.delivery_terms = (
            "Выполнение комплекса работ по благоустройству территории "
            "между многоквартирными домами."
        )
        contract_first.acceptance_procedure = (
            "Работы передаются заказчику после фактического выполнения. "
            "Приемка оформляется актом выполненных работ."
        )
        contract_first.warranty_months = 24
        contract_first.penalty_terms = (
            "Санкции применяются при нарушении сроков выполнения работ "
            "или выявлении недостатков результата работ."
        )

        add_or_update_act(
            contract=contract_first,
            act_number="БЛ-05/2024-А1",
            act_date=date(2024, 9, 15),
            act_type="Акт выполненных работ",
            work_name="Благоустройство территории между МКД 81, 87, 89, 93",
            amount=Decimal("2875000.00"),
            vat_amount=Decimal("575000.00"),
            total_amount=Decimal("3450000.00"),
            acceptance_place="КЧР, село Первомайское",
            acceptance_status="Подписан",
            signed_by_customer="Глава администрации Первомайского сельского поселения",
            signed_by_contractor="Директор ООО «Дорожник»",
            comment="Акт выполненных работ по благоустройству территории."
        )

    # 5. Коммерческое предложение КП-24/04
    contract_kp = find_contract(["КП-24/04"])

    if contract_kp:
        contract_kp.start_date = date(2026, 5, 1)
        contract_kp.end_date = date(2026, 7, 30)
        contract_kp.status = "Планируется"
        contract_kp.contractor_name = "ООО «Дорожник»"
        contract_kp.supplier_name = None
        contract_kp.acceptance_place = "Районы Карачаево-Черкесской Республики"
        contract_kp.delivery_terms = (
            "Восстановление асфальтобетонного покрытия дорог и тротуаров "
            "на территории районов Карачаево-Черкесской Республики."
        )
        contract_kp.acceptance_procedure = (
            "Коммерческое предложение действует до 30.07.2026. "
            "После согласования условий может быть оформлен договор или муниципальный контракт."
        )
        contract_kp.warranty_months = 12
        contract_kp.penalty_terms = (
            "Санкции, порядок приемки и гарантийные обязательства будут уточнены "
            "после заключения основного договора."
        )

    db.session.commit()

    print("Готово!")
    print("Сроки, сдача-приемка и акты заполнены.")