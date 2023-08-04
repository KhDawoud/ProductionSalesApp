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
    if form.validate_on_submit():
        if form.daily.data.strip() or form.content.data.strip():
            if form.daily.data.strip():
                daily_message = DailyMessage(date=datetime.datetime.now().replace(second=0, microsecond=0),
                                             message=form.daily.data,
                                             salesperson=current_user)
                db.session.add(daily_message)

            if form.content.data.strip():
                content_message = ContentMessage(date=datetime.datetime.now().replace(second=0, microsecond=0),
                                                 message=form.content.data,
                                                 salesperson=current_user)
                db.session.add(content_message)
            db.session.commit()
            flash("Message Added Successfully")
            return redirect(url_for('main.home'))
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
                              destinations=form.destinations.data, entity=current_user.entity)
        db.session.add(new_partner)
        db.session.commit()
        flash('Partner Added Successfully')
        return redirect(url_for('main.home'))
    colour = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] else "primary"
    background = "blob2-bg" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"]\
        else "blob-bg"
    button = "gradient-button4" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"]\
        else "gradient-button3"
    return render_template('update_partner.html', form=form, colour=colour, background=background, button=button)
