from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock tenants with users
db_tenants = {
    "tenant1": {"users": {"student": {"password": "student123", "role": "student"},
                          "teacher": {"password": "teacher123", "role": "teacher"}}},
    "tenant2": {"users": {"student": {"password": "student456", "role": "student"},
                          "teacher": {"password": "teacher456", "role": "teacher"}}}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tenant = request.form['tenant']
        username = request.form['username']
        password = request.form['password']

        tenant_data = db_tenants.get(tenant)
        if tenant_data:
            user = tenant_data['users'].get(username)
            if user and user['password'] == password:
                session['tenant'] = tenant
                session['username'] = username
                session['role'] = user['role']
                return redirect(url_for('dashboard'))
        return "Invalid credentials"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    tenant = session.get('tenant')
    role = session.get('role')
    if tenant and role:
        if role == 'student':
            return render_template('student_dashboard.html', tenant=tenant, user=session['username'])
        elif role == 'teacher':
            return render_template('teacher_dashboard.html', tenant=tenant, user=session['username'])
        else:
            return "Unauthorized access"
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
