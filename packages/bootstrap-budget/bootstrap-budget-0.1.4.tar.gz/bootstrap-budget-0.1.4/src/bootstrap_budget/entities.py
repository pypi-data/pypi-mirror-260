from datetime import datetime
from pony import orm


# Define database and entities (Pony ORM)
db = orm.Database()


class User(db.Entity):
    _table_ = 'USER'

    id = orm.PrimaryKey(int, auto=True)
    last_name = orm.Optional(str, nullable=True)
    first_name = orm.Optional(str, nullable=True)
    middle_name = orm.Optional(str, nullable=True)
    username = orm.Required(str, unique=True)
    address_line_1 = orm.Optional(str, nullable=True)
    address_line_2 = orm.Optional(str, nullable=True)
    city = orm.Optional(str, nullable=True)
    state = orm.Optional(str, nullable=True)
    zipcode = orm.Optional(str, nullable=True)
    email = orm.Optional(str, nullable=True)
    phone_number = orm.Optional(str, nullable=True)
    hash = orm.Required(str)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    accounts = orm.Set('Account')
    configs = orm.Set('Config')
    budgets = orm.Set('Budget')
    budget_items = orm.Set('BudgetItem')
    transactions = orm.Set('Transaction')
    user_budgets = orm.Set('UserBudget')


"""
CREATE TABLE "USER" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "last_name" TEXT,
    "first_name" TEXT,
    "middle_name" TEXT,
    "username" TEXT UNIQUE NOT NULL,
    "address_line_1" TEXT,
    "address_line_2" TEXT,
    "city" TEXT,
    "state" TEXT,
    "zipcode" TEXT,
    "email" TEXT,
    "phone_number" TEXT,
    "hash" TEXT NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL
);
"""


class Config(db.Entity):
    _table_ = 'CONFIG'

    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str, unique=True)
    description = orm.Optional(str, nullable=True)
    config_value = orm.Optional(str, nullable=True)
    config_value_type = orm.Required(int, default=0)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    orm.composite_key(name, user_id)


"""
CREATE TABLE "CONFIG" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT UNIQUE NOT NULL,
    "description" TEXT,
    "config_value" TEXT,
    "config_value_type" INTEGER NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    CONSTRAINT "unq_config__name_user_id" UNIQUE ("name", "user_id")
);

CREATE INDEX "idx_config__user_id" ON "CONFIG" ("user_id");
"""


class Budget(db.Entity):
    _table_ = 'BUDGET'

    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    description = orm.Optional(str, nullable=True)
    budget_year = orm.Required(int)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    user_budgets = orm.Set('UserBudget')
    orm.composite_key(name, user_id)


"""
CREATE TABLE "BUDGET" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "budget_year" INTEGER NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    CONSTRAINT "unq_budget__name_user_id" UNIQUE ("name", "user_id")
);

CREATE INDEX "idx_budget__user_id" ON "BUDGET" ("user_id");
"""


class UserBudget(db.Entity):
    _table_ = 'USER_BUDGET'

    id = orm.PrimaryKey(int, auto=True)
    permissions = orm.Required(int)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    budget_id = orm.Required(Budget)


"""
CREATE TABLE "USER_BUDGET" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "permissions" INTEGER NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    "budget_id" INTEGER NOT NULL REFERENCES "BUDGET" ("id") ON DELETE CASCADE
);

CREATE INDEX "idx_user_budget__budget_id" ON "USER_BUDGET" ("budget_id");
CREATE INDEX "idx_user_budget__user_id" ON "USER_BUDGET" ("user_id");
"""


class BudgetItem(db.Entity):
    _table_ = 'BUDGET_ITEM'

    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    description = orm.Optional(str, nullable=True)
    budget_amount = orm.Required(float, default=0)
    sequence_order = orm.Required(int, default=99)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    transactions = orm.Set('Transaction')
    orm.composite_key(name, user_id)


"""
CREATE TABLE "BUDGET_ITEM" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "budget_amount" REAL NOT NULL,
    "sequence_order" INTEGER NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    CONSTRAINT "unq_budget_item__name_user_id" UNIQUE ("name", "user_id")
);

CREATE INDEX "idx_budget_item__user_id" ON "BUDGET_ITEM" ("user_id");
"""


class Account(db.Entity):
    _table_ = 'ACCOUNT'

    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    description = orm.Optional(str, nullable=True)
    account_number = orm.Optional(str, nullable=True)
    account_route_nbr = orm.Optional(str, nullable=True)
    opening_amount = orm.Required(float, default=0)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    transactions = orm.Set('Transaction')
    orm.composite_key(name, user_id)


"""
CREATE TABLE "ACCOUNT" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "account_number" TEXT,
    "account_route_nbr" TEXT,
    "opening_amount" REAL NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    CONSTRAINT "unq_account__name_user_id" UNIQUE ("name", "user_id")
);

CREATE INDEX "idx_account__user_id" ON "ACCOUNT" ("user_id");
"""


class Transaction(db.Entity):
    _table_ = 'TRANSACTION'

    id = orm.PrimaryKey(int, auto=True)
    description = orm.Optional(str, nullable=True)
    amount = orm.Required(float, default=0)
    transaction_dt_tm = orm.Required(datetime)
    note = orm.Optional(str, nullable=True)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime, nullable=True)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    account_id = orm.Required(Account)
    budget_item_id = orm.Required(BudgetItem)


"""
CREATE TABLE "TRANSACTION" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "description" TEXT,
    "amount" REAL NOT NULL,
    "transaction_dt_tm" DATETIME NOT NULL,
    "note" TEXT,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    "account_id" INTEGER NOT NULL REFERENCES "ACCOUNT" ("id") ON DELETE CASCADE,
    "budget_item_id" INTEGER NOT NULL REFERENCES "BUDGET_ITEM" ("id") ON DELETE CASCADE
);

CREATE INDEX "idx_transaction__account_id" ON "TRANSACTION" ("account_id");
CREATE INDEX "idx_transaction__budget_item_id" ON "TRANSACTION" ("budget_item_id");
CREATE INDEX "idx_transaction__user_id" ON "TRANSACTION" ("user_id");
"""
