import datetime
from flask import Blueprint, render_template, url_for, redirect, flash, get_flashed_messages
from flask_login import login_required, current_user
from SiteCode import db
from SiteCode.Main.forms import UpdatePartnerForm, AdminUpdatesForm
from SiteCode.models import Partner, DailyMessage, ContentMessage, SalesPerson

main = Blueprint("main", __name__)


@main.route("/", methods=["POST", "GET"])
@login_required
def home():
    form = AdminUpdatesForm()

    if current_user.role == 2:
        form.company.choices = ["Choose...", "All"] + current_user.companies_available.split(',')
        dm = (
            DailyMessage.query
            .join(DailyMessage.salesperson)
            .filter(SalesPerson.companies_available.contains(current_user.entity))
            .filter(DailyMessage.date.between(datetime.datetime.now().replace(second=0, microsecond=0)
                                              .replace(hour=0, minute=0), datetime.datetime.now().
                                              replace(second=0, microsecond=0).replace(hour=23, minute=59)))
            .all())
        cm = (
            ContentMessage.query
            .join(ContentMessage.salesperson)
            .filter(SalesPerson.companies_available.contains(current_user.entity))
            .filter(ContentMessage.date.between(datetime.datetime.now().replace(second=0, microsecond=0)
                                                .replace(hour=0, minute=0), datetime.datetime.now().
                                                replace(second=0, microsecond=0).replace(hour=23, minute=59)))
            .all())
    else:
        dm = (
            DailyMessage.query
            .filter(DailyMessage.companies.contains(current_user.entity))
            .filter(DailyMessage.date.between(datetime.datetime.now().replace(second=0, microsecond=0)
                                              .replace(hour=0, minute=0), datetime.datetime.now().
                                              replace(second=0, microsecond=0).replace(hour=23, minute=59)))
            .all())
        cm = (
            ContentMessage.query
            .filter(ContentMessage.companies.contains(current_user.entity))
            .filter(ContentMessage.date.between(datetime.datetime.now().replace(second=0, microsecond=0)
                                                .replace(hour=0, minute=0), datetime.datetime.now().
                                                replace(second=0, microsecond=0).replace(hour=23, minute=59)))
            .all())

        dm = dm if current_user.username != "Admin 1" else DailyMessage.query.filter(
            DailyMessage.date.between(datetime.datetime.now().replace(second=0, microsecond=0)
                                      .replace(hour=0, minute=0), datetime.datetime.now().
                                      replace(second=0, microsecond=0).replace(hour=23, minute=59))).all()
    cm = cm if current_user.username != "Admin 1" else ContentMessage.query.filter(
        ContentMessage.date.between(datetime.datetime.now().replace(second=0, microsecond=0)
                                    .replace(hour=0, minute=0), datetime.datetime.now().
                                    replace(second=0, microsecond=0).replace(hour=23, minute=59))).all()
    if form.validate_on_submit():
        if form.daily.data.strip() or form.content.data.strip():
            if form.company.data != "Choose...":
                if form.daily.data.strip():
                    company = form.company.data if form.company.data != "All" else current_user.companies_available
                    daily_message = DailyMessage(date=datetime.datetime.now().replace(second=0, microsecond=0),
                                                 message=form.daily.data,
                                                 companies=company, salesperson=current_user)
                    db.session.add(daily_message)

                if form.content.data.strip():
                    company = form.company.data if form.company.data != "All" else current_user.companies_available
                    content_message = ContentMessage(date=datetime.datetime.now().replace(second=0, microsecond=0),
                                                     message=form.content.data, salesperson=current_user,
                                                     companies=company)
                    db.session.add(content_message)
                db.session.commit()
                flash("Message Added Successfully")
                return redirect(url_for('main.home'))
            else:
                form.company.errors.append("This field is required")
        else:
            form.daily.errors.append("At least one field must be filled")
            form.content.errors.append("At least one field must be filled")
    colour = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] else "primary"
    return render_template("home.html", current_user=current_user, form=form, daily_messages=dm, content_messages=cm,
                           colour=colour)


@main.route('/updatepartner', methods=["GET", "POST"])
@login_required
def update_partner():
    form = UpdatePartnerForm()
    if form.validate_on_submit():
        new_partner = Partner(date=datetime.datetime.now().replace(second=0, microsecond=0), name=form.name.data,
                              email=form.email.data, skype=form.skype.data, relation=form.relation.data,
                              destinations=form.destinations.data, entity=current_user.entity, salesperson=current_user)
        db.session.add(new_partner)
        db.session.commit()
        flash('Partner Added Successfully')
        return redirect(url_for('main.home'))
    colour = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] else "primary"
    background = "blob2-bg" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] \
        else "blob-bg"
    button = "gradient-button4" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] \
        else "gradient-button3"
    return render_template('update_partner.html', form=form, colour=colour, background=background, button=button)


@login_required
@main.route('/deletecm/<int:msg_id>')
def delete_cmessage(msg_id):
    if current_user.role != 2:
        flash("Must be admin")
        return redirect(url_for("main.home"))
    msg = ContentMessage.query.get(msg_id)
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for("main.home"))


@main.route('/deletedm/<int:msg_id>')
def delete_dmessage(msg_id):
    if current_user.role != 2:
        flash("Must be admin")
        return redirect(url_for("main.home"))
    msg = DailyMessage.query.get(msg_id)
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for("main.home"))
