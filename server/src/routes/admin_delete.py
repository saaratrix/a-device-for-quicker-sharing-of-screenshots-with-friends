import os
from flask import Blueprint, Response, current_app
from .admin_stats import month_lookup
from ..admin_tools.admin_url_prefix import admin_url_prefix
from server.src.uploads.file_manager import FileManager
from server.src.admin_tools.admin_credentials import auth

admin_delete_bp = Blueprint('admin_delete', __name__, template_folder='')
reverse_month_lookup = {value: key for key, value in month_lookup.items()}


@admin_delete_bp.route(f'{admin_url_prefix}/delete/year/<year>')
@auth.login_required
def delete_year(year: str) -> Response:
    year = year[2:]
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], year)
    success = FileManager.delete_date_directory_recursively(path)
    return "Success" if success else "Failed", 200


@admin_delete_bp.route(f'{admin_url_prefix}/delete/year/<year>/month/<month>')
@auth.login_required
def delete_month(year: str, month: str) -> Response:
    year = year[2:]
    month = reverse_month_lookup.get(month, "undefined")
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], year, month)
    success = FileManager.delete_date_directory_recursively(path)
    return "Success" if success else "Failed", 200


@admin_delete_bp.route(f'{admin_url_prefix}/delete/year/<string:year>/month/<string:month>/day/<string:day>')
@auth.login_required
def delete_day(year: str, month: str, day: str) -> Response:
    year = year[2:]
    month = reverse_month_lookup.get(month, None)
    if (month is None):
        return "Failed", 200
    day = format_day(day)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], year, month, day)
    success = FileManager.delete_date_directory_recursively(path)
    return "Success" if success else "Failed", 200

def format_day(day: str) -> str:
    return f"0{day}" if int(day) < 10 else day