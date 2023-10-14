from flask import Flask, request, redirect, render_template, url_for
import sqlite3

app = Flask(__name__)


# I did not write this function. It is from:
# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-represents-a-number-float-or-int
def is_number(s):
    """
    Check if a string is a number (regardless of it being an int, long, float or complex number)
    :param s: string The string to check if it is a number
    :return: True if string is a number, False otherwise
    """
    try:
        complex(s)
    except ValueError:
        return False
    return True

def is_integer(s):
    """
    Check if a string is an integer
    :param s: string The string to check if it is an integer
    :return: True if string is an integer, False otherwise
    """
    try:
        int(s)
    except ValueError:
        return False
    return True
    
def string_to_int(s):
    """
    Convert a string to an integer
    :param s: string The string to convert to an int
    :return: int The int value of the string
    """
    if is_number(s):
        return int(s)
    else:
        return s

def string_length(s):
    """
    Get the length of a string
    :param s: string The string to get the length of
    :return: int The length of the string
    """
    return len(s)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/statistics/')
def statistics():
    with sqlite3.connect("iMusic.db") as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""SELECT
                            DISTINCT UnitPrice AS Price,
                            COUNT(Track.Name) AS Tracks,
                            COUNT(DISTINCT Album.Title) AS Albums,
                            COUNT(DISTINCT Artist.Name) AS Artists,
                            ROUND(SUM(Milliseconds)/1000, 0) AS Duration,
                            ROUND(UnitPrice*COUNT(Track.Name), 2) AS TotalValue
                        FROM
                            Track LEFT JOIN Album
                            ON Track.AlbumId = Album.AlbumId
                            LEFT JOIN Artist
                            ON Album.ArtistId = Artist.ArtistId
                        GROUP BY
                            UnitPrice
                        ORDER BY UnitPrice ASC;
                        """)
        part1 = cur.fetchall()
        cur.execute(""" SELECT
                            'Total' AS Price,
                            COUNT(Track.Name) AS Tracks,
                            COUNT(DISTINCT Album.Title) AS Albums,
                            COUNT(DISTINCT Artist.Name) AS Artists,
                            ROUND(SUM(Milliseconds)/1000, 0) AS Duration,
                            ROUND(SUM(UnitPrice), 2) AS TotalValue
                        FROM
                            Track LEFT JOIN Album
                            ON Track.AlbumId = Album.AlbumId
                            LEFT JOIN Artist
                            ON Album.ArtistId = Artist.ArtistId;
                        """)
        part2 = cur.fetchall()
        prices = part1+part2

    return render_template('statistics.html', prices = prices)


@app.route('/add/')
def add_get():
    # Create form
    with sqlite3.connect("iMusic.db") as conn:
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(""" SELECT AlbumId, Title
                            FROM Album
                            ORDER BY Title ASC;
                            """)
            albums = cur.fetchall()
            cur.execute(""" SELECT GenreId, Name
                            FROM Genre
                            ORDER BY Name ASC;
                            """)
            genres = cur.fetchall()
        except:
            return render_template('error.html')

    return render_template("add_track.html", albums=albums, genres=genres)


@app.route('/add/track', methods = ['POST'])
def add_post():
    if request.method == 'POST':
        Name = request.form.get('track_name')
        AlbumId = request.form.get('track_album')
        GenreId = request.form.get('track_genre')
        Composer = request.form.get('track_composer')
        Duration = request.form.get('track_duration')
        Price = request.form.get('track_price')
        
    # Check data validation
    messages = []
    with sqlite3.connect("iMusic.db") as conn:
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT AlbumId FROM Album;")
            AlbumId_list = cur.fetchall()
            cur.execute("SELECT DISTINCT GenreId FROM Genre;")
            GenreId_list = cur.fetchall()
        except:
            return render_template('error.html')

    try:
        if Name=='' or Name==None:
            messages.append("Track name is empty")
        elif string_length(Name) > 200:
            messages.append("Track name is too long")

        if AlbumId=='' or AlbumId==None or (not is_integer(AlbumId)):
            messages.append("Album ID is invalid")
        else:
            if_exist = 0
            for i in AlbumId_list:
                if i[0] == string_to_int(AlbumId):
                    if_exist = 1
                    break
            if if_exist == 0:
                messages.append("Album does not exist")

        if GenreId=='' or GenreId==None or (not is_integer(GenreId)):
            messages.append("Genre ID is invalid")
        else:
            if_exist = 0
            for i in GenreId_list:
                if i[0] == string_to_int(GenreId):
                    if_exist = 1
                    break
            if if_exist == 0:
                messages.append("Genre does not exist")

        if string_length(Composer) > 220:
            messages.append("Composer name is too long")

        if Duration=='' or Duration==None or (not is_number(Duration)):
            messages.append("Duration is invalid")
        else:
            Duration = float(Duration)
            Duration = int(Duration)*1000
            if Duration <= 0:
                messages.append("Duration must be a positive number")

        if Price=='' or Price==None or (not is_number(Price)):
            messages.append("Price is invalid")
        else:
            Price = float(Price)
            if Price<=0.00 or Price>10.00:
                messages.append("Price must be more than zero and less than or equal to 10")
    except:
        return render_template('error.html')

    # Insert new data
    if messages == []:
        with sqlite3.connect("iMusic.db") as conn:
            try:
                cur = conn.cursor()
                cur.execute("""INSERT INTO Track (Name, AlbumId, GenreId, Composer, Milliseconds, UnitPrice)
                                VALUES (?,?,?,?,?,?);""", (Name, AlbumId, GenreId, Composer, Duration, Price))
                # We do not need to update Artist, because the relationship between Artist
                # and Album is 1:M. Since we cannot add album, the artist will not change.
                conn.commit()
            except:
                return render_template('error.html')
        return redirect(url_for('index'))
    else:
        return render_template('error.html', messages=messages)


# You do not need to modify this function (list_album)
@app.route('/album/')
@app.route('/album/<album_id>')
def list_album(album_id=None):
    return render_template('error.html', messages=["Album listing is not implemented yet. Another developer is working on it."])

# === Do not modify or add code after this line ===
def main():
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()
