from __init__ import create_app
from scheduler import start_scheduler

app = create_app()
start_scheduler()

if __name__ == '__main__':
    app.run(debug=True)
