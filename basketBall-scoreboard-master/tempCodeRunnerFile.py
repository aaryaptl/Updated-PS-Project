# app.py
from flask import Flask, render_template
import subprocess
import threading

app = Flask(__name__, template_folder="C:\\Users\\ganji\\OneDrive\\Desktop\\integration")
count = 0  # Global variable to store the count
skip_count = 0  # Global variable to store the count of skipped outputs

def check_output():
    global count, skip_count
    process = subprocess.Popen(['python', 'your_script.py'], stdout=subprocess.PIPE, text=True)

    for line in process.stdout:
        line = line.strip()
        if line:
            print(f"Received from your_script.py: {line}")
            if(skip_count==0):
                if 'shot' in line :
                    count += 1
                    print(count)
                    update_webserver(count)
                    skip_count = 20  # Set skip_count to 5 to skip the next 5 outputs

            if skip_count > 0:
                skip_count -= 1
                continue

            update_webserver(count)

    process.wait()  # Wait for the subprocess to complete
    print("Process completed. Stopping the output checking.")

def update_webserver(count):
    with app.app_context():
        render_template('index_dynamic_update.html', count=count)

@app.route('/')
def index():
    return render_template('index_dynamic_update.html', count=count)

if __name__ == "__main__":
    output_thread = threading.Thread(target=check_output)
    output_thread.start()
    app.run(debug=True, use_reloader=False)