from flask import redirect, render_template, flash, request, session
from base import app
from werkzeug.utils import secure_filename
from base.com.service_layer.service import perform_inference
import os
from random import random
from base.com.vo.results_vo import ResultVO
from base.com.dao.results_dao import ResultsDAO

# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=['GET'])
def home():
    try:
        return render_template("login.html")
    except Exception as e:
        return render_template('/templates/errorPage.html', error=e)
    
    
app.config['UPLOAD_FOLDER'] = f"base/static/uploads/"
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username')
        passwd = request.form.get('password')
                
        if uname == 'admin' and passwd == 'admin':
            session['logged_in'] = True
            session['username'] = uname
            
            path_to_save = os.path.join(app.config['UPLOAD_FOLDER'])
            os.makedirs(path_to_save, exist_ok=True)
            
            return render_template('dashboard.html')
        else:
            flash('Username or passoword is wrong.')
            return redirect('/')
        
        
@app.route('/upload-to-infer')
def dashboard():
    return render_template('uploadPage.html')
              
@app.route('/upload-again')
def load_upload():
    return render_template('uploadPage.html')

@app.route('/back-dashboard')
def return_dashboard():
    return render_template('dashboard.html')
    
            
@app.route('/upload-file', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            uploaded_file = request.files['uploadfile']
            selected_model = request.form['model_name']
            print(selected_model)
            if uploaded_file.filename.endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi')):
                
                infer_file = secure_filename(uploaded_file.filename)
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], infer_file)
                uploaded_file.save(path_to_save)
                
                count = perform_inference(selected_model, infer_file)
                # print(garbage_count, pothole_count)
                results_vo = ResultVO()
                results_vo.image_name = infer_file
                
                if selected_model == 'pothole':
                    results_vo.potholes_count = count
                    results_vo.cattles_count = 0
                elif selected_model == 'cattle':
                    results_vo.cattles_count = count
                    results_vo.potholes_count = 0
                else:
                    pass
                    
                if selected_model in ('pothole', 'cattle'):  
                    results_dao = ResultsDAO()
                    results_dao.insert_result(results_vo)
                
                # results_view = results_dao.view_result()
                # print(results_view)
                cache_buster = int(random() * 1000)
            
                return render_template('results.html', results=infer_file, count=count, model_name=selected_model, cache_buster=cache_buster)
            else:
                return 'Invalid file type !!'
        
        except Exception as e:
                return render_template('errorPage.html', error=e)  
    # return render_template('uploadPage.html', default_model='model1')
    
@app.route('/logout')
def logout():
    if 'username' in session:
        uname = session['username']
        session.clear()
        
        folders = [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]
        for folder in folders:
            if os.path.exists(folder):
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        return render_template('errorPage.html', error=e)
    
        flash('Logged out successfully!!')
    return redirect('/')