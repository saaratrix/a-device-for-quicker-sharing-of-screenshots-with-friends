from flask import Blueprint, current_app, Response, request, render_template
from admin_tools.file_stats import get_overview_stats
from admin_tools.admin_credentials import auth

admin_stats_bp = Blueprint('admin_stats', __name__, template_folder='')

# Month lookup dictionary
month_lookup = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}


@admin_stats_bp.route('/admin/stats/overview', methods=['GET'])
@auth.login_required
def overview() -> Response:
    base_uri = get_base_uri(request.headers.environ)
    upload_path = current_app.config['UPLOAD_FOLDER']
    stats, year_stats = get_overview_stats(upload_path)

    overall_stats = convert_to_presentable_stats(stats, year_stats)
    # Now we have the stats, now we need some HTML to present it as a webpage.
    return render_template('stats_page.html', base_uri=base_uri, stats=overall_stats)


def get_base_uri(headers):
    # REQUEST_URI will look like "/admin/stats/overview"
    url = headers.get('X-Original-URI') or headers.get('REQUEST_URI')
    url = url.split('/stats/overview')[0]
    return url


def size_to_megabytes(size: int) -> str:
    megabytes = size / 2 ** 20
    text = f"{megabytes:.3f}".rstrip('0').rstrip('.')
    return f"{text} MB"


def convert_to_presentable_stats(root_stats, year_items):
    years = []
    for year_name, (year_stats, month_items) in year_items:
        months = []
        year = {
            # When we get to 22nd century this code is broken, waaaa!
            'name': f"20{year_stats['name']}",
            'size': size_to_megabytes(year_stats['total_size']),
            'files': year_stats['total_files'],
            'months': months
        }
        years.append(year)

        for month_name, (month_stats, day_items) in month_items:
            days = []

            month = {
                'name': month_lookup.get(month_stats['name'], "Unknown Month"),
                'size': size_to_megabytes(month_stats['total_size']),
                'files': month_stats['total_files'],
                'days': days,
            }
            months.append(month)

            for day_name, (day_stats, _) in day_items:
                day_name = str(int(day_stats['name']))

                day = {
                    'name': day_name,
                    'size': size_to_megabytes(day_stats['total_size']),
                    'files': day_stats['total_files'],
                }
                days.append(day)

    overall = {
        'name': 'Overview',
        'size': size_to_megabytes(root_stats['total_size']),
        'files': root_stats['total_files'],
        'years': years,
    }

    return overall
