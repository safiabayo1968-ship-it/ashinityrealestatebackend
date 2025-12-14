import sys
import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

# --- Ensure project root is on sys.path ---
# This makes "ashinity" importable when Alembic runs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# --- Import your settings and models ---
from ashinity.core.config import settings
from ashinity.core.db import Base
from ashinity.models import user, property, inquiry, favorite

# Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate'
target_metadata = Base.metadata


def get_url():
    # Use your DATABASE_URL from settings
    return settings.DATABASE_URL.replace("postgresql+psycopg", "postgresql+psycopg")


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(get_url(), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


## from logging.config import fileConfig
## from sqlalchemy import create_engine
## from sqlalchemy import pool
## from alembic import context



config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    return settings.DATABASE_URL.replace("postgresql+psycopg", "postgresql+psycopg")

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(get_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
