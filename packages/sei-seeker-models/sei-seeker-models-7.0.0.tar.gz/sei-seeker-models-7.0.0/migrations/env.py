import os
import sys
 
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from sqlalchemy import create_engine
from alembic import context
from sqlalchemy.engine import URL

from sei_seeker_models import * # noqa
from sei_seeker_models.base import Base


sys.path.insert(0, ".")

DB_USER = os.getenv('DB_USER')  
DB_PASS = os.getenv('DB_PASS')  
DB_HOST = os.getenv('DB_HOST')  
DB_PORT = os.getenv('DB_PORT')  
DB_NAME = os.getenv('DB_NAME')  

# build DB_URI manually in production as Alembic seems to do its own string interpolation
ALEMBIC_DB_URI = URL.create("postgresql", DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)


alembic_config = context.config
alembic_config.set_main_option("sqlalchemy.url", str(ALEMBIC_DB_URI))
alembic_config.set_main_option("file_template", "%%(slug)s_%%(rev)s")
alembic_config.set_main_option("script_location", "migrations")
target_metadata = Base.metadata


def run_migrations_offline():
    url = str(ALEMBIC_DB_URI)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        # render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = alembic_config.get_section(alembic_config.config_ini_section)
    configuration["sqlalchemy.url"] = str(ALEMBIC_DB_URI)

    def process_revision_directives(context, revision, directives):
        if alembic_config.cmd_opts and alembic_config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    
    connectable = create_engine(ALEMBIC_DB_URI)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            process_revision_directives=process_revision_directives,
            # render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
