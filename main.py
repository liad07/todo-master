from flask import Flask, request, redirect, session, url_for
import pyodbc
import struct

app = Flask(__name__)
app.secret_key="somekey"
# Replace 'your_database_file_path' with the actual path to your Access database file

def calculate_project_budget(muchforhour,numofhour,difficulty, clientdurak):


    return muchforhour*numofhour+difficulty*50+clientdurak*10


# Function to connect to the database
def connect_to_database():
    try:
        # Replace 'your_database_file_path' with the actual path to your Access database file
        DATABASE_PATH = r'path here '

        conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DATABASE_PATH+''
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()
        print("Connected to the database successfully!")
        return connection, cursor
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        return None, None

# Function to create a new task in the "Tasks" table
def create_task(user_id, title, description, priority, status, due_date):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Prepare the SQL query with parameter
            sql = "INSERT INTO Tasks (UserID, Title, Description, Priority, Status, DueDate) VALUES (?, ?, ?, ?, ?, ?)"
            values = (user_id, title, description, priority, status, due_date)

            # Execute the query with the provided values
            cursor.execute(sql, values)
            connection.commit()
            print("Task created successfully!")
            sql = "SELECT * FROM Tasks WHERE UserID=?"

            # Execute the query with the provided value
            cursor.execute(sql, (user_id,))
            tasks = cursor.fetchall()
            return len(cursor.fetchall())
        else:
            print("Unable to connect to the database.")
    except pyodbc.Error as e:
        print(f"Error creating task: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to read all tasks for a specific user from the "Tasks" table
def read_user_tasks(user_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Prepare the SQL query with parameters
            sql = "SELECT * FROM Tasks WHERE UserID=?"

            # Execute the query with the provided value
            cursor.execute(sql, (user_id,))
            tasks = cursor.fetchall()
            print("User Tasks:")
            for task in tasks:
                print(task)
        else:
            print("Unable to connect to the database.")
    except pyodbc.Error as e:
        print(f"Error reading user tasks: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to update an existing task in the "Tasks" table
def update_task(task_id, title, description, priority, status, due_date):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Prepare the SQL query with parameters
            sql = "UPDATE Tasks SET Title=?, Description=?, Priority=?, Status=?, DueDate=? WHERE TaskID=?"
            values = (title, description, priority, status, due_date, task_id)

            # Execute the query with the provided values
            cursor.execute(sql, values)
            connection.commit()
            print("Task updated successfully!")
        else:
            print("Unable to connect to the database.")
    except pyodbc.Error as e:
        print(f"Error updating task: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to delete a task from the "Tasks" table
def delete_task(task_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Prepare the SQL query with parameters
            sql = "DELETE FROM Tasks WHERE TaskID=?"

            # Execute the query with the provided value
            cursor.execute(sql, (task_id,))
            connection.commit()
            print("Task deleted successfully!")
        else:
            print("Unable to connect to the database.")
    except pyodbc.Error as e:
        print(f"Error deleting task: {e}")
    finally:
        cursor.close()
        connection.close()



# Function to check if a user exists in the database and validate the login credentials
def validate_user_login(username, password):
    connection, cursor = connect_to_database()
    if connection:
        # Prepare the SQL query with parameters
        sql = "SELECT * FROM Users WHERE Username=? AND Password=?"
        values = (username, password)

        # Execute the query with the provided values
        cursor.execute(sql, values)
        user = cursor.fetchone()

        if user:
            return str(user[0])
    return None
# Function to insert a new user into the "Users" table
def insert_user(username, password, email):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Prepare the SQL query with parameters
            sql = "INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)"
            values = (username, password, email)

            # Execute the query with the provided values
            cursor.execute(sql, values)
            connection.commit()
            print("User registered successfully!")
        else:
            print("Unable to connect to the database.")
    except pyodbc.Error as e:
        print(f"Error registering user: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to update a task in the database
def update_task_in_database(task_id, title, description, priority, status, due_date):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Prepare the SQL query with parameters
            sql = "UPDATE Tasks SET Title=?, Description=?, Priority=?, Status=?, DueDate=? WHERE TaskID=? AND UserID=?"
            values = (title, description, priority, status, due_date, task_id, session.get('user_id'))

            # Execute the query with the provided values
            cursor.execute(sql, values)
            connection.commit()
            print("Task updated successfully!")
        else:
            print("Unable to connect to the database.")
    except pyodbc.Error as e:
        print(f"Error updating task: {e}")
    finally:
        cursor.close()
        connection.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_id = validate_user_login(username, password)

        if user_id:
            # Store the user ID in the session to indicate successful login
            session['user_id'] = user_id
            return redirect(url_for('index'))
        else:
            # Display an error message for invalid credentials
            error_message = "Invalid username or password. Please try again."
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Login</title>
                <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
            </head>
            <body>
                <div class="container">
                    <h1>Login</h1>
                    <p style="color: red;">{error_message}</p>
                    <form method="post">
                        <input type="text" name="username" placeholder="Username" required>
                        <input type="password" name="password" placeholder="Password" required>
                        <button type="submit">Login</button>
                    </form>
                    <p>Don't have an account? <a href="{url_for('register')}">Register here</a>.</p>
                </div>
            </body>
            </html>
            """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
    </head>
    <body>
        <div class="container">
            <h1>Login</h1>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <p>Don't have an account? <a href="{url_for('register')}">Register here</a>.</p>
        </div>
    </body>
    </html>
    """

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve user registration data from the form
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Insert the new user into the database
        insert_user(username, password, email)  # Implement this function to insert a new user into the database

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register</title>
        <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
    </head>
    <body>
        <div class="container">
            <h1>Register</h1>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <input type="email" name="email" placeholder="Email" required>
                <button type="submit">Register</button>
            </form>
            <p>Already have an account? <a href="{url_for('login')}">Login here</a>.</p>
        </div>
    </body>
    </html>
    """

@app.route('/')
def index():
    user_id = session.get('user_id')

    if user_id:
        # Retrieve the username of the logged-in user
        connection, cursor = connect_to_database()
        if connection:
            sql = "SELECT Username FROM Users WHERE UserID=?"
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()

            if user:
                username = user[0]

                # Retrieve user tasks from the database
                sql = "SELECT * FROM Tasks WHERE UserID=? ORDER BY DueDate ASC"
                cursor.execute(sql, (user_id,))
                tasks = cursor.fetchall()

                # Generate HTML for the task list with links to task detail pages
                task_list = ""
                for task in tasks:
                    task_list += f"""
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">{task[1]}</h5>
                            <p class="card-text">Due Date: {task[5]}</p>
                            <a href="{url_for('task_details', task_id=task[0])}" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                    """

                return '''  <script>
        // Function to set the preferred color mode and store it in a cookie
        function setColorMode(colorMode) {
            document.cookie = `colorMode=${colorMode};path=/;max-age=31536000`; // Cookie expires in one year
            applyColorMode(colorMode);
        }

        // Function to apply the preferred color mode
        function applyColorMode(colorMode) {
            if (colorMode === 'dark') {
                // Apply dark mode styles
                document.body.classList.add('dark-mode');
            } else {
                // Apply white mode styles
                document.body.classList.remove('dark-mode');
            }
        }

        // Function to load the preferred color mode from the cookie when the page loads
        function loadColorMode() {
            const colorMode = document.cookie.replace(/(?:(?:^|.*;\s*)colorMode\s*\=\s*([^;]*).*$)|^.*$/, "$1");
            applyColorMode(colorMode);
        }

        // Load the preferred color mode when the page loads
        window.addEventListener('load', loadColorMode);
    </script>'''+f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Todo Master</title>
                    <link rel="stylesheet" href="{url_for('static', filename='css/bootstrap.min.css')}">
                    <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
                </head>
                <body>
                    <nav class="navbar navbar-dark bg-dark">
                        <div class="container">
                            <a class="navbar-brand" href="/">TodoMaster</a>
                            <div class="navbar-nav ml-auto">
                            <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('white')">White Mode</a>
            <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('dark')">Dark Mode</a>
                                <span class="navbar-text">Hello, {username}!</span>
                                <a class="nav-link" href="{url_for('logout')}">Logout</a>
                                <a class="nav-link" href="{url_for('new_task')}">New Task</a>
                            </div>
                        </div>
                    </nav>

                    <div class="container mt-5">
                        <div class="jumbotron text-center">
                            <h1 class="display-4">Welcome to Todo Master</h1>
                            <p class="lead">TodoMaster is a powerful task management web application that allows users to organize their tasks efficiently. With TodoMaster, users can create, edit, prioritize, and track their tasks, ensuring nothing falls through the cracks.</p>
                            <hr class="my-4">
                            <div class="task-list">
                                {task_list}
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                """

    # If the user is not logged in, show the default index page
    return '''  <script>
        // Function to set the preferred color mode and store it in a cookie
        function setColorMode(colorMode) {
            document.cookie = `colorMode=${colorMode};path=/;max-age=31536000`; // Cookie expires in one year
            applyColorMode(colorMode);
        }

        // Function to apply the preferred color mode
        function applyColorMode(colorMode) {
            if (colorMode === 'dark') {
                // Apply dark mode styles
                document.body.classList.add('dark-mode');
            } else {
                // Apply white mode styles
                document.body.classList.remove('dark-mode');
            }
        }

        // Function to load the preferred color mode from the cookie when the page loads
        function loadColorMode() {
            const colorMode = document.cookie.replace(/(?:(?:^|.*;\s*)colorMode\s*\=\s*([^;]*).*$)|^.*$/, "$1");
            applyColorMode(colorMode);
        }

        // Load the preferred color mode when the page loads
        window.addEventListener('load', loadColorMode);
    </script>'''+f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo Master</title>
        <link rel="stylesheet" href="{url_for('static', filename='css/bootstrap.min.css')}">
        <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">TodoMaster</a>
                <div class="navbar-nav ml-auto">
                <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('white')">White Mode</a>
            <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('dark')">Dark Mode</a>
                    <a class="nav-link" href="{url_for('login')}">Login</a>
                    <a class="nav-link" href="{url_for('register')}">Register</a>
                </div>
            </div>
        </nav>

        <div class="container mt-5">
            <div class="jumbotron text-center">
                <h1 class="display-4">Welcome to Todo Master</h1>
                <p class="lead">Here, you can manage your tasks efficiently with our awesome To-Do App. Stay organized and focused on what matters!</p>
                <hr class="my-4">
                <p>Key features of our app include:</p>
                <ul class="list-unstyled">
                    <li>Create, update, and delete tasks.</li>
                    <li>Set task priorities and due dates.</li>
                    <li>Categorize tasks for better organization.</li>
                    <li>Tag tasks for easier identification.</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """




@app.route('/logout')
def logout():
    # Clear the user_id from the session to indicate logout
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/new_task', methods=['GET', 'POST'])
def new_task():
    user_id = session.get('user_id')

    if user_id:
        if request.method == 'POST':
            # Retrieve task details from the form
            title = request.form.get('title')
            description = request.form.get('description')
            priority = request.form.get('priority')
            status = request.form.get('status')
            due_date = request.form.get('due_date')

            # Insert the new task into the database
            task_id = create_task(user_id, title, description, priority, status, due_date)

            # Redirect to the index page after successful task creation
            return redirect(url_for('task_details', task_id=task_id))

        # Show the form to create a new task
        return '''  <script>
        // Function to set the preferred color mode and store it in a cookie
        function setColorMode(colorMode) {
            document.cookie = `colorMode=${colorMode};path=/;max-age=31536000`; // Cookie expires in one year
            applyColorMode(colorMode);
        }

        // Function to apply the preferred color mode
        function applyColorMode(colorMode) {
            if (colorMode === 'dark') {
                // Apply dark mode styles
                document.body.classList.add('dark-mode');
            } else {
                // Apply white mode styles
                document.body.classList.remove('dark-mode');
            }
        }

        // Function to load the preferred color mode from the cookie when the page loads
        function loadColorMode() {
            const colorMode = document.cookie.replace(/(?:(?:^|.*;\s*)colorMode\s*\=\s*([^;]*).*$)|^.*$/, "$1");
            applyColorMode(colorMode);
        }

        // Load the preferred color mode when the page loads
        window.addEventListener('load', loadColorMode);
    </script>'''+f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Create New Task</title>
            <link rel="stylesheet" href="{url_for('static', filename='css/bootstrap.min.css')}">
            <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
        </head>
        <body>
            <nav class="navbar navbar-dark bg-dark">
                <div class="container">
                    <a class="navbar-brand" href="/">TodoMaster</a>
                    <div class="navbar-nav ml-auto">
                    <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('white')">White Mode</a>
            <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('dark')">Dark Mode</a>
                        <a class="nav-link" href="{url_for('logout')}">Logout</a>
                    </div>
                </div>
            </nav>

            <div class="container mt-5">
                <div class="jumbotron text-center">
                    <h1>Create New Task</h1>
                    <form method="post">
                        <div class="form-group">
                            <label for="title">Title:</label>
                            <input type="text" class="form-control" id="title" name="title" required>
                        </div>
                        <div class="form-group">
                            <label for="description">Description:</label>
                            <textarea class="form-control" id="description" name="description" rows="3"></textarea>
                        </div>
                        <div class="form-group">
                            <label for="priority">Priority:</label>
                            <select class="form-control" id="priority" name="priority" required>
                                <option value="High">High</option>
                                <option value="Medium">Medium</option>
                                <option value="Low">Low</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="status">Status:</label>
                            <select class="form-control" id="status" name="status" required>
                                <option value="Pending">Pending</option>
                                <option value="In Progress">In Progress</option>
                                <option value="Completed">Completed</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="due_date">Due Date:</label>
                            <input type="date" class="form-control" id="due_date" name="due_date" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Create Task</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))


@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
def task_details(task_id):
    user_id = session.get('user_id')

    if user_id:
        # Check if the user owns the task
        connection, cursor = connect_to_database()
        if connection:
            sql = "SELECT UserID FROM Tasks WHERE TaskID=?"
            cursor.execute(sql, (task_id,))
            task_owner = cursor.fetchone()

            if task_owner and str(task_owner[0]) == str(user_id):


                # Retrieve the current task details to pre-fill the form
                sql = "SELECT * FROM Tasks WHERE TaskID=? AND UserID=?"
                cursor.execute(sql, (task_id, user_id))
                task = cursor.fetchone()

                if task:
                    sql1 = "SELECT Price FROM Tasks WHERE TaskID=?"
                    cursor.execute(sql1, task_id)
                    x=cursor.fetchone()
                    if request.method == 'POST' or x[0]:
                        # Retrieve task details from the form
                        if x[0]:
                            price=x[0]
                        else:
                            muchforhour = float(request.form.get('muchforhour'))
                            numofhour = int(request.form.get('numofhour'))
                            difficulty = int(request.form.get('difficulty'))
                            clientdurak = int(request.form.get('clientdurak'))

                            # Perform the calculation to get the project budget
                            price = calculate_project_budget(muchforhour, numofhour, difficulty, clientdurak)

                            # You can store the calculated price in the database if needed
                            # Update the 'Tasks' table with the calculated 'price' for the specific task_id
                            sql = "UPDATE Tasks SET Price=? WHERE TaskID=?"
                            cursor.execute(sql, (price, task_id))
                            connection.commit()

                        # Display the calculated price to the user
                        return  '''  <script>
        // Function to set the preferred color mode and store it in a cookie
        function setColorMode(colorMode) {
            document.cookie = `colorMode=${colorMode};path=/;max-age=31536000`; // Cookie expires in one year
            applyColorMode(colorMode);
        }

        // Function to apply the preferred color mode
        function applyColorMode(colorMode) {
            if (colorMode === 'dark') {
                // Apply dark mode styles
                document.body.classList.add('dark-mode');
            } else {
                // Apply white mode styles
                document.body.classList.remove('dark-mode');
            }
        }

        // Function to load the preferred color mode from the cookie when the page loads
        function loadColorMode() {
            const colorMode = document.cookie.replace(/(?:(?:^|.*;\s*)colorMode\s*\=\s*([^;]*).*$)|^.*$/, "$1");
            applyColorMode(colorMode);
        }

        // Load the preferred color mode when the page loads
        window.addEventListener('load', loadColorMode);
    </script>'''+f'''
                                       <!DOCTYPE html>
                                       <html>
                                       <head>
                                           <title>Task Details</title>
                                           <link rel="stylesheet" href="{url_for('static', filename='css/bootstrap.min.css')}">
                                           <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
                                       </head>
                                       <body>
                                           <nav class="navbar navbar-dark bg-dark">
                                               <div class="container">
                                                   <a class="navbar-brand" href="/">TodoMaster</a>
                                                   <div class="navbar-nav ml-auto">
                                                       <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('white')">White Mode</a>
                                                       <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('dark')">Dark Mode</a>
                                                       <a class="nav-link" href="{url_for('logout')}">Logout</a>
                                                   </div>
                                               </div>
                                           </nav>

                                           <div class="container mt-5">
                                                                                               <div class="jumbotron">

                                               <h1>Task Details</h1>
                                               <p>Title: {task[1]}</p>
                                               <p>Description: {task[2]}</p>
                                               <p>Due Date: {task[5]}</p>
                                               <p>Status: {task[4]}</p>
                                               <!-- Display other task details as needed -->
                                               <h2>Calculate Project Budget</h2>
                                       Calculated Project Budget: {price}
                                                                                      </div>
'''

                    # Generate HTML for the task details and the form to calculate project budget
                    task_details_html = '''  <script>
        // Function to set the preferred color mode and store it in a cookie
        function setColorMode(colorMode) {
            document.cookie = `colorMode=${colorMode};path=/;max-age=31536000`; // Cookie expires in one year
            applyColorMode(colorMode);
        }

        // Function to apply the preferred color mode
        function applyColorMode(colorMode) {
            if (colorMode === 'dark') {
                // Apply dark mode styles
                document.body.classList.add('dark-mode');
            } else {
                // Apply white mode styles
                document.body.classList.remove('dark-mode');
            }
        }

        // Function to load the preferred color mode from the cookie when the page loads
        function loadColorMode() {
            const colorMode = document.cookie.replace(/(?:(?:^|.*;\s*)colorMode\s*\=\s*([^;]*).*$)|^.*$/, "$1");
            applyColorMode(colorMode);
        }

        // Load the preferred color mode when the page loads
        window.addEventListener('load', loadColorMode);
    </script>'''+ f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Task Details</title>
                        <link rel="stylesheet" href="{url_for('static', filename='css/bootstrap.min.css')}">
                        <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
                    </head>
                    <body>
                        <nav class="navbar navbar-dark bg-dark">
                            <div class="container">
                                <a class="navbar-brand" href="/">TodoMaster</a>
                                <div class="navbar-nav ml-auto">
                                    <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('white')">White Mode</a>
                                    <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('dark')">Dark Mode</a>
                                    <a class="nav-link" href="{url_for('logout')}">Logout</a>
                                </div>
                            </div>
                        </nav>

                        <div class="container mt-5">
                                                    <div class="jumbotron">

                            <h1>Task Details</h1>
                            <p>Title: {task[1]}</p>
                            <p>Description: {task[2]}</p>
                            <p>Due Date: {task[5]}</p>
                            <p>Status: {task[4]}</p>
                                                    </div>

                            <!-- Display other task details as needed -->
                            <h2>Calculate Project Budget</h2>
                            <form method="post">
                                <div class="form-group">
                                    <label for="muchforhour">Hourly Rate:</label>
                                    <input type="number" class="form-control" id="muchforhour" name="muchforhour" step="0.01" required>
                                </div>
                                <div class="form-group">
                                    <label for="numofhour">Number of Hours:</label>
                                    <input type="number" class="form-control" id="numofhour" name="numofhour" required>
                                </div>
                                <div class="form-group">
                                    <label for="difficulty">Task Difficulty (1 to 10):</label>
                                    <input type="number" class="form-control" id="difficulty" name="difficulty" min="1" max="10" required>
                                </div>
                                <div class="form-group">
                                    <label for="clientdurak">Client's idiot (1 to 10):</label>
                                    <input type="number" class="form-control" id="clientdurak" name="clientdurak" min="1" max="10" required>
                                </div>
                                <button type="submit" class="btn btn-primary">Calculate Budget</button>
                            </form>
                           </div>
                        </div>
                    </body>
                    </html>
                    """

                    return task_details_html

    # If the user is not logged in or does not own the task, redirect to the login page
    return redirect(url_for('login'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    user_id = session.get('user_id')

    if user_id:
        # Check if the user owns the task
        connection, cursor = connect_to_database()
        if connection:
            sql = "SELECT UserID FROM Tasks WHERE TaskID=?"
            cursor.execute(sql, (task_id,))
            task_owner = cursor.fetchone()

            if task_owner and str(task_owner[0]) == str(user_id):
                if request.method == 'POST':
                    # Retrieve updated task details from the form
                    title = request.form.get('title')
                    description = request.form.get('description')
                    priority = request.form.get('priority')
                    status = request.form.get('status')
                    due_date = request.form.get('due_date')

                    # Here you can update the task in the database using the provided task details and task_id
                    update_task_in_database(task_id, title, description, priority, status, due_date)

                    # Redirect back to the task details page after successful update
                    return redirect(url_for('task_details', task_id=task_id))

                # Retrieve the current task details to pre-fill the form
                sql = "SELECT * FROM Tasks WHERE TaskID=? AND UserID=?"
                cursor.execute(sql, (task_id, user_id))
                task = cursor.fetchone()

                if task:
                    # Generate HTML for the edit task form
                    edit_task_html = '''  <script>
        // Function to set the preferred color mode and store it in a cookie
        function setColorMode(colorMode) {
            document.cookie = `colorMode=${colorMode};path=/;max-age=31536000`; // Cookie expires in one year
            applyColorMode(colorMode);
        }

        // Function to apply the preferred color mode
        function applyColorMode(colorMode) {
            if (colorMode === 'dark') {
                // Apply dark mode styles
                document.body.classList.add('dark-mode');
            } else {
                // Apply white mode styles
                document.body.classList.remove('dark-mode');
            }
        }

        // Function to load the preferred color mode from the cookie when the page loads
        function loadColorMode() {
            const colorMode = document.cookie.replace(/(?:(?:^|.*;\s*)colorMode\s*\=\s*([^;]*).*$)|^.*$/, "$1");
            applyColorMode(colorMode);
        }

        // Load the preferred color mode when the page loads
        window.addEventListener('load', loadColorMode);
    </script>''' + f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Edit Task</title>
                        <link rel="stylesheet" href="{url_for('static', filename='css/bootstrap.min.css')}">
                        <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
                    </head>
                    <body>

                        <nav class="navbar navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="/">TodoMaster</a>
        <div class="navbar-nav ml-auto">
            <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('white')">White Mode</a>
            <a class="nav-link" href="javascript:void(0)" onclick="setColorMode('dark')">Dark Mode</a>
            <a class="nav-link" href="{url_for('logout')}">Logout</a>
        </div>
    </div>
</nav>


                        <div class="container mt-5">
                            <div class="jumbotron text-center">
                                <h1>Edit Task</h1>
                                <form method="post">
                                    <div class="form-group">
                                        <label for="title">Title:</label>
                                        <input type="text" class="form-control" id="title" name="title" value="{task[1]}" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="description">Description:</label>
                                        <textarea class="form-control" id="description" name="description" required>{task[2]}</textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="priority">Priority:</label>
                                        <select class="form-control" id="priority" name="priority" required>
                                            <option value="High" {'selected' if task[3] == 'High' else ''}>High</option>
                                            <option value="Medium" {'selected' if task[3] == 'Medium' else ''}>Medium</option>
                                            <option value="Low" {'selected' if task[3] == 'Low' else ''}>Low</option>
                                        </select>
                                    </div>
                                    <div class="form-group">
                                        <label for="status">Status:</label>
                                        <select class="form-control" id="status" name="status" required>
                                            <option value="Pending" {'selected' if task[4] == 'Pending' else ''}>Pending</option>
                                            <option value="In Progress" {'selected' if task[4] == 'In Progress' else ''}>In Progress</option>
                                            <option value="Completed" {'selected' if task[4] == 'Completed' else ''}>Completed</option>
                                        </select>
                                    </div>
                                    <div class="form-group">
                                        <label for="due_date">Due Date:</label>
                                        <input type="date" class="form-control" id="due_date" name="due_date" value="{task[5]}" required>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Save Changes</button>
                                </form>
                            </div>
                        </div>
                    </body>
                    </html>
                    """

                    return edit_task_html

    # If the user is not logged in or does not own the task, redirect to the login page
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
