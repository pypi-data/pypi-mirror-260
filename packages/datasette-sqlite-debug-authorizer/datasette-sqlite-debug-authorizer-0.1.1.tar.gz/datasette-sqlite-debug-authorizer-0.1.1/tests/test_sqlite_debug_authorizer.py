from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_select(capsys):
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/_memory.json?sql=select+1")
    assert response.status_code == 200
    captured = capsys.readouterr().err
    # There should be all sorts of stuff in there
    for expected in (
        "SQLITE_SELECT:",
        'SQLITE_READ:  table="sqlite_master"',
        "SQLITE_PRAGMA:",
    ):
        assert expected in captured


@pytest.mark.asyncio
async def test_insert_delete(capsys):
    # https://github.com/datasette/datasette-sqlite-debug-authorizer/issues/2
    datasette = Datasette()
    db = datasette.add_memory_database("test_insert_delete")
    await db.execute_write("create table foo (name text)")
    await db.execute_write("insert into foo (name) values ('bar')")
    await db.execute_write("delete from foo where name='bar'")
    captured = capsys.readouterr().err
    assert 'SQLITE_INSERT:  table="foo" db_name=main' in captured
    assert 'SQLITE_DELETE:  table="foo" db_name=main' in captured
