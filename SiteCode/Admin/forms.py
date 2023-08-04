from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField


class UploadForm(FlaskForm):
    customer = FileField('Enter Customer Excel', validators=[FileAllowed(['xls', 'xlsx', "csv"], "Must be an excel or csv file")])
    vendor = FileField('Enter Vendor Excel', validators=[FileAllowed(['xls', 'xlsx', "csv"], "Must be an excel or csv file")])
    leads = FileField('Enter Leads Excel', validators=[FileAllowed(['xls', 'xlsx', "csv"], "Must be an excel or csv file")])
    submit = SubmitField('Submit')