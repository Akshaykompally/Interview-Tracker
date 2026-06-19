from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from collections import Counter

app = Flask(__name__)

# ---------------- SECRET KEY ----------------
app.secret_key = "random_secret_key"

# ---------------- MYSQL CONFIG ----------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@kshay03sep2004'
app.config['MYSQL_DB'] = 'authentication'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# ---------------- LOGIN MANAGER ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'


# ---------------- USER MODEL ----------------
class User(UserMixin):

    def __init__(self, user_id, full_name, user_email, user_password):
        self.id = user_id
        self.full_name = full_name
        self.email = user_email
        self.password = user_password

    @staticmethod
    def get(user_id):

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT user_id, full_name, user_email, user_password
            FROM login_credits
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:
            return User(
                user[0],
                user[1],
                user[2],
                user[3]
            )

        return None


# ---------------- LOAD USER ----------------
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('Main.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login_page():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':

        user_email = request.form['email']
        user_password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT user_id, full_name, user_email, user_password
            FROM login_credits
            WHERE user_email = %s
            """,
            (user_email,)
        )

        user_data = cursor.fetchone()
        cursor.close()

        if user_data:

            stored_password = user_data[3]

            if bcrypt.check_password_hash(
                stored_password,
                user_password
            ):

                user = User(
                    user_data[0],
                    user_data[1],
                    user_data[2],
                    user_data[3]
                )

                login_user(user)

                flash("Login successful!", "success")

                return redirect(url_for('dashboard'))

        flash("Invalid email or password", "danger")

    return render_template('Login.html')


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup_page():

    if request.method == 'POST':

        full_name = request.form['fname']
        user_email = request.form['email']
        user_password = request.form['password']

        cursor = mysql.connection.cursor()

        # CHECK EXISTING EMAIL
        cursor.execute(
            "SELECT * FROM login_credits WHERE user_email = %s",
            (user_email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already exists!", "warning")
            cursor.close()
            return redirect(url_for('signup_page'))

        hashed_password = bcrypt.generate_password_hash(
            user_password
        ).decode('utf-8')

        cursor.execute(
            """
            INSERT INTO login_credits
            (full_name, user_email, user_password)
            VALUES (%s, %s, %s)
            """,
            (
                full_name,
                user_email,
                hashed_password
            )
        )

        mysql.connection.commit()
        cursor.close()

        flash("Account created successfully!", "success")

        return redirect(url_for('login_page'))

    return render_template('Register.html')


# ---------------- ADD INTERVIEW ----------------
@app.route('/add_interview', methods=['GET', 'POST'])
@login_required
def add_interview():

    if request.method == 'POST':

        company_name = request.form['company-name']
        applied_role = request.form['role']
        date_attended = request.form['date']
        status_of_interview = request.form['status']

        rounds = request.form.getlist('choice')

        no_of_rounds_attended = ", ".join(rounds)

        notes = request.form['notes']

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO interview_details
            (
                company_name,
                applied_role,
                date_attended,
                status_of_interview,
                no_of_rounds_attended,
                fingure_it_out
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                company_name,
                applied_role,
                date_attended,
                status_of_interview,
                no_of_rounds_attended,
                notes
            )
        )

        mysql.connection.commit()
        cursor.close()

        flash("Interview added successfully!", "success")

        return redirect(url_for('dashboard'))

    return render_template('add.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
@login_required
def dashboard():

    cursor = mysql.connection.cursor()

    # GET ALL INTERVIEWS
    cursor.execute("SELECT * FROM interview_details")

    result = cursor.fetchall()

    # PIE CHART DATA
    cursor.execute(
        """
        SELECT status_of_interview, COUNT(*)
        FROM interview_details
        GROUP BY status_of_interview
        """
    )

    values_count = cursor.fetchall()

    cursor.close()

    # CHART LABELS
    labels = [row[0] for row in values_count]

    # CHART DATA
    data = [row[1] for row in values_count]

    # TOTAL INTERVIEWS
    n_interviews = sum(data)

    # STATUS COUNTS
    accept = 0
    reject = 0
    pending = 0

    for row in values_count:

        status = row[0]
        count = row[1]

        if status == "Accepted":
            accept = count

        elif status == "Rejected":
            reject = count

        elif status == "Pending":
            pending = count

    # BAR GRAPH DATA
    rounds_list = []

    for row in result:

        if len(row) > 5 and row[5]:

            rounds = row[5].split(',')

            rounds_list.extend(rounds)

    round_counts = Counter(rounds_list)

    round_labels = list(round_counts.keys())

    round_data = list(round_counts.values())

    return render_template(
        "MenuBar.html",
        result=result,
        labels=labels,
        data=data,
        round_labels=round_labels,
        round_data=round_data,
        n_interviews=n_interviews,
        accept=accept,
        reject=reject,
        pending=pending
    )


# ---------------- COMPANY HISTORY ----------------
@app.route('/Company_History')
@login_required
def company_history():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM interview_details")

    result = cursor.fetchall()

    cursor.close()

    return render_template(
        "History.html",
        result=result
    )


# ---------------- DELETE INTERVIEW ----------------
@app.route('/delete/<int:id>')
@login_required
def delete_interview(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM interview_details WHERE id = %s",
        (id,)
    )

    mysql.connection.commit()
    cursor.close()

    flash("Interview deleted successfully!", "success")

    return redirect(url_for('dashboard'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash("Logged out successfully!", "info")

    return redirect(url_for('login_page'))


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)