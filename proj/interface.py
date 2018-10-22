from flask import Flask
from .celery import app
from tasks import add

interface = Flask(__name__)
interface.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
interface.config['CELERY_RESULT_BACKEND'] = 'pyamqp://guest@localhost//'

#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config)

@app.route('/add', methods=['GET'])
def celery_add(x, y):
    task = add(x, y)
    return task

if __name__ == '__main__':
    interface.run(host='0.0.0.0',debug=True)
