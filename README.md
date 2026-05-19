# АИС учета клиентов строительной компании

Тема ВКР: Разработка автоматизированной информационной системы для учета клиентов в строительной компании.

## Стек технологий

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Jinja2
- HTML
- CSS
- Bootstrap

## Запуск проекта

1. Создать базу данных PostgreSQL:

```sql
CREATE DATABASE construction_crm;
```

## Структура проекта

```text
construction_crm/
├── app/
│   ├── __init__.py                  # создание и настройка Flask-приложения
│   ├── extensions.py                # подключение расширений Flask
│   ├── forms.py                     # WTForms-формы
│   ├── models.py                    # SQLAlchemy-модели базы данных
│   ├── routes.py                    # маршруты и основная логика страниц
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            # основные стили интерфейса
│   │   ├── js/
│   │   │   └── main.js              # клиентские скрипты
│   │   └── uploads/
│   │       └── documents/
│   │           └── .gitkeep         # папка для загружаемых документов
│   └── templates/
│       ├── base.html                # базовый шаблон
│       ├── index.html               # главная страница
│       ├── login.html               # страница входа
│       ├── activity/
│       │   └── activity_list.html   # журнал активности
│       ├── acts/
│       │   └── acts_list.html       # список актов
│       ├── clients/
│       │   ├── client_add.html
│       │   ├── client_detail.html
│       │   ├── client_edit.html
│       │   ├── client_form.html
│       │   └── clients_list.html
│       ├── contracts/
│       │   ├── contract_add.html
│       │   ├── contract_detail.html
│       │   ├── contract_edit.html
│       │   ├── contract_form.html
│       │   └── contracts_list.html
│       ├── documents/
│       │   └── documents_list.html  # список документов
│       ├── leads/
│       │   ├── lead_add.html
│       │   ├── lead_detail.html
│       │   ├── lead_edit.html
│       │   ├── lead_form.html
│       │   └── leads_list.html
│       ├── objects/
│       │   ├── object_add.html
│       │   ├── object_detail.html
│       │   ├── object_edit.html
│       │   ├── object_form.html
│       │   └── objects_list.html
│       ├── payments/
│       │   └── payments_list.html   # список платежей
│       ├── reports/
│       │   └── reports.html         # отчеты
│       └── tasks/
│           ├── task_add.html
│           ├── task_edit.html
│           ├── task_form.html
│           └── tasks_list.html
├── migrations/                      # папка для миграций Flask-Migrate
├── app.py                           # точка входа приложения
├── start_site.py                    # запуск сайта двойным щелчком
├── config.py                        # настройки проекта
├── requirements.txt                 # зависимости Python
├── seed_db.py                       # заполнение базы тестовыми данными
├── update_demo_data.py              # обновление демонстрационных данных
├── fill_extra_data.py               # добавление дополнительных данных
├── fill_leads_demo.py               # добавление демонстрационных лидов
├── fill_contract_documents.py       # добавление демонстрационных документов
├── .gitignore                       # исключения Git
└── README.md                        # описание проекта
```

Служебные и локальные файлы не входят в основную структуру проекта: `.env`, `.venv/`, `.history/`, `.vscode/`, `__pycache__/`, `instance/`, а также реальные файлы, загруженные в `app/static/uploads/documents/`.
