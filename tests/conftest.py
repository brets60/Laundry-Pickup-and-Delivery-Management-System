import os
import shutil
import pytest


@pytest.fixture(scope="session", autouse=True)
def preserve_database_state():
    """Preserves the live database state so running the test suite does not pollute operational tables."""
    db_path = "laundry.db"
    backup_path = "laundry.db.pytest_bak"

    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)

    yield

    if os.path.exists(backup_path):
        shutil.copy2(backup_path, db_path)
        try:
            os.remove(backup_path)
        except OSError:
            pass
