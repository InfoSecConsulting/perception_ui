from . import dashboards
from app.main.models import InventoryHost, InventorySvc, SvcNseScript, Vulnerability
from flask import render_template, request, jsonify
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

@dashboards.route('/individual_asset', methods=['GET'])
@login_required
def individual_asset():

  if request.method == 'GET':
    nse_scripts = list()
    data_id = request.args.get('data_id')
    services = InventorySvc.query.filter_by(inventory_host_id=data_id).all()
    vulns = Vulnerability.query.filter_by(inventory_host_id=data_id).all()

    for service in services:
      svc_nse_script = SvcNseScript.query.filter_by(inventory_svc_id=service.id).all()
      nse_scripts.append(svc_nse_script)

    #for service in services:
    #  svc_dict = {'name': service.name,
    #              'protocol': service.protocol,
    #              'port': service.portid,
    #              'product': service.svc_product,
    #              'extra_info': service.extra_info,
    #              'created_at': service.created_at.strftime('%b-%d-%Y %H:%M'),
    #              'updated_at': service.updated_at.strftime('%b-%d-%Y %H:%M')}
    #  svc_list.append(svc_dict)

    #return jsonify(svc_list=svc_list)

    return render_template('individual_asset.html', services=services, nse_scripts=nse_scripts, vulns=vulns)
