"""
Provides MusicValidator class
"""
from sqlite3 import Cursor
from pathlib import Path
import os
import logging

from music_checker_micro.music_checker import MusicChecker as MC
from ._music_file import MusicFile as MF
from ._database import DB


class MusicValidator():
    """
    Provided a series of MusicFile objects will check for attributes
    and tags of the provided files and validate against a series
    of conditions

    Will by default check for 'TALB' and 'TIT2' ID3 tags
    """
    # consts
    # App specific props
    app_name = 'MusicValidatorMicro'

    # Directory and files
    config_dir: str = os.path.join(
        str(Path.home()), ".config/", app_name)
    config_file: str = f"{app_name}.conf"
    cache_dir: str = os.path.join(
        str(Path.home()), ".cache/", app_name)
    cache_file: str = 'cache.db'
    ###

    # Instance vars
    music_checker: MC
    library: str
    database: DB
    db_cursor: Cursor
    library_path: str
    tag_list: list[str]

    db_music_file_list: list[tuple[str, str]]
    mc_music_file_list: list[MF]

    file_tag_dict: list

    tag_report_result: dict[str:list[str]]

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    DEBUG = False

    def _debug(self, message):
        if self.DEBUG:
            logging.debug(str(message))

    def __init__(self, library: str = 'library', tag_list: list[str] = None, mc: MC = None) -> None:
        if mc is None:
            self.music_checker = MC(library)
        else:
            self.music_checker = mc
        if tag_list is None:
            self.tag_list = ['TALB', 'TIT2']
        else:
            self.tag_list = tag_list
        self._set_library(library)
        self._setup_database()

    def _generate_library_path(self) -> str:
        self.library_path = os.path.join(
            self.cache_dir, self.library, self.cache_file)
        path = Path(os.path.join(self.cache_dir, self.library))
        path.mkdir(parents=True, exist_ok=True)

    def _setup_database(self):
        self.database = DB()
        self.db_cursor = self.database.instantiate_sqlite_table(
            self.library_path)

    def _set_library(self, library):
        self.library = library
        self._generate_library_path()

    def _get_mc_file_list(self):
        return self.music_checker.get_list()

    def _get_db_file_list(self):
        return self.database.db_get_all_tracks(self.db_cursor)

    def _set_db_music_file_list(self, media_list: list):
        self.db_music_file_list = media_list

    def _set_mc_music_file_list(self, media_list: list[MF]):
        self.mc_music_file_list = media_list

    def _remove_old_db_entries(self):
        """
        Compares the values in mc_music_file_list and 
        db_music_file_list to remove missing entries
        """
        cur_entries = [x[0] for x in self.db_music_file_list]
        to_compare = [os.path.join(x.path, x.file_name)
                      for x in self.mc_music_file_list]

        diff = list(set(cur_entries).difference(to_compare))
        for d in diff:
            self.database.db_delete_track(self.db_cursor, d)
        self._db_commit()

    def _update_db_entries(self):
        """
        Using the mc_music_file_list adds each entry to the db
        and associated tag entries
        """

        for m in self.mc_music_file_list:
            self.database.db_insert_track(self.db_cursor, m)

        self._db_commit()
        for m in self.mc_music_file_list:
            for k, v in m.tags.items():
                self.database.db_insert_tag(
                    self.db_cursor,
                    os.path.join(m.path, m.file_name),
                    k,
                    v
                )
        self._set_db_music_file_list(self._get_db_file_list())
        self._db_commit()

    def _db_commit(self):
        self.database.db_commit(self.db_cursor.connection)

    def _construct_tag_dict(self):
        """
        Iterates across the db files and builds a dict from them
        in the format {path:file_path,tags:{tag:value}}
        """
        self.file_tag_dict = []
        for m in self.db_music_file_list:
            entry = {}
            entry["path"] = m[0]
            entry["tags"] = {x[1]: x[2]
                             for x in self.database.db_get_track_tags(
                self.db_cursor,
                m[0]
            )
            }
            self.file_tag_dict.append(entry)

    def _generate_report(self):
        """
        For each value in the file tags compares the object with
        the list of tags to check. For each missing adds to a report
        with the file path
        """
        self.tag_report_result = {k: [] for k in self.tag_list}
        for f in self.file_tag_dict:
            cur_entries = [k for k, v in f['tags'].items()]
            to_compare = self.tag_list

            diff = list(set(to_compare).difference(cur_entries))
            for d in diff:
                self.tag_report_result[f"{d}"].append(f["path"])

    def get_all_artist_mbid(self) -> list[str]:
        ret_val = []
        ret_val = self.database.db_get_distinct_artist_mbid(self.db_cursor)
        return ret_val

    def execute(self) -> dict[str:list[str]]:
        """
        Runs the report on the most recent MusicChecker dataset
        will prune old tracks and update tag entries

        Returns an object of tags with tracks that did not pass
        the validation
        """
        self._set_mc_music_file_list(self._get_mc_file_list())
        self._set_db_music_file_list(self._get_db_file_list())
        self._remove_old_db_entries()
        self._construct_tag_dict()
        self._update_db_entries()
        self._generate_report()
        return self.tag_report_result

    def get_list(self) -> dict:
        """
        Returns the current report result
        """
        self._set_db_music_file_list(self._get_db_file_list())
        self._construct_tag_dict()
        self._generate_report()
        return self.tag_report_result
