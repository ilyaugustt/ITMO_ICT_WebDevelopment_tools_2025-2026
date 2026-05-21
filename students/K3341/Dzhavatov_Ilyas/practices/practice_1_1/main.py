import fastapi
from typing import Optional
from datetime import date, datetime
from models import (
    User, UserCreate, UserUpdate,
    Category, CategoryCreate, CategoryUpdate,
    Transaction, TransactionCreate, TransactionUpdate,
    Budget, BudgetCreate, BudgetUpdate,
    Goal, GoalCreate, GoalUpdate,
    Notification, NotificationCreate,
    Profession, ProfessionCreate, ProfessionUpdate,
)


app = fastapi.FastAPI(title="Finance Manager API", version="1.0.0")


# =============================================================================
# Вложенная temp_bd: пользователи с вложенными сущностями
# =============================================================================

temp_bd = {
    1: {
        "id": 1,
        "username": "ilyas_dzhavatov",
        "email": "ilyas@example.com",
        "currency": "RUB",
        "created_at": datetime(2025, 1, 15, 10, 30, 0),
        "updated_at": datetime(2025, 5, 10, 14, 0, 0),
        "categories": [
            {
                "id": 1,
                "name": "Зарплата",
                "type": "income",
                "user_id": 1,
                "icon": "💰",
                "created_at": datetime(2025, 1, 15, 10, 30, 0),
            },
            {
                "id": 2,
                "name": "Фриланс",
                "type": "income",
                "user_id": 1,
                "icon": "💻",
                "created_at": datetime(2025, 2, 1, 12, 0, 0),
            },
            {
                "id": 3,
                "name": "Продукты",
                "type": "expense",
                "user_id": 1,
                "icon": "🛒",
                "created_at": datetime(2025, 1, 15, 10, 30, 0),
            },
            {
                "id": 4,
                "name": "Транспорт",
                "type": "expense",
                "user_id": 1,
                "icon": "🚗",
                "created_at": datetime(2025, 1, 15, 10, 30, 0),
            },
            {
                "id": 5,
                "name": "Развлечения",
                "type": "expense",
                "user_id": 1,
                "icon": "🎮",
                "created_at": datetime(2025, 3, 1, 9, 0, 0),
            },
        ],
        "transactions": [
            {
                "id": 1,
                "amount": 150000.0,
                "type": "income",
                "category_id": 1,
                "user_id": 1,
                "date": date(2025, 5, 1),
                "description": "Зарплата за апрель",
                "created_at": datetime(2025, 5, 1, 10, 0, 0),
            },
            {
                "id": 2,
                "amount": 50000.0,
                "type": "income",
                "category_id": 2,
                "user_id": 1,
                "date": date(2025, 5, 10),
                "description": "Фриланс проект",
                "created_at": datetime(2025, 5, 10, 15, 0, 0),
            },
            {
                "id": 3,
                "amount": 15000.0,
                "type": "expense",
                "category_id": 3,
                "user_id": 1,
                "date": date(2025, 5, 5),
                "description": "Продукты на неделю",
                "created_at": datetime(2025, 5, 5, 18, 0, 0),
            },
            {
                "id": 4,
                "amount": 3000.0,
                "type": "expense",
                "category_id": 4,
                "user_id": 1,
                "date": date(2025, 5, 7),
                "description": "Бензин",
                "created_at": datetime(2025, 5, 7, 12, 0, 0),
            },
            {
                "id": 5,
                "amount": 5000.0,
                "type": "expense",
                "category_id": 5,
                "user_id": 1,
                "date": date(2025, 5, 12),
                "description": "Кино и игры",
                "created_at": datetime(2025, 5, 12, 20, 0, 0),
            },
            {
                "id": 6,
                "amount": 20000.0,
                "type": "expense",
                "category_id": 3,
                "user_id": 1,
                "date": date(2025, 5, 15),
                "description": "Продукты на месяц",
                "created_at": datetime(2025, 5, 15, 17, 0, 0),
            },
        ],
        "budgets": [
            {
                "id": 1,
                "amount": 30000.0,
                "period": "monthly",
                "category_id": 3,
                "user_id": 1,
                "start_date": date(2025, 5, 1),
                "end_date": date(2025, 5, 31),
                "created_at": datetime(2025, 5, 1, 9, 0, 0),
            },
            {
                "id": 2,
                "amount": 5000.0,
                "period": "monthly",
                "category_id": 4,
                "user_id": 1,
                "start_date": date(2025, 5, 1),
                "end_date": date(2025, 5, 31),
                "created_at": datetime(2025, 5, 1, 9, 0, 0),
            },
            {
                "id": 3,
                "amount": 10000.0,
                "period": "monthly",
                "category_id": 5,
                "user_id": 1,
                "start_date": date(2025, 5, 1),
                "end_date": date(2025, 5, 31),
                "created_at": datetime(2025, 5, 1, 9, 0, 0),
            },
        ],
        "goals": [
            {
                "id": 1,
                "name": "Купить машину",
                "target_amount": 1000000.0,
                "current_amount": 150000.0,
                "user_id": 1,
                "deadline": date(2026, 12, 31),
                "type": "savings",
                "created_at": datetime(2025, 1, 1, 0, 0, 0),
            },
            {
                "id": 2,
                "name": "Накопить на отпуск",
                "target_amount": 200000.0,
                "current_amount": 75000.0,
                "user_id": 1,
                "deadline": date(2025, 8, 1),
                "type": "savings",
                "created_at": datetime(2025, 3, 1, 0, 0, 0),
            },
            {
                "id": 3,
                "name": "Сократить траты на еду",
                "target_amount": 25000.0,
                "current_amount": 35000.0,
                "user_id": 1,
                "deadline": date(2025, 6, 30),
                "type": "reduction",
                "created_at": datetime(2025, 4, 1, 0, 0, 0),
            },
        ],
        "notifications": [
            {
                "id": 1,
                "user_id": 1,
                "message": "Вы потратили 80% бюджета на продукты",
                "type": "budget_exceeded",
                "is_read": True,
                "created_at": datetime(2025, 5, 10, 12, 0, 0),
            },
            {
                "id": 2,
                "user_id": 1,
                "message": "Поздравляем! Вы накопили на отпуск — 37.5%",
                "type": "goal_reached",
                "is_read": False,
                "created_at": datetime(2025, 5, 15, 10, 0, 0),
            },
        ],
        "professions": [
            {
                "id": 1,
                "title": "Backend Developer",
                "description": "Разработчик серверной части веб-приложений",
                "created_at": datetime(2025, 1, 1, 0, 0, 0),
            },
            {
                "id": 2,
                "title": "Frontend Developer",
                "description": "Разработчик клиентской части веб-приложений",
                "created_at": datetime(2025, 1, 1, 0, 0, 0),
            },
            {
                "id": 3,
                "title": "DevOps Engineer",
                "description": "Инженер по эксплуатации и автоматизации",
                "created_at": datetime(2025, 1, 1, 0, 0, 0),
            },
        ],
    },
    2: {
        "id": 2,
        "username": "maria_ivanova",
        "email": "maria@example.com",
        "currency": "RUB",
        "created_at": datetime(2025, 2, 20, 8, 0, 0),
        "updated_at": datetime(2025, 5, 18, 16, 30, 0),
        "categories": [
            {
                "id": 6,
                "name": "Зарплата",
                "type": "income",
                "user_id": 2,
                "icon": "💰",
                "created_at": datetime(2025, 2, 20, 8, 0, 0),
            },
            {
                "id": 7,
                "name": "Еда вне дома",
                "type": "expense",
                "user_id": 2,
                "icon": "🍽️",
                "created_at": datetime(2025, 2, 20, 8, 0, 0),
            },
            {
                "id": 8,
                "name": "Здоровье",
                "type": "expense",
                "user_id": 2,
                "icon": "🏥",
                "created_at": datetime(2025, 2, 20, 8, 0, 0),
            },
        ],
        "transactions": [
            {
                "id": 7,
                "amount": 80000.0,
                "type": "income",
                "category_id": 6,
                "user_id": 2,
                "date": date(2025, 5, 1),
                "description": "Зарплата",
                "created_at": datetime(2025, 5, 1, 10, 0, 0),
            },
            {
                "id": 8,
                "amount": 5000.0,
                "type": "expense",
                "category_id": 7,
                "user_id": 2,
                "date": date(2025, 5, 8),
                "description": "Ресторан",
                "created_at": datetime(2025, 5, 8, 21, 0, 0),
            },
            {
                "id": 9,
                "amount": 3000.0,
                "type": "expense",
                "category_id": 8,
                "user_id": 2,
                "date": date(2025, 5, 14),
                "description": "Аптека",
                "created_at": datetime(2025, 5, 14, 14, 0, 0),
            },
        ],
        "budgets": [
            {
                "id": 4,
                "amount": 15000.0,
                "period": "monthly",
                "category_id": 7,
                "user_id": 2,
                "start_date": date(2025, 5, 1),
                "end_date": date(2025, 5, 31),
                "created_at": datetime(2025, 5, 1, 9, 0, 0),
            },
        ],
        "goals": [
            {
                "id": 4,
                "name": "Подушка безопасности",
                "target_amount": 500000.0,
                "current_amount": 120000.0,
                "user_id": 2,
                "deadline": date(2026, 6, 30),
                "type": "savings",
                "created_at": datetime(2025, 2, 20, 8, 0, 0),
            },
        ],
        "notifications": [
            {
                "id": 3,
                "user_id": 2,
                "message": "Бюджет на еду превышен на 10%",
                "type": "budget_exceeded",
                "is_read": False,
                "created_at": datetime(2025, 5, 16, 18, 0, 0),
            },
        ],
        "professions": [
            {
                "id": 4,
                "title": "Data Scientist",
                "description": "Аналитик данных и машинное обучение",
                "created_at": datetime(2025, 2, 20, 8, 0, 0),
            },
        ],
    },
}

