from flask import jsonify, render_template_string

class APIError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(e):
        if request.is_json or request.path.startswith("/api/"):
            return jsonify({"error": e.message}), e.status
        return render_template_string(f"<h1>Error</h1><p>{e.message}</p>"), e.status

    @app.errorhandler(404)
    def handle_404(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Not found"}), 404
        return render_template_string("<h1>404</h1><p>Page not found</p>"), 404

    @app.errorhandler(500)
    def handle_500(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error"}), 500
        return render_template_string("<h1>500</h1><p>Server error</p>"), 500

from flask import request
