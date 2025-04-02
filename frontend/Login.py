import base64
import json
import reactpy
from reactpy import html, hooks
import requests

API_BASE = "http://localhost:8000/api"

def decode_jwt(token):
    """
    מפענח JWT ומחזיר את ה-payload כמילון.
    """
    try:
        # JWT בנוי מ-3 חלקים מופרדים ב-'.'
        payload_part = token.split('.')[1]
        # ודא שיש padding מתאים
        padding = '=' * ((4 - len(payload_part) % 4) % 4)
        payload_part += padding
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        return json.loads(decoded_bytes)
    except Exception as e:
        print("Error decoding JWT:", e)
        return {}

@reactpy.component
def Login(set_page, login_user=None):
    username, set_username = hooks.use_state("")
    password, set_password = hooks.use_state("")
    error_msg, set_error_msg = hooks.use_state("")

    def on_login(e):
        if not username or not password:
            set_error_msg("Username and password are required")
            return
        try:
            url = f"{API_BASE}/token/"
            payload = {"username": username, "password": password}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # data מכיל את המפתחות "access" ו-"refresh"
                access_token = data.get("access")
                # מפענחים את ה-JWT כדי לקבל את פרטי המשתמש
                user_data = decode_jwt(access_token)
                if login_user:
                    login_user(data, user_data)
                set_error_msg("")
                set_page("home")
            else:
                set_error_msg("Login failed. Please check your credentials.")
        except Exception as e:
            print("Login error:", e)
            set_error_msg("Login error. Please try again.")

    return html.div(
        {"style": {
            "maxWidth": "400px",
            "margin": "0 auto",
            "padding": "30px",
            "backgroundColor": "white",
            "borderRadius": "8px",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.1)"
        }},
        html.h1({"style": {
            "textAlign": "center",
            "marginBottom": "30px",
            "color": "#2c3e50"
        }}, "Login"),
        html.div(
            {"style": {"marginBottom": "20px"}},
            html.label({"htmlFor": "username", "style": {
                "display": "block",
                "marginBottom": "8px",
                "fontWeight": "bold"
            }}, "Username:"),
            html.input({
                "id": "username",
                "type": "text",
                "placeholder": "Enter your username",
                "value": username,
                "onChange": lambda e: set_username(e["target"]["value"]),
                "style": {
                    "width": "100%",
                    "padding": "10px",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd",
                    "fontSize": "16px"
                }
            })
        ),
        html.div(
            {"style": {"marginBottom": "30px"}},
            html.label({"htmlFor": "password", "style": {
                "display": "block",
                "marginBottom": "8px",
                "fontWeight": "bold"
            }}, "Password:"),
            html.input({
                "id": "password",
                "type": "password",
                "placeholder": "Enter your password",
                "value": password,
                "onChange": lambda e: set_password(e["target"]["value"]),
                "style": {
                    "width": "100%",
                    "padding": "10px",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd",
                    "fontSize": "16px"
                }
            })
        ),
        html.div({"style": {"color": "red", "marginBottom": "20px", "textAlign": "center"}}, error_msg),
        html.div(
            {"style": {"textAlign": "center"}},
            html.button({
                "onClick": on_login, 
                "style": {
                    "padding": "12px 24px",
                    "backgroundColor": "#3498db",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "fontSize": "16px",
                    "width": "100%"
                }
            }, "Login")
        ),
        html.div(
            {"style": {"marginTop": "20px", "textAlign": "center"}},
            "Don't have an account? ",
            html.a({
                "href": "#",
                "onClick": lambda e: set_page("register"),
                "style": {
                    "color": "#3498db",
                    "cursor": "pointer",
                    "textDecoration": "none"
                }
            }, "Register here")
        ),
        html.div(
            {"style": {"marginTop": "30px", "textAlign": "center"}},
            html.button({
                "onClick": lambda e: set_page("home"), 
                "style": {
                    "padding": "8px 16px",
                    "backgroundColor": "#95a5a6",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "fontSize": "14px"
                }
            }, "Back to Home")
        )
    )
