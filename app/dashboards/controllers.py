from . import dashboards
from app.main.models import InventoryHost
from flask import render_template
from flask.ext.login import login_required

@dashboards.route('/overview')
@login_required
def overview():
  return render_template('overview.html')

@dashboards.route('/assets')
@login_required
def assets():
  inventory_hosts = InventoryHost.query.all()
  return render_template('assets.html', inventory_hosts=inventory_hosts)
