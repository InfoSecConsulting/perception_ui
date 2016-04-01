# Import flask dependencies
from app.main.models import CoreRouter, LinuxUser, SmbUser, SnmpString
from flask import request, render_template, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app import db
from . import settings
from .forms import Seeds, ServiceAccounts
from flask.ext.login import login_required
from ipaddress import ip_address


@settings.route('/seeds', methods=['GET', 'POST'])
@login_required
def seeds():
  seeds_form = Seeds(request.form)
  seed_router = CoreRouter.query.first()
  if seed_router is None:

    if request.method == 'POST':
      if seeds_form.validate_on_submit():

        linux_user = LinuxUser(username=seeds_form.username.data,
                             password=seeds_form.password.data,
                             enable_password=seeds_form.enable_password.data)
        try:
          u = LinuxUser.query.filter_by(username=seeds_form.username.data).first()

          if u is None:
            db.session.add(linux_user)
            db.session.commit()
            u = LinuxUser.query.filter_by(username=seeds_form.username.data).first()

        except IntegrityError as e:
          db.session.rollback()
          flash(e)
          return redirect(url_for('settings.seeds'))

        try:
          if ip_address(seeds_form.ip_addr.data):
            core_router = CoreRouter(ip_addr=seeds_form.ip_addr.data,
                                      linux_user_id=u.id)

        except ValueError:
          core_router = CoreRouter(host_name=seeds_form.ip_addr.data,
                                    linux_user_id=u.id)

        try:
          db.session.add(core_router)
          db.session.commit()
        except IntegrityError as e:
          db.session.rollback()
          flash(e)
          return redirect(url_for('settings.seeds'))

  elif seed_router:

    if request.method == 'POST':
      print('post')

  return render_template('seeds.html',
                         seeds_form=seeds_form,
                         seed_router=seed_router)

@settings.route('/service_accounts', methods=['GET', 'POST'])
@login_required
def service_accounts():
  accounts = []
  smb_users = SmbUser.query.all()
  linux_users = LinuxUser.query.all()
  svc_accounts_form = ServiceAccounts(request.form)

  if request.method == 'GET':

    for u in linux_users:
      d = {'username': u.username, 'u_id': u.id, 'account_type': 'l', 'description': u.description}
      accounts.append(d)

    for u in smb_users:
      d = {'username': u.username, 'u_id': u.id, 'account_type': 's', 'description': u.description}
      accounts.append(d)

  if request.method == 'POST':

    if svc_accounts_form.validate_on_submit():

      if svc_accounts_form.radio2.data:

        if svc_accounts_form.radio2.data == 'linux_user':

          linux_user = LinuxUser(username=svc_accounts_form.username.data,
                                 password=svc_accounts_form.password.data,
                                 enable_password=svc_accounts_form.enable_password.data,
                                 description=svc_accounts_form.description.data)

          try:
            db.session.add(linux_user)
            db.session.commit()
            return redirect(url_for('settings.service_accounts'))
          except IntegrityError as e:
            db.session.rollback()
            flash(e)
            return redirect(url_for('settings.service_accounts'))

        elif svc_accounts_form.radio2.data == 'smb_user':

          smb_user = SmbUser(username=svc_accounts_form.username.data,
                             password=svc_accounts_form.password.data,
                             domain_name=svc_accounts_form.domain_name.data,
                             description=svc_accounts_form.description.data)
          try:
            db.session.add(smb_user)
            db.session.commit()
            return redirect(url_for('settings.service_accounts'))
          except IntegrityError as e:
            db.session.rollback()
            flash(e)
            return redirect(url_for('settings.service_accounts'))

  return render_template('service_accounts.html',
                         service_accounts=accounts,
                         svc_accounts_form=svc_accounts_form)

@settings.route('/schedules', methods=['GET', 'POST'])
@login_required
def schedules():
  return render_template('schedules.html')
