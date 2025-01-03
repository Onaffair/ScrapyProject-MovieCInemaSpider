import json
import os.path
import re
from datetime import datetime, timedelta
import mysql.connector

# 数据库配置
base_dir = r'D:\Code\Database'

db = mysql.connector.Connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='online_purchase',
    charset='utf8',
    buffered=True
)
cursor = db.cursor()

def format_release_date_for_movie(date_str):
    """处理日期字符串，返回 'YYYY-MM-DD' 格式的日期"""
    if not date_str or not isinstance(date_str, str):
        return '2049-10-01'
    date_str = date_str.strip()
    try:
        date_str = date_str.split(' ')[0]
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m')
            return date_obj.replace(day=1).strftime('%Y-%m-%d')
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, '%Y')
                return date_obj.replace(month=1, day=1).strftime('%Y-%m-%d')
            except ValueError:
                return '2049-10-01'

def format_screening_time_for_screening(date_str):
    """
    提取和格式化时间数据。

    :param date_str: 时间字符串，如 "11月25日 15:30" 或 "Unknown Time"
    :return: 格式化后的时间对象，或者 None（如果数据为 Unknown Time）
    """
    if date_str.strip() == "Unknown Time":
        return None
    try:
        # 动态获取当前年份
        current_year = datetime.now().year
        # 在时间字符串中添加年份并解析
        formatted_date = datetime.strptime(f"{current_year}年{date_str.strip()}", "%Y年%m月%d日 %H:%M")
        return formatted_date.strftime('%Y-%m-%d %H:%M:%S')  # 返回标准的日期时间格式
    except ValueError:
        return None

def close_mysql():
    cursor.close()
    db.close()
def sql_commit():
    db.commit()
