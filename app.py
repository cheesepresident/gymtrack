from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import sirope
import classes
import redis

def create_app():
    lmanager = LoginManager()
    fapp = Flask(__name__)
    srp = sirope.Sirope()
    fapp.secret_key = "1e44b3a45067431da85bfe4259f5a15e"
    lmanager.init_app(fapp)
    return fapp, lmanager, srp

app, lm, srp = create_app()

@lm.user_loader
def user_loader(username):
    return classes.User.find(srp, username)

@lm.unauthorized_handler
def unauthorized_handler():
    flash("Unauthorized")
    return redirect("/login")



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username_txt = request.form.get('uname')
        password_txt = request.form.get('psw')

        if not username_txt or not password_txt:
            flash("No field entry")
            return redirect("/login")

        usr = classes.User.find(srp, username_txt)

        if not usr:
            flash("Account doesn't exist")
            return redirect("/login")
        else:
            login_user(usr)

        if current_user.is_authenticated:
            return redirect("/log")

    return render_template("login.html")

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username_txt = request.form.get('uname')
        password_txt = request.form.get('psw')

        if not username_txt or not password_txt:
            flash("No field entry")
            return redirect("/register")

        usr = classes.User.find(srp, username_txt)

        if not usr:
            usr = classes.User(username_txt, password_txt)
            srp.save(usr)
            login_user(usr)
        else:
            flash("Account with this username already exists")
            return redirect("/register")
        
        if current_user.is_authenticated:
            return redirect("/log")


    return render_template("register.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect('/login')

@app.route('/log', methods=["POST", "GET"])
@login_required
def log():
    if request.method == "POST":
        exercise_txt = request.form.get('exercise')
        amount_txt = request.form.get('amount')
        unit_txt = request.form.get('unit')
        weight_txt = request.form.get('weight')
        notes_txt = request.form.get('notes')

        if not exercise_txt:
                flash("Exercise field required")
                return redirect("/log")

        workout = classes.Workout(exercise_txt, amount_txt, unit_txt, weight_txt, notes_txt)
        #test username
        print(f"current user: {current_user.get_id()}")
        srp.save(workout)

    return render_template("log.html")

@app.route('/history')
@login_required
def history():
    ...
    return render_template("history.html")

@app.route("/api/workouts")
@login_required
def api_get_workouts():
    current_username = current_user.get_id()
    all_workouts = srp.load_all(classes.Workout)
    user_workouts = [
        {
            "date": f"{w.year} {w.month} {w.day:02d}",
            "exercise": w.exercise,
            "amount": w.amount,
            "unit": w.unit,
            "weight": w.weight,
            "notes": w.notes
        }
        for w in all_workouts if w.username == current_username
    ]
    for w in srp.load_all(classes.Workout):
        print(f"username:{w.username}, exercise:{w.exercise}")
    return jsonify(user_workouts)

if __name__ == "__main__":
    
    app.run(debug=True)