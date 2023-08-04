import datetime
import re
import pandas
from flask import Blueprint, render_template, url_for, redirect, request, flash
from SiteCode import db, bcrypt
from flask_login import login_user, login_required, current_user, logout_user
from SiteCode.models import SalesPerson, Progress, Partner
from SiteCode.Salesperson.forms import LoginForm, UpdateProgressForm, RegisterForm

sales_person = Blueprint("sales", __name__)

data = pandas.read_excel(r"C:\Users\Admin\Desktop\SalesApp\SiteCode\Live Data\leads.xlsx")


@sales_person.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data)
        pattern = r'@([^.]+)'
        new_entity = re.search(pattern, form.email.data).group(1)
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
        new_user = SalesPerson(username=form.username.data, email=form.email.data, password=password_hash, role=1,
                               entity=entity_dict[new_entity])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('sales.login'))
    return render_template('register.html', form=form)


@sales_person.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = SalesPerson.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            form.password.errors.append("Login failed. Check password")
            form.email.errors.append("Login failed. Check email")
    return render_template('login.html', form=form)


@sales_person.route('/updateprogress', methods=["POST", "GET"])
@login_required
def update_progress():
    sidebar = "sidebar2-bg" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] \
        else "sidebar-bg"
    background = "#F89880" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] \
        else "#E0FFFF"
    name_call_choices_dict = {
        "TechOpen": ["Choose...", "Layla", "Anna", "Mary"],
        "MCM": ["Choose...", "Shamim", "Sarah", "Jasmine", "Amreen", "Farheen", "Sam", "Muskan", "Tamanna", "Sunayana"],
        "Twiching": ["Choose...", "Andrea", "Adela", "Rache"],
        "Softtop": ["Choose...", "Camila", "Jacob", "Pablo", "Marry"],
        "Acepeak": ["Choose...", "Jennifer", "Rose", "Sana", "Stefany", "Linda", "Anna", "Poonam"],
        "Letsdial": ["Choose...", "Elsa", "Ammy", "Ricky", "Sofia"],
        "Ajoxi": ["Choose...", "Vaibhav", "Shazmeen"]
    }
    choice = name_call_choices_dict.get(current_user.entity)
    form = UpdateProgressForm()
    form.name_call.choices = choice
    if form.validate_on_submit():
        if form.conversation.data == "We both have communicated" and not form.response.data:
            form.response.errors.append('This field is required')
        else:
            new_prog = Progress(date=datetime.datetime.now().replace(second=0, microsecond=0),
                                company_name=form.company_name.data, conversation=form.conversation.data,
                                country=form.country.data, communication=form.communication.data,
                                bpo=form.sales_name.data, name_call=form.name_call.data, response=form.response.data)
            current_user.progresses.append(new_prog)
            db.session.commit()
            colour = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz",
                                                         "Rosper"] else "info"
            return render_template('update_progress_success.html', colour=colour, sidebar=sidebar,
                                   background=background)
    colour = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz",
                                                 "Rosper"] else "primary"
    btn = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] else "info"
    return render_template('update_progress.html', form=form, colour=colour, sidebar=sidebar, background=background,
                           btn=btn)


@sales_person.route('/viewinfo/<string:active>')
@login_required
def view_info(active):
    a = "" if active == "Progress" else "d-none"
    b = "" if active == "Partners" else "d-none"
    if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"]:
        c = "btn-danger" if not a else "btn-outline-danger"
        d = "btn-danger" if not b else "btn-outline-danger"
        colour = "danger"
    else:
        c = "btn-primary" if not a else "btn-outline-primary"
        d = "btn-primary" if not b else "btn-outline-primary"
        colour = "primary"
    prog = reversed(current_user.progresses)
    if current_user.role == 2:
        comp = current_user.companies_available.split(',')
        p_list = Partner.query.filter(Partner.entity.in_(comp)).all()
        prog = [s.progresses for s in SalesPerson.query.filter(SalesPerson.entity.in_(comp)).all()]
        prog = reversed([item for sublist in prog for item in sublist])
    else:
        p_list = Partner.query.filter_by(entity=current_user.entity).all()
        prog = reversed(current_user.progresses)
    return render_template('view_info.html', headings=["Username", "Date", "Company Name",
                                                       "Country", "Communication",
                                                       "SalesPerson BPO", "Name Call",
                                                       "Conversation"], p_headings=["Partner Name", "Date",
                                                                                    "Email ID", "Skype ID", "Type",
                                                                                    "Destinations"],
                           progress=prog, user=current_user, partner=p_list, a=a, b=b, c=c, d=d, colour=colour)


@login_required
@sales_person.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sales.login'))


@login_required
@sales_person.route('/viewleads')
def view_leads():
    global data
    data = pandas.read_excel(r"C:\Users\Admin\Desktop\SalesApp\SiteCode\Live Data\leads.xlsx")
    colour = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz",
                                                 "Rosper"] else "primary"
    if not current_user.lead:
        new_data = data.sample(n=10) if len(data) >= 10 else data
        return render_template('leads.html', data=new_data, colour=colour, user=current_user,
                               headings=["Name", "Contact Information"])
    else:
        return render_template('lead_chosen.html', user=current_user, colour=colour,
                               headings=["Name", "Contact Information"])


@login_required
@sales_person.route('/processleads/<string:info>')
def process_leads(info):
    global data
    current_user.lead = info
    data = data[data["Name"] != info.split()[0]]
    data.to_excel(r"C:\Users\Admin\Desktop\SalesApp\SiteCode\Live Data\leads.xlsx")
    db.session.commit()
    flash("Lead Chosen Succesfully")
    return redirect(url_for('main.home'))


@login_required
@sales_person.route('/leadcomplete')
def lead_complete():
    current_user.lead = None
    db.session.commit()
    return redirect(url_for('main.home'))


@login_required
@sales_person.route('/leadchange')
def lead_change():
    global data
    info = current_user.lead.split()
    new_row = {'Name': info[0], 'Contact': info[1]}
    data.loc[len(data)] = new_row
    data.to_excel(r"C:\Users\Admin\Desktop\SalesApp\SiteCode\Live Data\leads.xlsx")
    current_user.lead = None
    db.session.commit()
    return redirect(url_for('main.home'))