# Глобальные счётчики для ID
next_transaction_id = 10
next_category_id = 9
next_budget_id = 5
next_goal_id = 5
next_notification_id = 4
next_profession_id = 5


# =============================================================================
# Вспомогательные функции
# =============================================================================

def get_user(user_id: int) -> Optional[dict]:
    """Получить пользователя по ID."""
    return temp_bd.get(user_id)


def find_transaction(user_id: int, transaction_id: int) -> Optional[dict]:
    """Найти транзакцию у пользователя по ID."""
    user = get_user(user_id)
    if not user:
        return None
    for t in user.get("transactions", []):
        if t["id"] == transaction_id:
            return t
    return None


def find_category(user_id: int, category_id: int) -> Optional[dict]:
    """Найти категорию у пользователя по ID."""
    user = get_user(user_id)
    if not user:
        return None
    for c in user.get("categories", []):
        if c["id"] == category_id:
            return c
    return None


def find_budget(user_id: int, budget_id: int) -> Optional[dict]:
    """Найти бюджет у пользователя по ID."""
    user = get_user(user_id)
    if not user:
        return None
    for b in user.get("budgets", []):
        if b["id"] == budget_id:
            return b
    return None


def find_goal(user_id: int, goal_id: int) -> Optional[dict]:
    """Найти цель у пользователя по ID."""
    user = get_user(user_id)
    if not user:
        return None
    for g in user.get("goals", []):
        if g["id"] == goal_id:
            return g
    return None


