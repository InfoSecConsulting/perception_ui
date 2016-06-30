# Import flask dependencies
from app.main.models import CoreRouter, LinuxUser, SmbUser, Target, SnmpString, Schedule
from flask import request, render_template, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app import db
from . import settings
from .forms import Seeds, ServiceAccounts, Targets, SnmpInfo, EditSnmpInfo, SchedulesInfo
from flask.ext.login import login_required
from ipaddress import ip_address
from app.lib.crypt import decrypt_string


@settings.route('/seeds', methods=['GET', 'POST'])
@login_required
def seeds():
  core_router = None
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
          core_router = CoreRouter(ip_addr=seeds_form.ip_addr.data,
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

@settings.route('/delete_service_accounts', methods=['POST'])
@login_required
def delete_service_accounts():
  record = None

  if request.method == 'POST':
    data_id = request.args.get('data_id')
    data_set = request.args.get('data_set')

    if data_set == 'l':
      record = LinuxUser.query.filter_by(id=data_id).first()

    if data_set == 's':
      record = SmbUser.query.filter_by(id=data_id).first()

    if record is not None:
      try:
        db.session.delete(record)
        db.session.commit()
      except IntegrityError as e:
        db.session.rollback()
        flash(e)

    return redirect(url_for('settings.service_accounts'))

@settings.route('/targets', methods=['GET', 'POST'])
@login_required
def targets():
  targets_a = []
  targets = Target.query.all()
  targets_form = Targets(request.form)
  ip_addr = None
  subnet = None

  if request.method == 'GET':

    for t in targets:
      d = {'ip_addr': t.ip_addr,
           'subnet': t.subnet}
      targets_a.append(d)

  if request.method == 'POST':

    if targets_form.validate_on_submit():
      return redirect(url_for('settings.forms'))

  return render_template('targets.html',
                         ip_addr=ip_addr,
                         subnet=subnet,
                         targets_form=targets_form)

@settings.route('/snmp_info', methods=['GET', 'POST'])
@login_required
def snmp_info():
  d = {}
  snmp_a = []
  snmp_strings = SnmpString.query.all()
  snmp_users = None
  snmp_groups = None
  community_strings = None
  snmp_info_form = SnmpInfo(request.form)
  edit_snmp_info_form = EditSnmpInfo(request.form)

  if request.method == 'GET':
    for s in snmp_strings:
      if s.snmp_user_encrypted is None:
        d = {'id': s.id,
             'community_string': decrypt_string(s.community_string_encrypted.encode("utf-8"),
                                                s.community_string_encrypted_salt.encode("utf-8")),
             'snmp_user': None,
             'snmp_group': None}
      if s.community_string_encrypted is None:
        d = {'id': s.id,
             'snmp_user': decrypt_string(s.snmp_user_encrypted.encode("utf-8"),
                                         s.snmp_user_encrypted_salt.encode("utf-8")),
             'snmp_group': decrypt_string(s.snmp_group_encrypted.encode("utf-8"),
                                          s.snmp_group_encrypted_salt.encode("utf-8")),
             'community_string': None}
      snmp_a.append(d)

  if request.method == 'POST':

    if snmp_info_form.validate_on_submit():
      if snmp_info_form.strings.data:
        s = snmp_info_form.strings.data

        for community_string in s.split(','):
          cs = SnmpString(community_string=community_string)

          try:
            db.session.add(cs)
            db.session.commit()
          except IntegrityError as e:
            db.session.rollback()
            flash(e)

      return redirect(url_for('settings.snmp_info'))

  return render_template('snmp_info.html',
                         snmp_a=snmp_a,
                         community_string=community_strings,
                         snmp_user=snmp_users,
                         snmp_group=snmp_groups,
                         snmp_info_form=snmp_info_form,
                         edit_snmp_info_form=edit_snmp_info_form)


@settings.route('/edit_snmp_info', methods=['POST'])
@login_required
def edit_snmp_info():
  edit_snmp_info_form = EditSnmpInfo(request.form)

  if request.method == 'POST':
    data_id = request.args.get('data_id')
    community_sting = request.args.get('community_sting')
    snmp_user = request.args.get('snmp_user')
    snmp_group = request.args.get('snmp_group')

  return redirect(url_for('settings.snmp_info'))


@settings.route('/delete_snmp_info', methods=['POST'])
@login_required
def delete_snmp_info():

  if request.method == 'POST':
    data_id = request.args.get('data_id')
    record = SnmpString.query.filter_by(id=data_id).first()

    try:
      db.session.delete(record)
      db.session.commit()
    except IntegrityError as e:
      db.session.rollback()
      flash(e)

    return redirect(url_for('settings.snmp_info'))


@settings.route('/schedules', methods=['GET', 'POST'])
@login_required
def schedules():
  schedules_info_form = SchedulesInfo(request.form)

  if request.method == 'POST':
    if schedules_info_form.validate_on_submit():
      if schedules_info_form.name.data:
        s_name = schedules_info_form.name.data

  if request.method == 'GET':
    all_schedules = Schedule.query.all()

  return render_template('schedules.html', all_schedules=all_schedules, schedules_info_form=schedules_info_form)
