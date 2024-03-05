from datasette_test import Datasette
import pytest
import sqlite3


@pytest.fixture
def db_paths(tmpdir):
    db_paths = []
    for name in ("test1.db", "test2.db"):
        db_path = str(tmpdir / name)
        conn = sqlite3.connect(db_path)
        with conn:
            conn.executescript(
                """
                create table protected (id integer primary key, name text);
                insert into protected (name) values ('one');
                """
            )
        db_paths.append(db_path)
    return db_paths


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sql",
    (
        "delete from protected",
        "delete from protected where id = 1",
        "update protected set name = 'foo'",
        "drop table protected",
        "insert into protected (name) values ('two')",
        "alter table protected rename to protected2",
    ),
)
@pytest.mark.parametrize("configured", (True, False))
@pytest.mark.parametrize("test1_only", (None, "test1"))
async def test_read_only_tables(sql, configured, db_paths, test1_only):
    plugin_config = {}
    if configured:
        rule = {
            "table": "protected",
        }
        if test1_only:
            rule["database"] = "test1"
        plugin_config = {"datasette-sqlite-authorizer": {"read_only_tables": [rule]}}

    datasette = Datasette(db_paths, plugin_config=plugin_config)
    db = datasette.get_database("test1")
    if configured:
        # SQL should not be allowed
        with pytest.raises(Exception):
            await db.execute_write(sql)

        if test1_only:
            # SQL should be allowed on test2
            db2 = datasette.get_database("test2")
            await db2.execute_write(sql)
        else:
            # SQL should not be allowed on test2
            db2 = datasette.get_database("test2")
            with pytest.raises(Exception):
                await db2.execute_write(sql)

    else:
        # SQL should be allowed
        await db.execute_write(sql)


@pytest.mark.asyncio
async def test_debug_actions(capsys):
    datasette = Datasette(
        plugin_config={
            "datasette-sqlite-authorizer": {
                "debug_actions": [
                    "SQLITE_SELECT",
                    "SQLITE_CREATE",
                    "SQLITE_INSERT",
                    "SQLITE_DELETE",
                ]
            }
        }
    )
    db = datasette.add_memory_database("test_debug_actions")
    await db.execute("select 1")
    await db.execute_write("create table foo (id integer primary key)")
    await db.execute_write("insert into foo (id) values (1)")
    await db.execute_write("delete from foo where id = 1")
    captured = capsys.readouterr().err
    assert captured == (
        'authorizer: {"action": "SQLITE_SELECT", "arg1": null, "arg2": null, '
        '"db_name": null, "trigger_name": null, "result": "OK"}\n'
        'authorizer: {"action": "SQLITE_INSERT", "arg1": "sqlite_master", "arg2": null, '
        '"db_name": "main", "trigger_name": null, "result": "OK"}\n'
        'authorizer: {"action": "SQLITE_INSERT", "arg1": "foo", "arg2": null, '
        '"db_name": "main", "trigger_name": null, "result": "OK"}\n'
        'authorizer: {"action": "SQLITE_DELETE", "arg1": "foo", "arg2": null, '
        '"db_name": "main", "trigger_name": null, "result": "OK"}\n'
    )
