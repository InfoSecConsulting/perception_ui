from . import settings
from flask import render_template
from flask.ext.login import login_required


@settings.route('/seeds')
@login_required
def seeds():
  return render_template('seeds.html')
