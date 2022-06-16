from email import message
from app import app, q
from flask import render_template, request, flash
from app.tasks import count_words, create_image_set
from time import strftime
import secrets, os


@app.route('/')
def index():
    return 'Hey ya'

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    jobs = q.jobs
    message = None

    if request.args:
        url = request.args.get('url')
        task = q.enqueue(count_words, url)
        jobs = q.jobs
        q_len = len(q)
        message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs queued"

    return render_template('add_task.html', message = message, jobs = jobs)



app.config['SECRET_KEY'] = 'e7320fksue8909@Hdeowie'
app.config['UPLOAD_DIRECTORY'] = '/home/james/Desktop/PYthon_Projects/NEW_PROJECTS/TASK_QUEUES/main/app/static/img/uploads'

@app.route('/upload_image', methods = ['GET', 'POST'])
def upload_image():
    message = None
    if request.method == 'POST':
        image = request.files['image']
        image_dir_name = secrets.token_hex(16)

        os.mkdir(os.path.join(app.config['UPLOAD_DIRECTORY'], image_dir_name))
        image.save(os.path.join(app.config['UPLOAD_DIRECTORY'], image_dir_name, image.filename))

        image_dir = os.path.join(app.config['UPLOAD_DIRECTORY'], image_dir_name)

        q.enqueue(create_image_set, image_dir, image.filename)

        flash("Image uploaded and sent for resizing", 'success')

        message = f"/image/{image_dir_name}/{image.filename.split('.')[0]}"
        

    return render_template('upload_image.html', message = message)

@app.route('/image/<dir>/<img>')
def view_image(dir, img):
    return render_template('view_image.html', dir = dir, img = img)