import threading
import webview
from flask import Flask, render_template
import mimetypes

mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('image/svg+xml', '.svg')

# Создание экземпляра приложения Flask
app = Flask(__name__, static_folder=r'static\node_modules', template_folder='templates')

# Определение маршрута для главной страницы
@app.route("/")
def main():
    return render_template("index.html")

# Функция для запуска сервера Flask в отдельном потоке
def run_flask():
    app.run(port=5000, use_reloader=False)  # Отключите debug и use_reloader для многопоточной среды

# Запуск Flask-сервера в фоновом режиме
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Запуск окна webview, указывая URL локального сервера
w = webview.create_window('Flask Example', 'http://127.0.0.1:5000')

webview.start()



