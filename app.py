from flask import Flask, render_template, request, redirect, url_for, session
from db_connect import get_db_connection
import bcrypt
from Encryption import encrypt_vote, decrypt_vote

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        voter_id = request.form["voter_id"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE voter_id=?", (voter_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_password = user[3]

            if bcrypt.checkpw(password.encode(), stored_password.encode()):
                session["user"] = voter_id
                return redirect(url_for("vote"))

        return "Invalid Login ❌"

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        voter_id = request.form["voter_id"]
        password = request.form["password"]

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO Users(name, voter_id, password) VALUES (?, ?, ?)",
                (name, voter_id, hashed)
            )
            conn.commit()
            conn.close()

            return "✅ Registered Successfully! <a href='/'>Login</a>"

        except:
            conn.close()
            return "❌ Voter ID already exists!"

    return render_template("register.html")


# ---------------- VOTE ----------------
@app.route("/vote", methods=["GET", "POST"])
def vote():

    if "user" not in session:
        return redirect("/")

    voter_id = session["user"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # check if already voted
    cursor.execute("SELECT has_voted FROM Users WHERE voter_id=?", (voter_id,))
    result = cursor.fetchone()

    if result[0] == 1:
        conn.close()
        return "❌ You have already voted!"

    if request.method == "POST":
        candidate = request.form["candidate"]

        # 🔐 Encrypt vote
        encrypted = encrypt_vote(candidate)

        # ✅ FIXED: removed voter_id (maintains anonymity)
        cursor.execute(
            "INSERT INTO Votes(encrypted_vote) VALUES (?)",
            (encrypted,)
        )

        # mark as voted
        cursor.execute(
            "UPDATE Users SET has_voted=1 WHERE voter_id=?",
            (voter_id,)
        )

        conn.commit()
        conn.close()

        return "✅ Vote submitted securely!"

    conn.close()
    return render_template("vote.html")


# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ FIXED: fetch hashed password only
        cursor.execute(
            "SELECT password FROM Admin WHERE username=?",
            (username,)
        )

        admin = cursor.fetchone()
        conn.close()

        if admin and bcrypt.checkpw(password.encode(), admin[0].encode()):
            session["admin"] = username
            return redirect(url_for("results"))

        return "Invalid Admin Login ❌"

    return render_template("admin.html")


# ---------------- RESULTS ----------------
@app.route("/results")
def results():

    if "admin" not in session:
        return "❌ Access Denied"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT encrypted_vote FROM Votes")
    votes = cursor.fetchall()

    # 🔓 decrypt votes
    decrypted_votes = [decrypt_vote(v[0]) for v in votes]

    # count votes
    results = {}
    for vote in decrypted_votes:
        results[vote] = results.get(vote, 0) + 1

    conn.close()

    return render_template("results.html", results=results.items())


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)