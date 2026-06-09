from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB = "foodwaste.db"


def init_db():
    conn = sqlite3.connect("foodwaste.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS donations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor TEXT,
        food_name TEXT,
        quantity TEXT,
        location TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route('/')
def home():

    conn = sqlite3.connect("foodwaste.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM donations")

    donations = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        donations=donations
    )


@app.route('/add', methods=['POST'])
def add():

    donor = request.form['donor']
    food_name = request.form['food_name']
    quantity = request.form['quantity']
    location = request.form['location']

    conn = sqlite3.connect("foodwaste.db")
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO donations
        (donor, food_name, quantity, location, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            donor,
            food_name,
            quantity,
            location,
            "Available"
        )
    )

    conn.commit()
    conn.close()

    return redirect(url_for('home'))


@app.route('/accept/<int:id>')
def accept(id):

    conn = sqlite3.connect("foodwaste.db")
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE donations
        SET status='Accepted'
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('home'))
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("foodwaste.db")
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM donations
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

if __name__ == "__main__":

    init_db()

    app.run(debug=True)