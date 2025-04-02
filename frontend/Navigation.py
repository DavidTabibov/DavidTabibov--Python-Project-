import reactpy
from reactpy import html

@reactpy.component
def Navigation(current_page, set_page, user=None, logout_user=None):
    def handle_logout(e):
        if logout_user:
            logout_user()
        set_page("home")
    
    if user:
        auth_links = [
            html.span({"style": {"marginRight": "1rem", "color": "white"}}, f"Hello, {user.get('username', 'User')}"),
            html.a(
                {"href": "#", "onClick": handle_logout, "style": {
                    "color": "white",
                    "textDecoration": "none",
                    "padding": "8px 16px",
                    "backgroundColor": "#e74c3c",
                    "borderRadius": "4px",
                    "cursor": "pointer"
                }},
                "Logout"
            )
        ]
    else:
        auth_links = [
            html.a(
                {"href": "#", "onClick": lambda e: set_page("register"), "style": {
                    "color": "white",
                    "textDecoration": "none",
                    "marginRight": "15px",
                    "padding": "8px 16px",
                    "backgroundColor": "#2ecc71",
                    "borderRadius": "4px",
                    "cursor": "pointer"
                }},
                "Register"
            ),
            html.a(
                {"href": "#", "onClick": lambda e: set_page("login"), "style": {
                    "color": "white",
                    "textDecoration": "none",
                    "padding": "8px 16px",
                    "backgroundColor": "#3498db",
                    "borderRadius": "4px",
                    "cursor": "pointer"
                }},
                "Login"
            )
        ]
    
    return html.nav(
        {"style": {
            "padding": "15px 20px",
            "backgroundColor": "#2c3e50",
            "color": "white",
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "marginBottom": "30px",
            "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"
        }},
        html.div(
            {},
            html.a(
                {"href": "#", "onClick": lambda e: set_page("home"), "style": {
                    "color": "white",
                    "textDecoration": "none",
                    "fontSize": "22px",
                    "fontWeight": "bold"
                }},
                "Blog Home"
            )
        ),
        html.div({"style": {"display": "flex", "alignItems": "center"}}, *auth_links)
    )