def find_profession(user_id: int, profession_id: int) -> Optional[dict]:
    """Найти профессию у пользователя по ID."""
    user = get_user(user_id)
    if not user:
        return None
    for p in user.get("professions", []):
        if p["id"] == profession_id:
            return p
    return None


# =============================================================================
# Пользователи — CRUD
# =============================================================================

@app.get("/users", response_model=list[dict], tags=["Users"])
def list_users():
    """Получить список всех пользователей."""
    return list(temp_bd.values())


@app.get("/users/{user_id}", response_model=dict, tags=["Users"])
def get_user_by_id(user_id: int):
    """Получить пользователя по ID."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@app.post("/users", response_model=dict, status_code=201, tags=["Users"])
def create_user(user_data: UserCreate):
    """Создать нового пользователя."""
    user_id = len(temp_bd) + 1
    now = datetime.now()
    new_user = {
        "id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "currency": user_data.currency,
        "created_at": now,
        "updated_at": now,
        "categories": [],
        "transactions": [],
        "budgets": [],
        "goals": [],
        "notifications": [],
    }
    temp_bd[user_id] = new_user
    return new_user


@app.put("/users/{user_id}", response_model=dict, tags=["Users"])
def update_user(user_id: int, user_data: UserUpdate):
    """Обновить данные пользователя."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    if user_data.username is not None:
        user["username"] = user_data.username
    if user_data.email is not None:
        user["email"] = user_data.email
    if user_data.currency is not None:
        user["currency"] = user_data.currency
    user["updated_at"] = datetime.now()
    return user


