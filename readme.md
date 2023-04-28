## Запуск проекта

Для первого запуска
В консоли последовательно написать следующие 4 команды
```bash
python -m venv venv (для Windows) python3 -m venv venv (для Linux)
venv\Scripts\activate (для Windows) venv/bin/activate (для Linux)
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Для последующих запусков
```bash
venv\Scripts\activate (для Windows) venv/bin/activate (для Linux)
python app.py
```