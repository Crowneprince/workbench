import dash
from dash import Input, Output, State


def login_callback(app):
    @app.callback(
        Output('url-login', 'pathname'),
        Input('login-button', 'n_clicks'),
        [State('username', 'value'), State('password', 'value')],
        prevent_initial_call=True
    )
    def successful_login(n_clicks, username, password):
        if n_clicks and username == "admin" and password == "admin":
            return '/claims_analysis_pg'
        return dash.no_update

    # Callback to handle page routing (if any logic is needed beyond dash.page_container)

    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        # Routing logic here if needed
        return dash.page_container
