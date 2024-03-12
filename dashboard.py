from flask import Flask, Response, render_template, jsonify
from datetime import datetime
import random
import cv2

app = Flask(__name__)

# Mock data for compass direction
compass_direction = 0

# Mock data for humidity, temperature, and pressure
humidity = 50
temperature = 25
pressure = 1000

# Mock data for accelerometers
accelerometer1 = {'x': 0, 'y': 0, 'z': 9.8}
accelerometer2 = {'x': 0, 'y': 0, 'z': 9.8}
accelerometer3 = {'x': 0, 'y': 0, 'z': 9.8}

def gen_frames():
    camera = cv2.VideoCapture(0)  # Use 0 for the default camera
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/current-time')
def get_current_time():
    current_time = datetime.now().isoformat()
    return jsonify({'currentTime': current_time})

@app.route('/video-stream')
def get_video_stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/compass-direction')
def get_compass_direction():
    global compass_direction
    compass_direction += random.randint(-5, 5)  # Simulate compass direction change
    return jsonify({'direction': compass_direction})

@app.route('/humidity-data')
def get_humidity_data():
    global humidity
    humidity += random.randint(-2, 2)  # Simulate humidity change
    humidity = max(0, min(100, humidity))  # Clamp humidity between 0 and 100
    return jsonify({'humidity': humidity})

@app.route('/temperature-data')
def get_temperature_data():
    global temperature
    temperature += random.uniform(-1, 1)  # Simulate temperature change
    return jsonify({'temperature': temperature})

@app.route('/pressure-data')
def get_pressure_data():
    global pressure
    pressure += random.randint(-10, 10)  # Simulate pressure change
    return jsonify({'pressure': pressure})

@app.route('/accelerometer-data')
def get_accelerometer_data():
    global accelerometer1, accelerometer2, accelerometer3
    accelerometer1['x'] += random.uniform(-0.1, 0.1)  # Simulate accelerometer changes
    accelerometer1['y'] += random.uniform(-0.1, 0.1)
    accelerometer1['z'] += random.uniform(-0.1, 0.1)

    accelerometer2['x'] += random.uniform(-0.1, 0.1)
    accelerometer2['y'] += random.uniform(-0.1, 0.1)
    accelerometer2['z'] += random.uniform(-0.1, 0.1)

    accelerometer3['x'] += random.uniform(-0.1, 0.1)
    accelerometer3['y'] += random.uniform(-0.1, 0.1)
    accelerometer3['z'] += random.uniform(-0.1, 0.1)

    return jsonify({
        'accelerometer1': accelerometer1,
        'accelerometer2': accelerometer2,
        'accelerometer3': accelerometer3
    })

if __name__ == '__main__':
    app.run(debug=True)