def saveMovie():
    movies_path = os.path.join(base_dir, 'movie.json')
    with open(movies_path, 'r', encoding='utf-8') as f:
        movies = json.loads(f.read())

        # 查询现有电影信息到内存
        cursor.execute("SELECT movie_id, title, rating, director, release_date, production_region, synopsis, poster_url, tags, collection_count FROM movie")
        existing_movies = {row[1]: row for row in cursor.fetchall()}

        insert_data = []
        update_data = []

        for item in movies:
            title = item['title']
            release_date = format_release_date_for_movie(item['release_date'])

            if title in existing_movies:
                existing_record = existing_movies[title]
                # 判断是否需要更新
                if (existing_record[2] != item['rating'] or
                    existing_record[3] != item['director'] or
                    existing_record[4] != release_date or
                    existing_record[5].strip() != item['production_region'].strip() or
                    existing_record[6] != item['synopsis'] or
                    existing_record[7] != item['poster_url'] or
                    existing_record[8] != item['tags'] or
                    existing_record[9] != item['collection_count']):
                    update_data.append((
                        item['rating'], item['director'], release_date,
                        item['production_region'].strip(), item['synopsis'],
                        item['poster_url'], item['tags'], item['collection_count'], existing_record[0]
                    ))
            else:
                # 如果不存在则准备插入
                insert_data.append((
                    title, item['rating'], item['director'], release_date,
                    item['production_region'].strip(), item['synopsis'],
                    item['poster_url'], item['tags'], item['collection_count']
                ))

        # 批量插入和更新
        if insert_data:
            sql_insert = """INSERT INTO movie (title, rating, director, release_date, production_region, synopsis, poster_url, tags, collection_count)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.executemany(sql_insert, insert_data)

        if update_data:
            sql_update = """UPDATE movie SET rating=%s, director=%s, release_date=%s,
                            production_region=%s, synopsis=%s, poster_url=%s, tags=%s, collection_count=%s
                            WHERE movie_id=%s"""
            cursor.executemany(sql_update, update_data)

        sql_commit()
def saveActor():
    actors_path = os.path.join(base_dir, 'actor.json')
    with open(actors_path, 'r', encoding='utf-8') as f:
        actors = json.loads(f.read())

        # 查询现有演员信息到内存
        cursor.execute("SELECT actor_id, actor_name FROM actor")
        existing_actors = {row[1]: row[0] for row in cursor.fetchall()}

        insert_data = []

        for item in actors:
            actor_name = item['actor_name']
            if actor_name not in existing_actors:
                # 如果不存在则准备插入
                insert_data.append((actor_name,))

        # 批量插入
        if insert_data:
            sql_insert = "INSERT INTO actor (actor_name) VALUES (%s)"
            cursor.executemany(sql_insert, insert_data)
            sql_commit()
def saveMovieActor():
    movieActors_path = os.path.join(base_dir, 'movieActor.json')
    with open(movieActors_path, 'r', encoding='utf-8') as f:
        movieActors = json.loads(f.read())

        # 查询现有的电影和演员对应关系到内存
        cursor.execute("SELECT movie_id, actor_id, role FROM movie_actor")
        existing_movie_actor = {(row[0], row[1]): row[2] for row in cursor.fetchall()}

        # 查询所有电影和演员的信息到内存
        cursor.execute("SELECT movie_id, title FROM movie")
        mv2id = {row[1]: row[0] for row in cursor.fetchall()}

        cursor.execute("SELECT actor_id, actor_name FROM actor")
        ac2id = {row[1]: row[0] for row in cursor.fetchall()}

        insert_data = []
        update_data = []

        for item in movieActors:
            movie_id = mv2id.get(item['movie_name'])
            actor_id = ac2id.get(item['actor_name'])

            if movie_id and actor_id:
                key = (movie_id, actor_id)
                if key in existing_movie_actor:
                    # 如果存在，检查是否需要更新
                    if existing_movie_actor[key] != item['role']:
                        update_data.append((item['role'], movie_id, actor_id))
                else:
                    # 如果不存在则准备插入
                    insert_data.append((movie_id, actor_id, item['role']))

        # 批量插入和更新
        if insert_data:
            sql_insert = "INSERT INTO movie_actor (movie_id, actor_id, role) VALUES (%s, %s, %s)"
            cursor.executemany(sql_insert, insert_data)

        if update_data:
            sql_update = "UPDATE movie_actor SET role=%s WHERE movie_id=%s AND actor_id=%s"
            cursor.executemany(sql_update, update_data)

        sql_commit()

def saveCinema():
    cinema_path = os.path.join(base_dir,'cinema.json')

    with open(cinema_path, 'r', encoding='utf-8') as f:
        cinemas = json.loads(f.read())

        # 查询已存在的影院名称
        cursor.execute("SELECT name FROM cinema")
        existing_cinema_names = {row[0] for row in cursor.fetchall()}
        insert_data = []
        for item in cinemas:
            name = item['name']
            if name not in existing_cinema_names:
                insert_data.append((name, item['contact_number'], item['location']))
                existing_cinema_names.add(name)
        if insert_data:
            sql = "INSERT INTO cinema (name, contact_number, location) VALUES (%s, %s, %s)"
            cursor.executemany(sql, insert_data)
            sql_commit()
def saveScreeningRoom():
    screeningRoom_path = os.path.join(base_dir, 'screeningRoom.json')
    with open(screeningRoom_path, 'r', encoding='utf-8') as f:
        screeningRooms = json.loads(f.read())
        # 查询已存在的影院和影厅名称
        cursor.execute("SELECT cinema_id, room_number FROM screeningroom")
        existing_cinema_room_names = {(row[0], row[1]) for row in cursor.fetchall()}
        insert_data = []
        for item in screeningRooms:
            cursor.execute("SELECT cinema_id FROM cinema WHERE name = %s", (item['cinema_name'],))
            cinema_id = cursor.fetchone()

            if cinema_id:
                cinema_room_key = (cinema_id[0], item['room_number'])
                if cinema_room_key not in existing_cinema_room_names:
                    insert_data.append((cinema_id[0], item['room_number'], item['seat_count']))
                    existing_cinema_room_names.add(cinema_room_key)
        if insert_data:
            sql = "INSERT INTO screeningroom (cinema_id,room_number, seat_count) VALUES (%s, %s, %s)"
            cursor.executemany(sql, insert_data)
            sql_commit()
def saveScreening():
    screening_path = os.path.join(base_dir, 'screening.json')
    with open(screening_path, 'r', encoding='utf-8') as f:
        screenings = json.loads(f.read())

        # 删除所有时间小于今天的播放安排
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("DELETE FROM screening WHERE DATE(screening_time) < %s", (today,))
        sql_commit()

        # 查询已存在的放映安排
        cursor.execute("SELECT movie_id, room_id, screening_time FROM screening")
        existing_screenings = {tuple(row) for row in cursor.fetchall()}

        insert_data = []
        for item in screenings:
            # 获取 movie_id
            cursor.execute("SELECT movie_id FROM movie WHERE title = %s", (item['movie_name'],))
            movie_id = cursor.fetchone()
            # 获取 room_id
            cursor.execute("SELECT room_id FROM screeningroom WHERE room_number = %s", (item['room_number'],))
            room_id = cursor.fetchone()

            if movie_id and room_id:
                if item['screening_time'] == 'Unknown Time':
                    continue
                screening_time = format_screening_time_for_screening(item['screening_time'])
                screening_key = (movie_id[0], room_id[0], screening_time)

                if screening_key not in existing_screenings:
                    insert_data.append((movie_id[0], room_id[0], screening_time, item['price']))
                    existing_screenings.add(screening_key)


        if insert_data:
            sql = """INSERT INTO screening (movie_id, room_id, screening_time, price)
                     VALUES (%s, %s, %s, %s)"""
            cursor.executemany(sql, insert_data)
            sql_commit()

def main():
    # saveMovie()
    # print('saveMovie success')
    # saveActor()
    # print('saveActor success')
    # saveMovieActor()
    # print('saveMovieActor success')
    # saveCinema()
    # print('saveCinema success')
    # saveScreeningRoom()
    # print('saveScreeningRoom success')
    saveScreening()
    print('saveScreening success')
    close_mysql()


if __name__ == '__main__':
    main()
