import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, Length
from SiteCode import db
from SiteCode.models import SalesPerson
import email_validator


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 60)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(4, 60)])
    submit = SubmitField("Create Account")

    def validate_email(self, email):
        pattern = r'@([^.]+)'
        new_entity = re.search(pattern, email.data).group(1)
        entity_dict = {
            'meratalk': 'Mera Talk',
            'acepeakinvestment': 'Acepeak',
            'twichinggeneraltrading': 'Twiching',
            'softtop': 'Softtop',
            'letsdial': 'Letsdial',
            'ajoxi': 'Ajoxi',
            'techopensystems': 'TechOpen',
            'teloz': 'Teloz',
            'rozper': 'Rosper',
            'mycompanymobile': 'MCM'
        }
        if not entity_dict.get(new_entity):
            raise ValidationError("This is not a valid company email")
        if db.session.query(SalesPerson).filter_by(email=email.data).first():
            raise ValidationError("Email already in use")

    def validate_username(self, username):
        if db.session.query(SalesPerson).filter_by(username=username.data).first():
            raise ValidationError("Username already in use")


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(4, 60)])
    submit = SubmitField("Login")


class UpdateProgressForm(FlaskForm):

    company_name = StringField("Company Name", validators=[DataRequired()])
    country = SelectField("Country", choices=["Choose...", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
                                              "Antigua and Barbuda", "Argentina",
                                              "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
                                              "Bangladesh", "Barbados",
                                              "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
                                              "Bosnia and Herzegovina", "Botswana",
                                              "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde",
                                              "Cambodia", "Cameroon",
                                              "Canada", "Central African Republic", "Chad", "Chile", "China",
                                              "Colombia", "Comoros", "Congo",
                                              "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark",
                                              "Djibouti", "Dominica",
                                              "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador",
                                              "Equatorial Guinea", "Eritrea",
                                              "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon",
                                              "Gambia", "Georgia",
                                              "Germany",
                                              "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
                                              "Guyana", "Haiti", "Honduras",
                                              "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
                                              "Israel", "Italy", "Jamaica",
                                              "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North",
                                              "Korea, South", "Kosovo",
                                              "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia",
                                              "Libya", "Liechtenstein",
                                              "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives",
                                              "Mali", "Malta",
                                              "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia",
                                              "Moldova", "Monaco", "Mongolia",
                                              "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
                                              "Nepal", "Netherlands",
                                              "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia",
                                              "Norway", "Oman", "Pakistan",
                                              "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
                                              "Poland", "Portugal",
                                              "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
                                              "Saint Lucia",
                                              "Saint Vincent and the Grenadines",
                                              "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal",
                                              "Serbia", "Seychelles",
                                              "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
                                              "Somalia", "South Africa",
                                              "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
                                              "Switzerland", "Syria", "Taiwan",
                                              "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga",
                                              "Trinidad and Tobago", "Tunisia", "Turkey",
                                              "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
                                              "United Kingdom",
                                              "United States",
                                              "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela",
                                              "Vietnam", "Yemen", "Zambia",
                                              "Zimbabwe"
                                              ], validators=[DataRequired()])
    communication = SelectField("Mode Of Communication", choices=["Choose...", "Skype-Chat", "Email", "Phone"],
                                validators=[DataRequired()])
    name_call = SelectField("Company Name Call", choices=["Choose..."], validators=[DataRequired()])
    sales_name = StringField("Salesperson Name at BPO", validators=[DataRequired()])
    conversation = SelectField("Conversation", choices=["Choose...", "I have sent message but no response",
                                                             "We both have communicated",
                                                             "Internal communication (not with customer)"],
                               validators=[DataRequired()])
    response = TextAreaField("Enter Customer Response")
    submit = SubmitField("Submit")

    def validate_country(self, country):
        if country.data == "Choose...":
            raise ValidationError("This Field is Required")

    def validate_communication(self, comm):
        if comm.data == "Choose...":
            raise ValidationError("This Field is Required")

    def validate_name_call(self, name):
        if name.data == "Choose...":
            raise ValidationError("This Field is Required")

    def validate_conversation(self, conversation):
        if conversation.data == "Choose...":
            raise ValidationError("This Field is Required")
