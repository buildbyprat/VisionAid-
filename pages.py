from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def index():
    return render_template("index.html")

@pages_bp.route("/login")
def login_page():
    return render_template("login.html")

@pages_bp.route("/signup")
def signup_page():
    return render_template("signup.html")

@pages_bp.route("/verify")
def verify_page():
    return render_template("verify.html")

@pages_bp.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

@pages_bp.route("/reports")
def reports_page():
    return render_template("reports.html")

@pages_bp.route("/profile")
def profile_page():
    return render_template("profile.html")
