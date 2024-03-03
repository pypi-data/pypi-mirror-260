from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Bootstrap Budget Imports
from .auth import login_required, user_only


# Define as a Flask blueprint: User
bp = Blueprint('budget_item', __name__, url_prefix='/budget-items')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    return render_template('budget-item.html')
