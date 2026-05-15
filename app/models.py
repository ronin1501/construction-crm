from datetime import datetime
from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="user",
        lazy=True
    )


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)

    client_type = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    inn = db.Column(db.String(20))
    kpp = db.Column(db.String(20))
    ogrn = db.Column(db.String(20))

    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    address = db.Column(db.String(300))
    representative = db.Column(db.String(200))

    tags_text = db.Column(db.String(300))
    note = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    contracts = db.relationship(
        "Contract",
        back_populates="client",
        lazy=True
    )

    leads = db.relationship(
        "Lead",
        back_populates="client",
        lazy=True
    )

    tasks = db.relationship(
        "Task",
        back_populates="client",
        lazy=True
    )

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="client",
        lazy=True
    )


class ConstructionObject(db.Model):
    __tablename__ = "construction_objects"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(300))
    district = db.Column(db.String(150))
    work_type = db.Column(db.String(255))
    status = db.Column(db.String(100), default="В работе")

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    contracts = db.relationship(
        "Contract",
        back_populates="object",
        lazy=True
    )

    leads = db.relationship(
        "Lead",
        back_populates="object",
        lazy=True
    )


class Contract(db.Model):
    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True)

    number = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    contract_type = db.Column(db.String(150))

    contract_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    amount = db.Column(db.Numeric(14, 2))
    vat_rate = db.Column(db.String(20))

    status = db.Column(db.String(100), default="Действующий")

    contractor_name = db.Column(db.String(255), default="ООО «Дорожник»")
    supplier_name = db.Column(db.String(255))

    acceptance_place = db.Column(db.String(300))
    delivery_terms = db.Column(db.Text)
    acceptance_procedure = db.Column(db.Text)

    warranty_months = db.Column(db.Integer)
    penalty_terms = db.Column(db.Text)

    description = db.Column(db.Text)

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    object_id = db.Column(db.Integer, db.ForeignKey("construction_objects.id"))

    client = db.relationship(
        "Client",
        back_populates="contracts"
    )

    object = db.relationship(
        "ConstructionObject",
        back_populates="contracts"
    )

    documents = db.relationship(
        "Document",
        back_populates="contract",
        lazy=True,
        cascade="all, delete-orphan"
    )

    payments = db.relationship(
        "Payment",
        back_populates="contract",
        lazy=True,
        cascade="all, delete-orphan"
    )

    stages = db.relationship(
        "WorkStage",
        back_populates="contract",
        lazy=True,
        cascade="all, delete-orphan"
    )

    acts = db.relationship(
        "AcceptanceAct",
        back_populates="contract",
        lazy=True,
        cascade="all, delete-orphan"
    )

    tasks = db.relationship(
        "Task",
        back_populates="contract",
        lazy=True
    )

    leads = db.relationship(
        "Lead",
        back_populates="contract",
        lazy=True
    )

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="contract",
        lazy=True
    )


class WorkStage(db.Model):
    __tablename__ = "work_stages"

    id = db.Column(db.Integer, primary_key=True)

    stage_number = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)

    planned_start = db.Column(db.Date)
    planned_end = db.Column(db.Date)

    actual_start = db.Column(db.Date)
    actual_end = db.Column(db.Date)

    status = db.Column(db.String(100), default="Планируется")
    comment = db.Column(db.Text)

    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"), nullable=False)

    contract = db.relationship(
        "Contract",
        back_populates="stages"
    )


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    payment_date = db.Column(db.Date)
    amount = db.Column(db.Numeric(14, 2), nullable=False)

    payment_type = db.Column(db.String(100))
    status = db.Column(db.String(100), default="Ожидается")
    purpose = db.Column(db.String(255))

    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"), nullable=False)

    contract = db.relationship(
        "Contract",
        back_populates="payments"
    )


class AcceptanceAct(db.Model):
    __tablename__ = "acceptance_acts"

    id = db.Column(db.Integer, primary_key=True)

    act_number = db.Column(db.String(100), nullable=False)
    act_date = db.Column(db.Date)

    act_type = db.Column(db.String(100), default="Акт выполненных работ")
    work_name = db.Column(db.String(255))

    amount = db.Column(db.Numeric(14, 2))
    vat_amount = db.Column(db.Numeric(14, 2))
    total_amount = db.Column(db.Numeric(14, 2))

    acceptance_place = db.Column(db.String(300))
    acceptance_status = db.Column(db.String(100), default="Подготовлен")

    signed_by_customer = db.Column(db.String(200))
    signed_by_contractor = db.Column(db.String(200))

    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"), nullable=False)

    contract = db.relationship(
        "Contract",
        back_populates="acts"
    )


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    document_type = db.Column(db.String(100))

    file_extension = db.Column(db.String(20))
    file_size = db.Column(db.Integer)

    extracted_text = db.Column(db.Text)

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"), nullable=False)

    contract = db.relationship(
        "Contract",
        back_populates="documents"
    )


class Lead(db.Model):
    """
    Заявка / обращение клиента.
    Используется для фиксации первичного контакта до заключения договора.
    """

    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    lead_date = db.Column(db.Date, nullable=False)

    source = db.Column(db.String(100), default="Сайт")
    status = db.Column(db.String(100), default="Новая")
    priority = db.Column(db.String(50), default="Обычная")

    contact_person = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))

    work_type = db.Column(db.String(255))
    object_address = db.Column(db.String(300))
    estimated_budget = db.Column(db.Numeric(14, 2))

    responsible = db.Column(db.String(150), default="Менеджер")
    comment = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    object_id = db.Column(db.Integer, db.ForeignKey("construction_objects.id"))
    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"))

    client = db.relationship(
        "Client",
        back_populates="leads"
    )

    object = db.relationship(
        "ConstructionObject",
        back_populates="leads"
    )

    contract = db.relationship(
        "Contract",
        back_populates="leads"
    )

    tasks = db.relationship(
        "Task",
        back_populates="lead",
        lazy=True
    )

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="lead",
        lazy=True
    )


class Task(db.Model):
    """
    Задача / напоминание по клиенту, договору или заявке.
    """

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    task_type = db.Column(db.String(100), default="Задача")
    priority = db.Column(db.String(50), default="Обычная")
    status = db.Column(db.String(100), default="Новая")

    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    responsible = db.Column(db.String(200), default="Менеджер")

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"))
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"))

    client = db.relationship(
        "Client",
        back_populates="tasks"
    )

    contract = db.relationship(
        "Contract",
        back_populates="tasks"
    )

    lead = db.relationship(
        "Lead",
        back_populates="tasks"
    )

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="task",
        lazy=True
    )


class ActivityLog(db.Model):
    """
    Журнал действий пользователя в системе.
    """

    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    action_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"))
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))

    user = db.relationship(
        "User",
        back_populates="activity_logs"
    )

    client = db.relationship(
        "Client",
        back_populates="activity_logs"
    )

    contract = db.relationship(
        "Contract",
        back_populates="activity_logs"
    )

    lead = db.relationship(
        "Lead",
        back_populates="activity_logs"
    )

    task = db.relationship(
        "Task",
        back_populates="activity_logs"
    )