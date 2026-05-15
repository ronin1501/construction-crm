from datetime import date
from decimal import Decimal

from app import create_app
from app.extensions import db
from app.models import Contract, AcceptanceAct


app = create_app()


with app.app_context():
    contract = Contract.query.filter_by(number="03-П/2024").first()

    if contract:
        contract.contract_type = "Договор поставки"
        contract.contractor_name = "ООО «Дорожник»"
        contract.supplier_name = "ООО «Барсуковская ПМК»"
        contract.start_date = date(2024, 5, 23)
        contract.end_date = date(2024, 12, 31)
        contract.vat_rate = "20%"
        contract.acceptance_place = "Объект покупателя"
        contract.delivery_terms = (
            "Доставка товара осуществляется транспортом Поставщика. "
            "Товар передается Покупателю в срок, определенный сторонами."
        )
        contract.acceptance_procedure = (
            "Приемка товара производится полномочным представителем Покупателя "
            "в присутствии представителя Поставщика. Факт передачи подтверждается "
            "накладной, УПД или иным передаточным документом."
        )
        contract.penalty_terms = (
            "При просрочке оплаты может начисляться неустойка. "
            "При необоснованном отказе от приемки Покупатель несет расходы, "
            "связанные с простоем, доставкой и возвратом."
        )

    municipal_contract = Contract.query.filter_by(number="МК-23/07/2024").first()

    if municipal_contract:
        municipal_contract.contract_type = "Муниципальный контракт"
        municipal_contract.contractor_name = "ООО «Дорожник»"
        municipal_contract.start_date = date(2024, 7, 23)
        municipal_contract.end_date = date(2024, 12, 3)
        municipal_contract.vat_rate = "20%"
        municipal_contract.acceptance_place = "село Учкекен, Малокарачаевский район"
        municipal_contract.acceptance_procedure = (
            "Приемка результата выполненных работ осуществляется Заказчиком. "
            "Результат оформляется актом выполненных работ и справкой о стоимости "
            "выполненных работ и затрат."
        )
        municipal_contract.warranty_months = 36
        municipal_contract.penalty_terms = (
            "За нарушение сроков исполнения обязательств предусмотрены штрафы "
            "и неустойки согласно условиям контракта."
        )

        existing_act = AcceptanceAct.query.filter_by(
            contract_id=municipal_contract.id,
            act_number="2"
        ).first()

        if not existing_act:
            act = AcceptanceAct(
                act_number="2",
                act_date=date(2024, 12, 3),
                act_type="КС-3",
                work_name="Благоустройство села Учкекен в 2024 г.",
                amount=Decimal("8124087.53"),
                vat_amount=Decimal("1624817.51"),
                total_amount=Decimal("9748905.04"),
                acceptance_place="село Учкекен, Малокарачаевский район",
                acceptance_status="Подписан",
                signed_by_customer="Глава Учкекенского сельского поселения",
                signed_by_contractor="Директор ООО «Дорожник»",
                comment="Справка о стоимости выполненных работ и затрат по форме КС-3.",
                contract_id=municipal_contract.id
            )
            db.session.add(act)

    project_contract = Contract.query.filter_by(number="02/10").first()

    if project_contract:
        project_contract.contract_type = "Договор подряда"
        project_contract.contractor_name = "ООО «Дорожник»"
        project_contract.start_date = date(2025, 10, 29)
        project_contract.end_date = date(2026, 2, 28)
        project_contract.vat_rate = "20%"
        project_contract.acceptance_place = "г. Черкесск"
        project_contract.delivery_terms = (
            "Подрядчик выполняет проектно-сметную и рабочую документацию "
            "по техническому заданию заказчика."
        )
        project_contract.acceptance_procedure = (
            "Результат работ передается заказчику комплектом документации "
            "на бумажном носителе и в электронном виде."
        )
        project_contract.penalty_terms = (
            "Ответственность сторон определяется условиями договора и действующим "
            "законодательством Российской Федерации."
        )

    commercial_offer = Contract.query.filter_by(number="КП-24/04").first()

    if commercial_offer:
        commercial_offer.contract_type = "Коммерческое предложение"
        commercial_offer.contractor_name = "ООО «Дорожник»"
        commercial_offer.start_date = date(2026, 5, 1)
        commercial_offer.end_date = date(2026, 7, 30)
        commercial_offer.vat_rate = "22%"
        commercial_offer.acceptance_place = "Районы Карачаево-Черкесской Республики"
        commercial_offer.delivery_terms = (
            "Восстановление асфальтобетонного покрытия дорог и тротуаров "
            "на территории районов КЧР."
        )
        commercial_offer.acceptance_procedure = (
            "Коммерческое предложение действует до 30.07.2026. "
            "После согласования условий может быть оформлен договор или контракт."
        )

    db.session.commit()

    print("Демонстрационные данные обновлены.")