import logging
from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor
from models import AbstractExtractor

logger = logging.getLogger()


class PostgresExtractor(AbstractExtractor):

    data = []

    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = pg_conn.cursor(cursor_factory=RealDictCursor)

    def get_data(self):
        """
        Получает не проиндексированные фильмы с сопутствующими данными
        :return: результат выборки
        """
        sql = """
            WITH movies AS (
                SELECT
                    id, 
                    title, 
                    description, 
                    rating, 
                    type 
                FROM content.film_work
                WHERE not indexed
                LIMIT 100
            )
            SELECT
                fw.id, 
                fw.title, 
                fw.description, 
                fw.rating, 
                fw.type,
                CASE
                    WHEN pfw.role = 'actor' 
                    THEN ARRAY_AGG(distinct p.full_name)
                END AS actors,
                CASE
                    WHEN pfw.role = 'writer' 
                    THEN ARRAY_AGG(distinct p.full_name)
                END AS writers,
                CASE
                    WHEN pfw.role = 'director' 
                    THEN ARRAY_AGG(distinct p.full_name)
                END AS directors,
                ARRAY_AGG(g.name) AS genres
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            GROUP BY
                fw.id, 
                fw.title, 
                fw.description, 
                fw.rating, 
                fw.type, 
                pfw.role	                   
        """

        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()

        logger.info('Extracted', len(self.data))
        return self.data

    def set_index(self):
        """
        После загрузки устанавливается признак индексации
        Снятие индексации происходит во время обновления записей в админке
        :return:
        """
        data = ','.join(self.cursor.mogrify('%s', (item['id'],)).decode()
                        for item in self.data)
        sql = f"""
            UPDATE content.film_work
            SET indexed = True
            WHERE id in ({data});
        """

        self.cursor.execute(sql, (data, ))
        self.conn.commit()
        logger.info('Indexed')