@app.delete("/users/{user_id}", status_code=204, tags=["Users"])
def delete_user(user_id: int):
    """Удалить пользователя."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    del temp_bd[user_id]
    return None


# =============================================================================
# Категории — CRUD
# =============================================================================

@app.get("/users/{user_id}/categories", response_model=list[dict], tags=["Categories"])
def list_categories(user_id: int):
    """Получить список категорий пользователя."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    return user.get("categories", [])


@app.get("/users/{user_id}/categories/{category_id}", response_model=dict, tags=["Categories"])
def get_category(user_id: int, category_id: int):
    """Получить категорию по ID."""
    category = find_category(user_id, category_id)
    if not category:
        raise fastapi.HTTPException(status_code=404, detail="Категория не найдена")
    return category


@app.post("/users/{user_id}/categories", response_model=dict, status_code=201, tags=["Categories"])
def create_category(user_id: int, category_data: CategoryCreate):
    """Создать новую категорию."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    global next_category_id
    new_category = {
        "id": next_category_id,
        "name": category_data.name,
        "type": category_data.type,
        "user_id": user_id,
        "icon": "📁",
        "created_at": datetime.now(),
    }
    next_category_id += 1
    user["categories"].append(new_category)
    return new_category


@app.put("/users/{user_id}/categories/{category_id}", response_model=dict, tags=["Categories"])
def update_category(user_id: int, category_id: int, category_data: CategoryUpdate):
    """Обновить категорию."""
    category = find_category(user_id, category_id)
    if not category:
        raise fastapi.HTTPException(status_code=404, detail="Категория не найдена")
    if category_data.name is not None:
        category["name"] = category_data.name
    if category_data.type is not None:
        category["type"] = category_data.type
    return category


@app.delete("/users/{user_id}/categories/{category_id}", status_code=204, tags=["Categories"])
def delete_category(user_id: int, category_id: int):
    """Удалить категорию."""
    category = find_category(user_id, category_id)
    if not category:
        raise fastapi.HTTPException(status_code=404, detail="Категория не найдена")
    user = get_user(user_id)
    user["categories"] = [c for c in user["categories"] if c["id"] != category_id]
    return None


# =============================================================================
# Транзакции — CRUD
# =============================================================================

@app.get("/users/{user_id}/transactions", response_model=list[dict], tags=["Transactions"])
def list_transactions(user_id: int, category_id: Optional[int] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):
    """Получить список транзакций пользователя с фильтрацией."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    transactions = user.get("transactions", [])
    if category_id is not None:
        transactions = [t for t in transactions if t["category_id"] == category_id]
    if start_date is not None:
        transactions = [t for t in transactions if t["date"] >= start_date]
    if end_date is not None:
        transactions = [t for t in transactions if t["date"] <= end_date]
    return transactions


@app.get("/users/{user_id}/transactions/{transaction_id}", response_model=dict, tags=["Transactions"])
def get_transaction(user_id: int, transaction_id: int):
    """Получить транзакцию по ID."""
    transaction = find_transaction(user_id, transaction_id)
    if not transaction:
        raise fastapi.HTTPException(status_code=404, detail="Транзакция не найдена")
    return transaction


