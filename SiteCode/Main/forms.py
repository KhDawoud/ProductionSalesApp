from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email
from SiteCode import db
from SiteCode.models import Partner
import email_validator


class UpdatePartnerForm(FlaskForm):
    name = StringField("Partner Name", validators=[DataRequired(), Length(2, 50)])
    email = StringField("Email ID", validators=[DataRequired(), Email()])
    skype = StringField("Skype ID", validators=[DataRequired()])
    relation = SelectField("Relation", validators=[DataRequired()],
                           choices=["Choose...", "Customer", "Bilateral", "Vendor"])
    destinations = TextAreaField("Offered Destinations (Separate with Comma)", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_relation(self, relation):
        if relation.data == "Choose...":
            raise ValidationError("This Field is Required")

    def validate_email(self, email):
        if db.session.query(Partner).filter_by(email=email.data).first():
            raise ValidationError("Email already in use")

    def validate_skype(self, skype):
        if db.session.query(Partner).filter_by(skype=skype.data).first():
            raise ValidationError("Skype ID already in use")


class AdminUpdatesForm(FlaskForm):
    daily = StringField('Daily Message', validators=[Length(0, 50)])
    content = TextAreaField('Content', validators=[Length(0, 400)])
    company = SelectField("Message for Company", choices=["Choose..."])
    submit = SubmitField("Send")
