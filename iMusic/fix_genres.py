import csv
import sqlite3

def fix_genres():
    with sqlite3.connect("iMusic.db") as conn:
        cur = conn.cursor()
        with open('genres.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute("UPDATE Genre SET Name=? WHERE GenreId=?", (row['genre_name'],row['genre_id']))
            conn.commit()


if __name__ == '__main__':
    fix_genres()
