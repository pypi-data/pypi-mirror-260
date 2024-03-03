"""
Provides DB functions
"""
import sqlite3
import os

from ._music_file import MusicFile as MF


class DB():
    """
    Only need to instantiate once, not dependant on specific DB you are accessing 
    """

    def __init__(self) -> None:
        pass

    def instantiate_sqlite_table(self, file_name: str) -> sqlite3.Cursor:
        """Sets up the required sqlite db"""
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS track(
                    file_path type UNIQUE,
                    mtime
                    )
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS track_tag(
                    track,
                    tag,
                    value,
                    PRIMARY KEY (track, tag)
                    FOREIGN KEY (track)
                        REFERENCES track (ROWID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )
                    """)
        return cur

    def db_get_all_tracks(self, cur: sqlite3.Cursor) -> list[tuple[str, str]]:
        """Returns all values from the current db"""
        res = cur.execute("SELECT * FROM track")
        ret_val = res.fetchall()
        # print(f'db_get_all ret val {ret_val}')
        return [] if ret_val is None else ret_val

    def db_get_track_tags(self, cur: sqlite3.Cursor, path: str) -> list[tuple]:
        """
        With a given file path returns a list of tuples of the tags.
        In the format of (path, tag name, tag value)
        """
        sub_obj = {
            'file_path': path
        }
        res = cur.execute(
            """
SELECT *
FROM track_tag
WHERE track=:file_path
            """,
            sub_obj
        )
        ret_val = res.fetchall()
        return [] if ret_val is None else ret_val

    def db_get_all_tags(self, cur: sqlite3.Cursor) -> list:
        """Returns all the tag records from the db"""
        res = cur.execute("SELECT * FROM track_tag")
        ret_val = res.fetchall()
        return [] if ret_val is None else ret_val

    def db_get_distinct_artist_mbid(self, cur: sqlite3.Cursor) -> list:
        res = cur.execute("""
                          SELECT DISTINCT value
                          FROM track_tag
                          WHERE tag="TXXX:MusicBrainz Artist Id"
                          """)
        ret_val = [x[0] for x in res.fetchall()]
        return [] if ret_val is None else ret_val

    def mf_to_sub(self, entry: MF):
        """
        Converts a MusicFile object to a suitable dict for substitutions
        """
        return {
            'file_path': os.path.join(entry.path, entry.file_name),
            'mtime': entry.mtime,
        }

    def db_insert_track(self, cur: sqlite3.Cursor, entry: MF):
        """Places an entry into the db with two values
        mtime and file_path from the tuple
        will match on file_path to update existing rows"""
        sub_obj = self.mf_to_sub(entry)
        cur.execute("""
                    INSERT INTO track(mtime,file_path) 
                    VALUES (:mtime, :file_path) 
                    ON CONFLICT(file_path) 
                    DO UPDATE SET mtime=:mtime, file_path=:file_path
                    """,
                    sub_obj)

    def db_get_track_id(self,
                        cur: sqlite3.Cursor,
                        file_path: str
                        ) -> str:
        sub_obj = {
            "file_path": file_path
        }
        res = cur.execute("""
                        SELECT ROWID
                        FROM track
                        WHERE file_path=:file_path
                        """,
                          sub_obj)
        ret_val = res.fetchone()
        return () if ret_val is None else ret_val

    def db_insert_tag(
            self,
            cur: sqlite3.Cursor,
            file_path: str,
            tag_name: str,
            tag_value: str) -> None:
        """
        Place a new tag entry related to a track, if the tag name
        already exists will update the value
        """

        track_id = self.db_get_track_id(cur, file_path)[0]
        sub_obj = {
            "track": track_id,
            "tag": tag_name,
            "value": tag_value,
        }
        res = cur.execute(
            """
INSERT INTO track_tag(track, tag, value)
VALUES(:track,:tag,:value)
ON CONFLICT (track, tag)
DO UPDATE SET value=:value
            """,
            sub_obj
        )

    def _db_delete_tags(self, cur: sqlite3.Cursor, path):
        pass

    def db_delete_track(self, cur: sqlite3.Cursor, path):
        """
        With a given file path will attempt to delete the track
        record. Cascade delete will remove related tags 
        """
        sub_obj = {
            "file_path": path
        }
        res = cur.execute(
            """
DELETE FROM track
WHERE file_path=:path
            """,
            sub_obj
        )

    def _insert_tags(self, cur: sqlite3.Cursor, path):
        pass

    def db_commit(self, sql_con: sqlite3.Connection) -> None:
        """Commits all outstanding statements"""
        sql_con.commit()

    def db_close(self, sql_con: sqlite3.Connection) -> None:
        """Closes the connection"""
        sql_con.close()