@app.post("/users/{user_id}/transactions", response_model=dict, status_code=201, tags=["Transactions"])
def create_transaction(user_id: int, transaction_data: TransactionCreate):
    """Создать новую транзакцию."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    # Проверка существования категории
    cat = find_category(user_id, transaction_data.category_id)
    if not cat:
        raise fastapi.HTTPException(status_code=404, detail="Категория не найдена")
    global next_transaction_id
    new_transaction = {
        "id": next_transaction_id,
        "amount": transaction_data.amount,
        "type": transaction_data.type,
        "category_id": transaction_data.category_id,
        "user_id": user_id,
        "date": transaction_data.date,
        "description": transaction_data.description,
        "created_at": datetime.now(),
    }
    next_transaction_id += 1
    user["transactions"].append(new_transaction)
    return new_transaction


@app.put("/users/{user_id}/transactions/{transaction_id}", response_model=dict, tags=["Transactions"])
def update_transaction(user_id: int, transaction_id: int, transaction_data: TransactionUpdate):
    """Обновить транзакцию."""
    transaction = find_transaction(user_id, transaction_id)
    if not transaction:
        raise fastapi.HTTPException(status_code=404, detail="Транзакция не найдена")
    if transaction_data.amount is not None:
        transaction["amount"] = transaction_data.amount
    if transaction_data.type is not None:
        transaction["type"] = transaction_data.type
    if transaction_data.category_id is not None:
        transaction["category_id"] = transaction_data.category_id
    if transaction_data.date is not None:
        transaction["date"] = transaction_data.date
    if transaction_data.description is not None:
        transaction["description"] = transaction_data.description
    return transaction


@app.delete("/users/{user_id}/transactions/{transaction_id}", status_code=204, tags=["Transactions"])
def delete_transaction(user_id: int, transaction_id: int):
    """Удалить транзакцию."""
    transaction = find_transaction(user_id, transaction_id)
    if not transaction:
        raise fastapi.HTTPException(status_code=404, detail="Транзакция не найдена")
    user = get_user(user_id)
    user["transactions"] = [t for t in user["transactions"] if t["id"] != transaction_id]
    return None


# =============================================================================
# Бюджеты — CRUD
# =============================================================================

@app.get("/users/{user_id}/budgets", response_model=list[dict], tags=["Budgets"])
def list_budgets(user_id: int):
    """Получить список бюджетов пользователя."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    return user.get("budgets", [])


@app.get("/users/{user_id}/budgets/{budget_id}", response_model=dict, tags=["Budgets"])
def get_budget(user_id: int, budget_id: int):
    """Получить бюджет по ID."""
    budget = find_budget(user_id, budget_id)
    if not budget:
        raise fastapi.HTTPException(status_code=404, detail="Бюджет не найден")
    return budget


@app.post("/users/{user_id}/budgets", response_model=dict, status_code=201, tags=["Budgets"])
def create_budget(user_id: int, budget_data: BudgetCreate):
    """Создать новый бюджет."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    # Проверка существования категории
    cat = find_category(user_id, budget_data.category_id)
    if not cat:
        raise fastapi.HTTPException(status_code=404, detail="Категория не найдена")
    global next_budget_id
    new_budget = {
        "id": next_budget_id,
        "amount": budget_data.amount,
        "period": budget_data.period,
        "category_id": budget_data.category_id,
        "user_id": user_id,
        "start_date": budget_data.start_date,
        "end_date": budget_data.end_date,
        "created_at": datetime.now(),
    }
    next_budget_id += 1
    user["budgets"].append(new_budget)
    return new_budget


@app.put("/users/{user_id}/budgets/{budget_id}", response_model=dict, tags=["Budgets"])
def update_budget(user_id: int, budget_id: int, budget_data: BudgetUpdate):
    """Обновить бюджет."""
    budget = find_budget(user_id, budget_id)
    if not budget:
        raise fastapi.HTTPException(status_code=404, detail="Бюджет не найден")
    if budget_data.amount is not None:
        budget["amount"] = budget_data.amount
    if budget_data.period is not None:
        budget["period"] = budget_data.period
    if budget_data.category_id is not None:
        budget["category_id"] = budget_data.category_id
    if budget_data.start_date is not None:
        budget["start_date"] = budget_data.start_date
    if budget_data.end_date is not None:
        budget["end_date"] = budget_data.end_date
    return budget


@app.delete("/users/{user_id}/budgets/{budget_id}", status_code=204, tags=["Budgets"])
def delete_budget(user_id: int, budget_id: int):
    """Удалить бюджет."""
    budget = find_budget(user_id, budget_id)
    if not budget:
        raise fastapi.HTTPException(status_code=404, detail="Бюджет не найден")
    user = get_user(user_id)
    user["budgets"] = [b for b in user["budgets"] if b["id"] != budget_id]
    return None


# =============================================================================
# Финансовые цели — CRUD
# =============================================================================

@app.get("/users/{user_id}/goals", response_model=list[dict], tags=["Goals"])
def list_goals(user_id: int):
    """Получить список целей пользователя."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    return user.get("goals", [])


