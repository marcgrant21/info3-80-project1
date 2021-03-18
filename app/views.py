from app import app, db
from flask import render_template, request, url_for, redirect, flash, send_from_directory
from .forms import NewForm
from werkzeug.utils import secure_filename
from .models import Property
from sqlalchemy import exc

import datetime
import os

@app.route("/")
def home():
    return render_template('home.html')
    
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')   
    
@app.route("/property", methods=["GET", "POST"])
def property():
    newPropertyForm = NewForm()
    
    if request.method == "POST":
        if  newPropertyForm.validate_on_submit():
           
                title =  newPropertyForm.title.data
                description = newPropertyForm.description.data
                number_of_bedrooms = newPropertyForm.number_of_bedrooms.data
                number_of_bathrooms = newPropertyForm.number_of_bathrooms.data
                location = newPropertyForm.location.data
                price = newPropertyForm.price.data
                Type = newPropertyForm.Type.data
                photo = newPropertyForm.photo.data
                filename = secure_filename(photo.filename)
                
                propertyH = Property(title,description,number_of_bedrooms,number_of_bathrooms,price,location,Type,filename)
                
                db.session.add(propertyH)
                db.session.commit()
                
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                
                flash("Profile Added", "success")
                return redirect(url_for("properties"))
            
        
        errors = form_errors(newPropertyForm)
        flash(''.join(error+" " for error in errors), "danger")
    return render_template("new_property.html", newPropertyForm = newPropertyForm)


@app.route("/properties")
def properties():
    propertyHA = Property.query.all()
    properties = []
    
    for propertyH  in propertyHA:
        properties.append({"title":propertyH.title, "price":propertyH.price, "location":propertyH.location, "photo":propertyH.photo, "id":propertyH.id})
    
    return render_template("view_all_properties.html", properties = properties)

@app.route('/property/<propertyid>')
def inidi_property(propertyid):
    propertyH  = Property.query.filter_by(id=propertyid).first()
    
    if propertyH  is None:
        return redirect(url_for('home'))
    
    return render_template("property.html", propertyH=propertyH)

@app.route('/uploads/<filename>')
def get_image(filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILES_DIR = os.path.abspath(os.path.join(BASE_DIR, app.config['UPLOAD_FOLDER']))
    return send_from_directory(FILES_DIR, filename, as_attachment =True)
    


def read_file(filename):
    data = ""
    
    with open(filename, "r") as stream:
        data = stream.read()
        
    return data

def form_errors(form):
    error_list =[]
    for field, errors in form.errors.items():
        for error in errors:
            error_list.append(field+": "+error)
            
    return error_list
    
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
