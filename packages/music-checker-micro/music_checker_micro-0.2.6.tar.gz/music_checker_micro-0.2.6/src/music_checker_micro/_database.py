"""
Database functions for music checker
"""

from ._music_file import MusicFile as MF
import logging
import sqlite3
import os
import jsonpickle

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
DEBUG = False


def __debug_message(message):
    if DEBUG:
        logging.debug(str(message))


def instantiate_sqlite_table(library_file: str) -> sqlite3.Cursor:
    """Sets up the required sqlite db"""
    con = sqlite3.connect(library_file)
    cur = con.cursor()
    res = cur.execute("SELECT ? FROM sqlite_master", ('media',))
    is_created = res.fetchone()
    if is_created is None:
        __debug_message("DB file not found - creating")
        cur.execute("CREATE TABLE media(tags, mtime, file_path type UNIQUE)")
    return cur


def db_connect(library_file: str) -> sqlite3.Cursor:
    con = sqlite3.connect(library_file)
    return con.cursor()


def mf_to_sub(entry: MF):
    return {'file_path': os.path.join(entry.path, entry.file_name)}


def db_entry_exists(cur: sqlite3.Cursor, entry: MF):
    # print(entry)
    sub_obj = mf_to_sub(entry)
    res = cur.execute('''
SELECT COUNT(1)
FROM media
WHERE file_path = :file_path;
''', sub_obj)
    return res.fetchone()


def db_get_mtime(cur: sqlite3.Cursor, entry: MF):
    sub_obj = mf_to_sub(entry)
    res = cur.execute('''
SELECT mtime
FROM media
WHERE file_path = :file_path;
''', sub_obj)
    return res.fetchone()


def db_get_all_paths(cur: sqlite3.Cursor):
    res = cur.execute('''
SELECT file_path
FROM media
                      ''')
    return res.fetchall()


def db_get_media_mtime(cur: sqlite3.Cursor, entry: MF) -> tuple:
    sub_obj = mf_to_sub(entry)
    res = cur.execute('''
SELECT mtime
FROM media
WHERE file_path = :file_path;
''', sub_obj)
    ret_val = res.fetchone()
    return 0 if ret_val is None else ret_val


def db_get_tag_dict(cur: sqlite3.Cursor, entry: MF) -> dict:
    return jsonpickle.decode(db_entry_get_tags(cur, entry)[0])


def db_entry_get_tags(cur: sqlite3.Cursor, entry: MF) -> tuple:
    sub_obj = mf_to_sub(entry)
    res = cur.execute('''
SELECT tags
FROM media
WHERE file_path = :file_path;
''', sub_obj)
    return res.fetchone()


def db_select_all(cur: sqlite3.Cursor) -> list:
    """
    Gets all entries from the DB
    """
    res = cur.execute(
        """
SELECT mtime, file_path
FROM media
    """
    )
    return res.fetchall()


def db_insert(cur: sqlite3.Cursor, entry: MF):
    """Places an entry into the db will match on file_path to update existing rows"""
    sub_obj = {
        'tags': jsonpickle.encode(entry.tags),
        'mtime': entry.mtime,
        'file_path': os.path.join(entry.path, entry.file_name)
    }
    cur.execute("""
                INSERT INTO media(mtime,file_path, tags) 
                VALUES (:mtime, :file_path, :tags) 
                ON CONFLICT(file_path) 
                DO UPDATE SET mtime=:mtime, file_path=:file_path, tags=:tags
                """,
                sub_obj)


def db_delete_entry(cur: sqlite3.Cursor, path: str):
    sub_obj = {
        'file_path': path
    }
    cur.execute("""
DELETE FROM media
WHERE file_path=:file_path;
""", sub_obj)


def db_delete(cur: sqlite3.Cursor) -> None:
    """Performs a delete on all rows in the music db"""
    cur.execute("DELETE FROM media")


def db_commit(sql_con: sqlite3.Connection) -> None:
    """Commits all outstanding statements"""
    sql_con.commit()


def db_close(sql_con: sqlite3.Connection) -> None:
    """Closes the connection"""
    sql_con.close()
