from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from database import fetch_sensor_data, fetch_sensor_data_last_minute
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
# socketio = SocketIO(app)


@app.route('/')
def index():
    """Главная страница с отображением текущих данных датчиков."""
    data = fetch_sensor_data_last_minute()
    data_average = calculate_average(data)
    return render_template('index.html', data=data, data_average=data_average)


@app.route('/sensor/<int:sensor_type>')
def sensor_chart(sensor_type):
    """Страница с графиком для одного датчика."""
    return render_template('sensor_chart.html', sensor_type=sensor_type)


@app.route('/overview')
def overview_chart():
    """Страница с общим графиком всех датчиков."""
    data = fetch_sensor_data_last_minute()
    sensors = list({row['sensor_id'] for row in data})
    return render_template('overview.html', sensors=sensors)

@socketio.on('connect')
def handle_connect():
    print("Клиент подключился")

@socketio.on('request_chart_data')
def send_chart_data(sensor_type):
    print(f"Получен запрос на данные для графика датчика {sensor_type}")
    data = fetch_sensor_data_last_minute(sensor_type)
    socketio.emit('chart_data', {'sensor_type': sensor_type, 'data': data})

@socketio.on('request_overview_data')
def send_overview_data():
    print("Получен запрос на данные для общего графика")
    data = fetch_sensor_data_last_minute()
    socketio.emit('overview_data', {'data': data})


def calculate_average(data):
    """Вычисляет среднее значение для каждого датчика."""
    averages = {}
    for row in data:
        sensor_type = row['sensor_id']
        if sensor_type not in averages:
            averages[sensor_type] = []
        averages[sensor_type].append(row['value'])
    return {sensor_type: round(sum(values) / len(values), 2) for sensor_type, values in averages.items()}


def data_update_thread():
    """Фоновый поток для обновления данных."""
    while True:
        time.sleep(1)
        data = fetch_sensor_data_last_minute()
        data_average = calculate_average(data)
        socketio.emit('update_data', {'averages': data_average})


if __name__ == '__main__':
    threading.Thread(target=data_update_thread, daemon=True).start()
    socketio.run(app, debug=True)
