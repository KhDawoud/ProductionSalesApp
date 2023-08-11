from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from pandas import read_excel
from SiteCode.models import SalesPerson, Progress
from SiteCode.Admin.forms import UploadForm
import pandas as pd
from sqlalchemy import or_

admin = Blueprint("admin", __name__)

original_data = read_excel(r'SiteCode/Live Data/vendor.xlsx')
original_data = original_data[original_data["Cost"] > 0]
original_data2 = read_excel(r'SiteCode/Live Data/customer.xlsx')
original_data2 = original_data2[original_data2["Revenue"] > 0]
data = None
data2 = None
active = "All"
active2 = "All"


@admin.route('/setup')
@login_required
def setup():
    if current_user.role != 2:
        return redirect(url_for('main.home'))
    global original_data2, original_data, active, active2, data, data2
    active, active2 = "All", "All"
    data, data2 = None, None
    comp = set(current_user.companies_available.split(','))
    original_data = original_data[original_data['Carrier'].isin(comp)]

    original_data2 = original_data2 if current_user.username == "Admin1" else \
        original_data2[original_data2['Carrier'].str.contains('|'.join(comp), case=False)]

    return redirect(url_for('admin.partner_admin'))


@login_required
@admin.route('/partneradmincustomer')
def customer_table():
    if current_user.role != 2:
        return redirect(url_for('main.home'))
    comp = SalesPerson.query.filter_by(username=current_user.username)
    comp = comp.first().companies_available.split(',')
    data = original_data2 if data2 is None else data2
    colour = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] else "primary"
    return render_template('partneradmincustomer.html', companies_available=comp, active=active2, data=data,
                           headings=["Carrier", "Country", "Revenue"], colour=colour)


@admin.route('/processtablecustomer/<string:company>')
def process_table_customer(company):
    if current_user.role != 2:
        return redirect(url_for('main.home'))
    global original_data2, data2, active2
    if company != "All":
        active2 = company
        data2 = original_data2[original_data2['Carrier'].str.lower().str.contains(company.lower())]
    else:
        data2 = None
        active2 = "All"
    return redirect(url_for('admin.customer_table'))


@login_required
@admin.route('/processtable/<string:company>')
def process_table(company):
    if current_user.role != 2:
        return redirect(url_for('main.home'))
    global original_data, data, active
    if company != "All":
        active = company
        data = original_data[original_data['Cost'] > 0]
        data = data[data['Carrier'] == company]
    else:
        data = None
        active = "All"
    return redirect(url_for("admin.partner_admin"))


@admin.route('/partneradmin')
@login_required
def partner_admin():
    global original_data, data, active
    if current_user.role != 2:
        return redirect(url_for('main.home'))
    comp = SalesPerson.query.filter_by(username=current_user.username)
    comp = comp.first().companies_available.split(',')
    table = data if data is not None else original_data
    colour = "danger" if current_user.entity in ["Acepeak", "TechOpen", "Letsdial", "Teloz", "Rosper"] else "primary"
    return render_template('partner_admin.html', companies_available=comp, headers=["Carrier", "Country", "Cost"],
                           data=table, active=active, colour=colour)


@admin.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    global original_data, original_data2
    if current_user.role != 2:
        return redirect(url_for('main.home'))
    form = UploadForm()
    height = "75vh"

    if form.validate_on_submit():
        if form.customer.data:
            customer_file = form.customer.data
            if customer_file.filename.lower().endswith('.csv'):
                try:
                    df = pd.read_csv(customer_file, encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(customer_file, encoding='latin-1')
                df.to_excel(r"SiteCode/Live Data/customer.xlsx", index=False)
            else:
                df = pd.read_excel(customer_file)
                df.to_excel(r"SiteCode/Live Data/customer.xlsx", index=False)
            original_data2 = pd.read_excel(r"SiteCode/Live Data/customer.xlsx")
            original_data2 = original_data2[original_data2["Revenue"] > 0]
        if form.vendor.data:
            vendor_file = form.vendor.data
            if vendor_file.filename.lower().endswith('.csv'):
                try:
                    df = pd.read_csv(vendor_file, encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(vendor_file, encoding='latin-1')
                df.to_excel(r"SiteCode/Live Data/vendor.xlsx", index=False)
            else:
                df = pd.read_excel(vendor_file)
                df.to_excel(r"SiteCode/Live Data/vendor.xlsx", index=False)
            original_data = pd.read_excel(r"SiteCode/Live Data/vendor.xlsx")
            original_data = original_data[original_data["Cost"] > 0]

        if form.leads.data:
            leads_file = form.leads.data
            if leads_file.filename.lower().endswith('.csv'):
                try:
                    df = pd.read_csv(leads_file, encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(leads_file, encoding='latin-1')
                df.to_excel(r"SiteCode/Live Data/leads.xlsx", index=False)
            else:
                df = pd.read_excel(leads_file)
                df.to_excel(r"SiteCode/Live Data/leads.xlsx", index=False)

        if not any([form.customer.data, form.vendor.data, form.leads.data]):
            form.leads.errors.append("At least one field must be entered")
            form.customer.errors.append("At least one field must be entered")
            form.vendor.errors.append("At least one field must be entered")
            height = "85vh"
    else:
        height = "85vh" if request.method == "POST" else "75vh"

    return render_template('upload.html', form=form, height=height)


def create_summary_table():
    usernames = SalesPerson.query.filter(
        (SalesPerson.role != 2) &
        (SalesPerson.progresses.any()) &
        (SalesPerson.partner.any()) &
        (SalesPerson.entity.in_(current_user.companies_available.split(',')))
    ).all()
    summary_data = []
    for user in usernames:
        communication_count = Progress.query.filter_by(salesperson=user,
                                                       conversation="We both have communicated").count()
        partner_names = [partner.name for partner in user.partner]
        live_status = any(original_data2['Carrier'].str.contains('|'.join(partner_names), case=False, na=False))
        summary_data.append((user.username, communication_count, live_status))
    return summary_data
