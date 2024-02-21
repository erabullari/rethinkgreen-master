from datetime import datetime
from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.recycle import Recycle
from flask_app.models.user import User
import os   
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/recycle' , methods=['POST'])   
def recycle():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Recycle.validate_recycle(request.form):
        return redirect(request.referrer)
    data = {
        "address": request.form['address'],
        "material": request.form['materialType'],
        "items": request.form['totalItems'],
        "user_id": session['user_id']
    }
    
    if request.form['materialType'] == 'aluminum':
        point_rc = 2 * int(request.form['totalItems'])
    elif request.form['materialType'] == 'plastic':
        point_rc = 0.5 * int(request.form['totalItems'])
    elif request.form['materialType'] == 'paper':
        point_rc = 1 * int(request.form['totalItems'])
    elif request.form['materialType'] == 'other':
        point_rc = 0.25 * int(request.form['totalItems'])
    
    user=User.get_by_id({'id':session['user_id']})
    user_points = user.points
    user_points += point_rc
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], current_time + filename))
            data["image"] = current_time + filename
            data2 = {
                "id": session['user_id'],
                "points": user_points
            }
            User.update_points(data2)
            Recycle.save(data)
    return redirect('/')
