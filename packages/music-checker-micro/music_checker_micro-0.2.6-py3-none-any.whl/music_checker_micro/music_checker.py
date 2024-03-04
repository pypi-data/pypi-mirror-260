"""
Provides MusicChecker class
"""
from pathlib import Path

import logging
import os
import sqlite3

from ._music_file import MusicFile as MF
from ._database import instantiate_sqlite_table, db_entry_exists, db_entry_get_tags, db_insert
from ._database import db_commit
from ._database import db_get_tag_dict
from ._database import db_get_all_paths
from ._database import db_delete_entry
from ._database import db_select_all
from ._database import db_get_media_mtime
from ._mutagen_handler import get_all_mp3_id3_tags, get_all_file_tags
from music_manager_micro.music_manager import MusicManager as MM


class MusicChecker:
    """Class for functions to run tag checks against media files
    """
    # Constants
    # App specific props
    app_name = 'MusicCheckerMicro'

    # Directory and files
    config_dir: str = os.path.join(
        str(Path.home()), ".config/", app_name)
    cache_dir: str = os.path.join(
        str(Path.home()), ".cache/", app_name)
    cache_file: str = 'cache.db'

    # Variable
    # Session
    library: str = ''
    media_list: list = []
    music_file_list: list[MF] = []
    force_cache: bool = False
    db_cursor: sqlite3.Cursor
    force_recheck: bool = False

    _library_path = ''

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    DEBUG = False

    def _debug(self, message):
        if self.DEBUG:
            logging.debug(str(message))

    def __init__(self,
                 library: str = 'Library',
                 media_list: list | None = None,
                 cache_dir: str = None,
                 force_recheck: bool = False
                 ):
        self.force_recheck = force_recheck
        self._set_library(library)
        if cache_dir is not None:
            self.cache_dir = cache_dir
        if media_list is not None:
            self.media_list = media_list
        else:
            self.media_list = self._get_music_manager_list()

    def _generate_library_path(self) -> str:
        self._library_path = os.path.join(
            self.cache_dir, self.library, self.cache_file)
        path = Path(os.path.join(self.cache_dir, self.library))
        path.mkdir(parents=True, exist_ok=True)

    def _set_library(self, library: str) -> None:
        """Used to change the active library used by the class"""
        self.library = library
        self._generate_library_path()
        self.db_cursor = instantiate_sqlite_table(self._library_path)

    def _get_entry_tags(self, entry: MF):
        exists = db_entry_exists(self.db_cursor, entry)
        if int(exists[0]) == 0 or self.force_recheck is True:
            entry.tags = get_all_file_tags(
                os.path.join(
                    entry.path,
                    entry.file_name
                )
            )
        else:

            db_tags = db_entry_get_tags(self.db_cursor, entry)
            if db_tags[0] is None:
                entry.tags = get_all_file_tags(
                    os.path.join(
                        entry.path,
                        entry.file_name
                    )
                )
            else:
                db_mtime = db_get_media_mtime(self.db_cursor, entry)
                if entry.mtime is not db_mtime:
                    entry.tags = get_all_file_tags(
                        os.path.join(
                            entry.path,
                            entry.file_name
                        )
                    )
                else:
                    entry.tags = db_get_tag_dict(self.db_cursor, entry)

        # if db_entry_exists(self.db_cursor, entry):
        #    entry.tags = db_entry_get_tags(self.db_cursor, entry)
        # else:
        #    entry.tags = get_all_mp3_id3_tags(entry.file_name)

    def _build_entry(self, media_file: tuple) -> MF:
        path = media_file[1].rsplit('/', 1)[0]
        file_name = media_file[1].split('/')[-1]
        mtime = media_file[0]
        entry = MF(
            path=path,
            file_name=file_name,
            mtime=mtime,
            file_type=file_name.split('.')[-1],
            tags={},
            artwork=[]
        )
        self._get_entry_tags(entry)
        return entry

    def _get_music_manager_list(self) -> list:
        mm = MM(self.library)
        # print(mm.get_list())
        return mm.get_list()

    def _build_list(self) -> list:
        music_file_list = []
        for m in self.media_list:
            music_file_list.append(self._build_entry(m))
        return music_file_list

    def _build_tag_list(self) -> list:
        tag_list = []
        for m in self.media_list:
            tag_list.append(self._build_entry(m))
        return tag_list

    def execute_tag_finder(self) -> list:
        """Returns a list of unique tags found"""
        return_list = []

        return return_list

    def get_all_db_entries(self) -> list[str]:
        cur_entries = db_get_all_paths(self.db_cursor)
        return [x[0] for x in cur_entries]

    def remove_old_entries(self) -> None:
        cur_entries = self.get_all_db_entries()
        to_compare = [os.path.join(x.path, x.file_name)
                      for x in self.music_file_list]
        diff = list(set(cur_entries).difference(to_compare))
        for d in diff:
            db_delete_entry(self.db_cursor, d)

    def get_list(self) -> list[MF]:
        all_music = db_select_all(self.db_cursor)
        self.music_file_list = []
        for a in all_music:
            self.music_file_list.append(self._build_entry(a))
        return self.music_file_list

    def save_list(self):
        for m in self.music_file_list:
            db_insert(self.db_cursor, m)
        db_commit(self.db_cursor.connection)

    def update_list(self):
        self.remove_old_entries()
        self.save_list()

    def execute(self) -> list[MF]:
        """Returns a list of tag values for each supported media file"""
        self.music_file_list = self._build_list()
        self.update_list()
        return self.music_file_list
