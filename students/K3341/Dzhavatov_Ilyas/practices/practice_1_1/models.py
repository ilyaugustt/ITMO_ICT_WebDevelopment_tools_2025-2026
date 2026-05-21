from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# --- Пользователи ---

class UserBase(BaseModel):
    username: str
    email: str
    currency: str = "RUB"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    currency: Optional[str] = None


class User(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# --- Категории ---

class CategoryBase(BaseModel):
    name: str
    type: str  # "income" или "expense"


class CategoryCreate(CategoryBase):
    user_id: int


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None


class Category(CategoryBase):
    id: int
    user_id: int
    icon: Optional[str] = None
    created_at: Optional[datetime] = None


# --- Транзакции ---

class TransactionBase(BaseModel):
    amount: float
    type: str  # "income" или "expense"
    category_id: int
    date: date
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    user_id: int


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category_id: Optional[int] = None
    date: Optional[date] = None
    description: Optional[str] = None


class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None


# --- Бюджеты ---

class BudgetBase(BaseModel):
    amount: float
    period: str  # "monthly", "weekly", "yearly"
    category_id: int


class BudgetCreate(BudgetBase):
    user_id: int
    start_date: date
    end_date: date


class BudgetUpdate(BaseModel):
    amount: Optional[float] = None
    period: Optional[str] = None
    category_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class Budget(BudgetBase):
    id: int
    user_id: int
    start_date: date
    end_date: date
    created_at: Optional[datetime] = None


# --- Финансовые цели ---

class GoalBase(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0
    deadline: Optional[date] = None
    type: str  # "savings" или "reduction"


class GoalCreate(GoalBase):
    user_id: int


class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[date] = None
    type: Optional[str] = None


class Goal(GoalBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None


# --- Профессии ---

class ProfessionBase(BaseModel):
    title: str
    description: Optional[str] = None


class ProfessionCreate(ProfessionBase):
    pass


class ProfessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class Profession(ProfessionBase):
    id: int
    created_at: Optional[datetime] = None


# --- Уведомления ---

class NotificationBase(BaseModel):
    message: str
    type: str  # "budget_exceeded" или "goal_reached"


class NotificationCreate(NotificationBase):
    user_id: int


class Notification(NotificationBase):
    id: int
    is_read: bool = False
    created_at: Optional[datetime] = None
