import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = '1234'  # Change this to a random secret key

# Database connection parameters
DB_USER = 'manu'
DB_PASSWORD = 'R0I6hkqUDpEc6KCm6De3vw'
DB_HOST = 'paper-orca-8106.8nk.cockroachlabs.cloud'
DB_PORT = '26257'
DB_NAME = 'defaultdb'

def create_connection():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/Main.html')
def main_page():
    return render_template('Main.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Insert user data into the users and signup tables
                    cursor.execute("INSERT INTO public.users (username, password) VALUES (%s, %s) RETURNING user_id;", (username, password))
                    user_id = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO public.signup (user_id, username, new_password, email) VALUES (%s, %s, %s, %s);", (user_id, username, password, email))
                    connection.commit()
                    flash('Registration successful! You can now log in.', 'success')
                    return redirect(url_for('main_page'))
            except Exception as e:
                connection.rollback()
                flash(f'Registration failed. Error: {e}', 'error')
            finally:
                connection.close()

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Check if the user exists in the database
                cursor.execute("SELECT user_id FROM public.users WHERE username = %s AND password = %s;", (username, password))
                user_id = cursor.fetchone()
                
                if user_id:
                    flash('Login successful!', 'success')
                    return redirect(url_for('main_page'))  # Redirect to 'main_page'
                else:
                    flash('Login failed. Please check your credentials.', 'error')
            except Exception as e:
                flash(f'Login failed. Error: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
