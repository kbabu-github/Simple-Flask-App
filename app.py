from flask import Flask, render_template, request, redirect, url_for
import os, json, string

app = Flask(__name__)

language_options = ["English", "Spanish", "French"]
port_options = [3306, 5432, 27017]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    filename = file.filename  # Get the filename
    # Get the list of available drives
    drives = get_available_drives()

    if file and filename.endswith('.json'):
        config_file = file.read().decode('utf-8')
        config_data = json.loads(config_file)
        return render_template('index.html', config_data=config_data, language_options=language_options, port_options=port_options, filename=filename,
                               drives=drives)
    else:
        return "Invalid file type"


@app.route('/save', methods=['POST'])
def save_config():
    filename = request.form['filename']
    # save_location = request.form.get('save_location')
    version = request.form.get('version')
    language = request.form.get('language')
    host = request.form.get('host')
    port = request.form.get('port')
    username = request.form.get('username')
    password = request.form.get('password')

    data = {
        "general": {
            "version": version,
            "language": language
        },
        "database": {
            "host": host,
            "port": port,
            "username": username,
            "password": password
        }
    }
    
    write_config(filename, data)
    
    confirmation_message = "Configuration file has been saved successfully."
    
    return render_template('confirmation.html', confirmation_message=confirmation_message)

def write_config(file_name, data):
    config_file_path = 'D:\\' + file_name
    with open(config_file_path, "w") as file:
        json.dump(data, file, indent=4)

def get_available_drives():
    # Get a list of available drives on the server
    if os.name == 'nt':
        # For Windows
        return ['{}:\\'.format(d) for d in string.ascii_uppercase if os.path.exists('{}:\\'.format(d))]
    else:
        # For Unix-like systems
        return ['/']
    
if __name__ == '__main__':
    app.run(debug=True)
