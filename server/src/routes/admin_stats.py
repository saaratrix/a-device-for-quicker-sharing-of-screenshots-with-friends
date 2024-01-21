from flask import Blueprint

admin_stats = Blueprint('admin_stats', __name__)


@admin_stats.route('/admin/stats/overview')
def overview():
    pass
