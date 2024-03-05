import concurrent.futures
import json
import sqlite3
from pathlib import Path
from threading import Event

from pysword.modules import SwordModules

from sword_converter.utils.progress import Progress


class Bible(object):
    def __init__(self, source, module):
        modules = SwordModules(source)
        parsed_modules = modules.parse_modules()
        self._name = parsed_modules[module]["description"]
        self._abbreviation = module
        self.sword_bible = modules.get_bible_from_module(module)
        self._output_file = f"{Path(source).resolve().parent / '_'.join(self._name.split())}.{{extension}}"

    def to_json(self):
        data = {
            "name": self._name,
            "abbreviation": self._abbreviation,
            "books": {}
        }

        for testament, books in self.sword_bible.get_structure().get_books().items():
            data["books"][testament] = []
            for book_number, book in enumerate(books, start=sum([len(v) for v in data["books"].values()]) + 1):
                progress = Progress(book.name, book.num_chapters)
                _book = {
                    "number": book_number,
                    "name": book.name,
                    "abbreviation": book.preferred_abbreviation,
                    "chapters": []
                }
                for chapter_number in range(1, book.num_chapters + 1):
                    _book["chapters"].append({
                        "number": chapter_number,
                        "verses": [{
                            "number": verse_number,
                            "text": self.sword_bible.get(
                                books=book.name,
                                chapters=chapter_number,
                                verses=verse_number,
                                join=""
                            )
                        } for verse_number in range(1, book.chapter_lengths[chapter_number - 1] + 1)]})
                    progress.update(chapter_number)
                data["books"][testament].append(_book)

        with open(self._output_file.format(extension="json"), "w") as fp:
            self._save(json.dump, obj=data, fp=fp)
            return fp.name

    def to_sqlite(self):
        database = self._output_file.format(extension="db")
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS verses")
        cursor.execute("DROP TABLE IF EXISTS chapters")
        cursor.execute("DROP TABLE IF EXISTS books")
        cursor.execute("DROP TABLE IF EXISTS translations")

        cursor.execute("""CREATE TABLE translations(
        name TEXT UNIQUE NOT NULL,
        abbreviation TEXT UNIQUE NOT NULL)""")

        cursor.execute("""CREATE TABLE books(
            translation INTEGER NOT NULL,
            number INTEGER NOT NULL,
            name TEXT NOT NULL,
            abbreviation TEXT NOT NULL,
            testament TEXT CHECK ( testament IN ('nt','ot')) NOT NULL,
            UNIQUE (translation,number,name,abbreviation),
            FOREIGN KEY (translation) REFERENCES translations(ROWID))""")

        cursor.execute("""CREATE TABLE chapters(
            book INTEGER NOT NULL,
            number INTEGER NOT NULL,
            UNIQUE (book,number),
            FOREIGN KEY (book) REFERENCES books(ROWID))""")

        cursor.execute("""CREATE TABLE verses(
            chapter INTEGER NOT NULL,
            number INTEGER NOT NULL,
            text TEXT NOT NULL,
            UNIQUE (chapter,number,text),
            FOREIGN KEY (chapter) REFERENCES chapters(ROWID))""")

        cursor.execute("INSERT INTO translations VALUES(?,?)", (self._name, self._abbreviation))

        translation_rowid = cursor.lastrowid

        for testament, books in self.sword_bible.get_structure().get_books().items():
            start = cursor.execute(
                "SELECT COUNT(*) FROM books WHERE translation = ?",
                (translation_rowid,)
            ).fetchone()[0]
            for book_number, book in enumerate(books, start=start + 1):
                progress = Progress(book.name, book.num_chapters)
                cursor.execute(
                    "INSERT INTO books VALUES(?,?,?,?,?)",
                    (
                        translation_rowid,
                        book_number,
                        book.name,
                        book.preferred_abbreviation,
                        testament
                    ))
                book_rowid = cursor.lastrowid
                for chapter_number in range(1, book.num_chapters + 1):
                    cursor.execute(
                        "INSERT INTO chapters VALUES(?,?)",
                        (
                            book_rowid,
                            chapter_number
                        ))
                    chapter_rowid = cursor.lastrowid
                    cursor.executemany(
                        "INSERT INTO verses VALUES(?,?,?)",
                        (
                            (
                                chapter_rowid,
                                verse_number,
                                self.sword_bible.get(
                                    books=book.name,
                                    chapters=chapter_number,
                                    verses=verse_number,
                                    join=""
                                )
                            ) for verse_number in range(1, book.chapter_lengths[chapter_number - 1] + 1)
                        ))
                    progress.update(chapter_number)

        def save():
            cursor.close()
            connection.commit()
            connection.close()

        self._save(save, database=database)
        return database

    @staticmethod
    def _save(fn, **kwargs):
        progress = Progress(title=f"Saving to {kwargs.pop('database', None) or kwargs['fp'].name}")
        event = Event()
        executor = concurrent.futures.ThreadPoolExecutor()
        executor.submit(progress.infinite, event)
        fn(**kwargs)
        event.set()
