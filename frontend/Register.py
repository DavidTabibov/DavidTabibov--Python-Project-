import reactpy
from reactpy import html, hooks
import requests

API_BASE = "http://localhost:8000/api"

@reactpy.component
def Register(set_page, login_user=None):
    username, set_username = hooks.use_state("")
    email, set_email = hooks.use_state("")
    password, set_password = hooks.use_state("")
    password_confirm, set_password_confirm = hooks.use_state("")
    error_msg, set_error_msg = hooks.use_state("")

    def handle_input_change(e, setter):
        if isinstance(e, dict) and "target" in e and "value" in e["target"]:
            setter(e["target"]["value"])
        else:
            setter(e)

    def on_register(e):
        if not username or not email or not password or not password_confirm:
            set_error_msg("All fields are required")
            return
        if password != password_confirm:
            set_error_msg("Passwords don't match")
            return
        try:
            url = f"{API_BASE}/register/"
            payload = {
                "username": username,
                "email": email,
                "password": password,
                "password2": password_confirm
            }
            print(f"Sending registration request: {payload}")
            response = requests.post(url, json=payload)
            print(f"Registration response: {response.status_code}")
            if response.status_code in [200, 201]:
                print("Registration successful")
                set_page("home")
            else:
                error_message = f"Registration failed: {response.status_code}"
                try:
                    error_data = response.json()
                    print(f"Error data: {error_data}")
                    if isinstance(error_data, dict):
                        details = []
                        for key, value in error_data.items():
                            if isinstance(value, list):
                                details.append(f"{key}: {', '.join(value)}")
                            else:
                                details.append(f"{key}: {value}")
                        if details:
                            error_message = " | ".join(details)
                except Exception as ex:
                    error_message = f"Error: {response.text}"
                set_error_msg(error_message)
        except Exception as ex:
            print(f"Registration error: {ex}")
            set_error_msg(f"Error: {str(ex)}")
    
    return html.div(
        {"style": {
            "maxWidth": "500px",
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
        }}, "Create an Account"),
        html.div({"style": {"marginBottom": "15px"}}, 
            html.label({"style": {"display": "block", "marginBottom": "5px"}}, "Username:"),
            html.input({
                "type": "text",
                "value": username,
                "onChange": lambda e: handle_input_change(e, set_username),
                "style": {
                    "width": "100%", 
                    "boxSizing": "border-box",
                    "padding": "8px",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd"
                }
            })
        ),
        html.div({"style": {"marginBottom": "15px"}}, 
            html.label({"style": {"display": "block", "marginBottom": "5px"}}, "Email:"),
            html.input({
                "type": "email",
                "value": email,
                "onChange": lambda e: handle_input_change(e, set_email),
                "style": {
                    "width": "100%", 
                    "boxSizing": "border-box",
                    "padding": "8px",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd"
                }
            })
        ),
        html.div({"style": {"marginBottom": "15px"}}, 
            html.label({"style": {"display": "block", "marginBottom": "5px"}}, "Password:"),
            html.input({
                "type": "password",
                "value": password,
                "onChange": lambda e: handle_input_change(e, set_password),
                "style": {
                    "width": "100%", 
                    "boxSizing": "border-box",
                    "padding": "8px",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd"
                }
            })
        ),
        html.div({"style": {"marginBottom": "15px"}}, 
            html.label({"style": {"display": "block", "marginBottom": "5px"}}, "Confirm Password:"),
            html.input({
                "type": "password",
                "value": password_confirm,
                "onChange": lambda e: handle_input_change(e, set_password_confirm),
                "style": {
                    "width": "100%", 
                    "boxSizing": "border-box",
                    "padding": "8px",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd"
                }
            })
        ),
        html.div({"style": {"color": "red", "textAlign": "center", "margin": "15px 0"}}, error_msg),
        html.div({"style": {"marginBottom": "15px"}},
            html.button({
                "onClick": lambda _: on_register(None), 
                "style": {
                    "width": "100%",
                    "padding": "10px",
                    "backgroundColor": "#4CAF50",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "fontSize": "16px"
                }
            }, "Register")
        ),
        html.div({"style": {"textAlign": "center", "marginBottom": "15px"}},
            "Already have an account? ",
            html.a({
                "onClick": lambda _: set_page("login"),
                "style": {"color": "#2196F3", "cursor": "pointer", "textDecoration": "none"}
            }, "Login here")
        ),
        html.div({"style": {"textAlign": "center"}},
            html.button({
                "onClick": lambda _: set_page("home"), 
                "style": {
                    "padding": "8px 16px",
                    "backgroundColor": "#95a5a6",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer"
                }
            }, "Back to Home")
        )
    )
