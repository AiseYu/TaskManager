from flask import render_template, request , redirect, url_for
from flask_login import login_user , logout_user , current_user , login_required

from models import Users , Tasks

def register_routes(app, db , bcrypt):
    @app.route('/', methods = ['GET' , 'POST'])
    def index():
        if current_user.is_authenticated:
            tasks = Tasks.query.filter_by(user_id=current_user.uid).all()
            return render_template('index.html', tasks=tasks)
        else:
            return render_template('index.html')

    @app.route('/signup' , methods = ['GET' , 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password)

            user = Users(username = username, password = hashed_password)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))

    @app.route('/login' ,methods = ['GET' , 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = Users.query.filter(Users.username == username).first()
            if user !=None:
                if bcrypt.check_password_hash(user.password , password):
                    login_user(user)
                    return redirect( url_for('index') )

                else:
                    return 'Login Failed'
            else:
                return "No user with this username is found."

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))


    @app.route('/add_task', methods=['GET', 'POST'])
    @login_required
    def add_task():
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            task = Tasks( title= title, description=description, user_id=current_user.uid)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add_task.html')

    @app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
    @login_required
    def edit_task(task_id):
        task = Tasks.query.get_or_404(task_id)
        if task.user_id != current_user.uid:
            abort(403)
        if request.method == 'POST':
            task.title = request.form['title']
            task.description = request.form['description']
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('edit_task.html', task=task)

    @app.route('/delete_task/<int:task_id>', methods=['POST'])
    @login_required
    def delete_task(task_id):
        task = Tasks.query.get_or_404(task_id)
        if task.user_id != current_user.uid:
            abort(403)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))

    

    

    