@app.get("/users/{user_id}/goals/{goal_id}", response_model=dict, tags=["Goals"])
def get_goal(user_id: int, goal_id: int):
    """Получить цель по ID."""
    goal = find_goal(user_id, goal_id)
    if not goal:
        raise fastapi.HTTPException(status_code=404, detail="Цель не найдена")
    return goal


@app.post("/users/{user_id}/goals", response_model=dict, status_code=201, tags=["Goals"])
def create_goal(user_id: int, goal_data: GoalCreate):
    """Создать новую финансовую цель."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    global next_goal_id
    new_goal = {
        "id": next_goal_id,
        "name": goal_data.name,
        "target_amount": goal_data.target_amount,
        "current_amount": goal_data.current_amount,
        "user_id": user_id,
        "deadline": goal_data.deadline,
        "type": goal_data.type,
        "created_at": datetime.now(),
    }
    next_goal_id += 1
    user["goals"].append(new_goal)
    return new_goal


@app.put("/users/{user_id}/goals/{goal_id}", response_model=dict, tags=["Goals"])
def update_goal(user_id: int, goal_id: int, goal_data: GoalUpdate):
    """Обновить финансовую цель."""
    goal = find_goal(user_id, goal_id)
    if not goal:
        raise fastapi.HTTPException(status_code=404, detail="Цель не найдена")
    if goal_data.name is not None:
        goal["name"] = goal_data.name
    if goal_data.target_amount is not None:
        goal["target_amount"] = goal_data.target_amount
    if goal_data.current_amount is not None:
        goal["current_amount"] = goal_data.current_amount
    if goal_data.deadline is not None:
        goal["deadline"] = goal_data.deadline
    if goal_data.type is not None:
        goal["type"] = goal_data.type
    return goal


@app.delete("/users/{user_id}/goals/{goal_id}", status_code=204, tags=["Goals"])
def delete_goal(user_id: int, goal_id: int):
    """Удалить финансовую цель."""
    goal = find_goal(user_id, goal_id)
    if not goal:
        raise fastapi.HTTPException(status_code=404, detail="Цель не найдена")
    user = get_user(user_id)
    user["goals"] = [g for g in user["goals"] if g["id"] != goal_id]
    return None


# =============================================================================
# Уведомления — CRUD
# =============================================================================

@app.get("/users/{user_id}/notifications", response_model=list[dict], tags=["Notifications"])
def list_notifications(user_id: int, is_read: Optional[bool] = None):
    """Получить список уведомлений пользователя."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    notifications = user.get("notifications", [])
    if is_read is not None:
        notifications = [n for n in notifications if n["is_read"] == is_read]
    return notifications


@app.get("/users/{user_id}/notifications/{notification_id}", response_model=dict, tags=["Notifications"])
def get_notification(user_id: int, notification_id: int):
    """Получить уведомление по ID."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    for n in user.get("notifications", []):
        if n["id"] == notification_id:
            return n
    raise fastapi.HTTPException(status_code=404, detail="Уведомление не найдено")


@app.post("/users/{user_id}/notifications", response_model=dict, status_code=201, tags=["Notifications"])
def create_notification(user_id: int, notification_data: NotificationCreate):
    """Создать уведомление."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    global next_notification_id
    new_notification = {
        "id": next_notification_id,
        "user_id": user_id,
        "message": notification_data.message,
        "type": notification_data.type,
        "is_read": False,
        "created_at": datetime.now(),
    }
    next_notification_id += 1
    user["notifications"].append(new_notification)
    return new_notification


