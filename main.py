from flask import Flask, render_template, request, flash, redirect, session
# from flask.ext.session import Session
from werkzeug.utils import secure_filename
from imageSplitter import responsive
import os, time

UPLOAD_FOLDER = 'static/User/'
# savingPath = '/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
user = 'AiDesign'
saveTime = 0

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template("index.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global user
    user = 'AiDesign'
    return redirect('/')# render_template("index.html")

@app.route('/beranda', methods=['GET', 'POST'])
def homepage():
    # return('home')
    global user
    if user == 'AiDesign' or user== None:
        user = request.form.get("userActive", type=str)
    username = {"nickname": user}
    if user == None:
        pass
    elif os.path.isdir(UPLOAD_FOLDER+user) == False: 
        os.makedirs(UPLOAD_FOLDER+user )
        os.makedirs(UPLOAD_FOLDER+user +'/ImageSplitter/')

    return render_template("main.html", user=username)

# Function for image cropper
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imageSplitter', methods=['GET', 'POST'])
def uploadFile():
    global user, saveTime
    if request.method == 'POST':
        splitXby = request.form.get("countX", type=int)
        splitYby = request.form.get("countY", type=int)

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            # return ('HEHE')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_filename = os.path.join((app.config['UPLOAD_FOLDER']+user), filename)
            saveTime = int(time.time())
            os.makedirs(UPLOAD_FOLDER+user +'/ImageSplitter/'+str(saveTime)+'/')
            file.save(full_filename)
            responsive((UPLOAD_FOLDER+user+'/'+filename),splitXby,splitYby,(UPLOAD_FOLDER+user+'/ImageSplitter/'+str(saveTime)+'/'))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            # return render_template("imageShow.html",user_image=full_filename)

            # files = os.listdir(UPLOAD_FOLDER+user+'/ImageSplitter/')
            # return render_template('files.html', files=files, user=user)
            return redirect('/results')

    return render_template('imageSplitter.html', user=user)

@app.route('/results', methods=['GET', 'POST'])
def results():
    files = os.listdir(UPLOAD_FOLDER+user+'/ImageSplitter/'+str(saveTime)+'/')
    return render_template('files.html', files=files, user=user, saveTime=saveTime)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # session.init_app(app)
    app.run(debug=True)
    