from flask import render_template, request
from App import app 


@app.errorhandler(403)
def unauthorised(e):
    return render_template('errors/403.html', msg=e), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', msg=e), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('errors/405.html', msg=e), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', msg=e), 500


app.register_error_handler(403, unauthorised)
app.register_error_handler(404, page_not_found)
app.register_error_handler(405, method_not_allowed)
app.register_error_handler(500, internal_server_error)