@app.put("/users/{user_id}/notifications/{notification_id}", response_model=dict, tags=["Notifications"])
def update_notification(user_id: int, notification_id: int, is_read: bool = True):
    """Обновить уведомление (например, пометить как прочитанное)."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    for n in user.get("notifications", []):
        if n["id"] == notification_id:
            n["is_read"] = is_read
            return n
    raise fastapi.HTTPException(status_code=404, detail="Уведомление не найдено")


@app.delete("/users/{user_id}/notifications/{notification_id}", status_code=204, tags=["Notifications"])
def delete_notification(user_id: int, notification_id: int):
    """Удалить уведомление."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    notifications = user.get("notifications", [])
    for i, n in enumerate(notifications):
        if n["id"] == notification_id:
            user["notifications"].pop(i)
            return None
    raise fastapi.HTTPException(status_code=404, detail="Уведомление не найдено")


# =============================================================================
# Профессии — CRUD
# =============================================================================

@app.get("/users/{user_id}/professions", response_model=list[dict], tags=["Professions"])
def list_professions(user_id: int):
    """Получить список профессий пользователя."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    return user.get("professions", [])


@app.get("/users/{user_id}/professions/{profession_id}", response_model=dict, tags=["Professions"])
def get_profession(user_id: int, profession_id: int):
    """Получить профессию по ID."""
    profession = find_profession(user_id, profession_id)
    if not profession:
        raise fastapi.HTTPException(status_code=404, detail="Профессия не найдена")
    return profession


@app.post("/users/{user_id}/professions", response_model=dict, status_code=201, tags=["Professions"])
def create_profession(user_id: int, profession_data: ProfessionCreate):
    """Создать новую профессию."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    global next_profession_id
    new_profession = {
        "id": next_profession_id,
        "title": profession_data.title,
        "description": profession_data.description,
        "created_at": datetime.now(),
    }
    next_profession_id += 1
    user["professions"].append(new_profession)
    return new_profession


@app.put("/users/{user_id}/professions/{profession_id}", response_model=dict, tags=["Professions"])
def update_profession(user_id: int, profession_id: int, profession_data: ProfessionUpdate):
    """Обновить профессию."""
    profession = find_profession(user_id, profession_id)
    if not profession:
        raise fastapi.HTTPException(status_code=404, detail="Профессия не найдена")
    if profession_data.title is not None:
        profession["title"] = profession_data.title
    if profession_data.description is not None:
        profession["description"] = profession_data.description
    return profession


@app.delete("/users/{user_id}/professions/{profession_id}", status_code=204, tags=["Professions"])
def delete_profession(user_id: int, profession_id: int):
    """Удалить профессию."""
    profession = find_profession(user_id, profession_id)
    if not profession:
        raise fastapi.HTTPException(status_code=404, detail="Профессия не найдена")
    user = get_user(user_id)
    user["professions"] = [p for p in user["professions"] if p["id"] != profession_id]
    return None


# =============================================================================
# Отчёты и аналитика
# =============================================================================

@app.get("/users/{user_id}/reports/summary", tags=["Reports"])
def get_summary(user_id: int):
    """Получить сводку по финансам пользователя."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    transactions = user.get("transactions", [])
    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    return {
        "user_id": user_id,
        "currency": user["currency"],
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense,
        "transactions_count": len(transactions),
        "categories_count": len(user.get("categories", [])),
        "budgets_count": len(user.get("budgets", [])),
        "goals_count": len(user.get("goals", [])),
    }


@app.get("/users/{user_id}/reports/by-category", tags=["Reports"])
def get_by_category(user_id: int):
    """Получить отчёт по категориям."""
    user = get_user(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="Пользователь не найден")
    transactions = user.get("transactions", [])
    categories = user.get("categories", [])
    category_map = {c["id"]: c["name"] for c in categories}
    category_totals = {}
    for t in transactions:
        cat_id = t["category_id"]
        cat_name = category_map.get(cat_id, f"Unknown ({cat_id})")
        if cat_name not in category_totals:
            category_totals[cat_name] = {"income": 0.0, "expense": 0.0}
        if t["type"] == "income":
            category_totals[cat_name]["income"] += t["amount"]
        else:
            category_totals[cat_name]["expense"] += t["amount"]
    return {"user_id": user_id, "categories": category_totals}
