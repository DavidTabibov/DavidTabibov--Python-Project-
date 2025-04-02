import reactpy
from reactpy import html, hooks
import requests

API_BASE = "http://localhost:8000/api"

@reactpy.component
def EditArticle(article, set_page, token=None):
    title, set_title = hooks.use_state(article.get("title", ""))
    content, set_content = hooks.use_state(article.get("content", ""))
    tags, set_tags = hooks.use_state(article.get("tags", ""))
    error_msg, set_error_msg = hooks.use_state("")
    
    def handle_input_change(e, setter):
        if isinstance(e, dict) and 'target' in e and 'value' in e['target']:
            setter(e['target']['value'])
        else:
            setter(e)
    
    def update_article(e):
        if not title or not content:
            set_error_msg("Title and content are required")
            return
            
        if not token:
            set_error_msg("You must be logged in to edit an article")
            return
            
        try:
            url = f"{API_BASE}/articles/{article.get('id')}/"
            headers = {"Authorization": f"Bearer {token.get('access')}"}
            
            payload = {
                "title": title,
                "content": content,
                "tags": tags
            }
            
            print(f"Updating article: {payload}")
            response = requests.put(url, json=payload, headers=headers)
            print(f"Update article response: {response.status_code}")
            
            if response.status_code in [200, 201, 204]:
                set_page("home")  # Redirect to home after successful update
            else:
                try:
                    error_data = response.json()
                    print(f"Error data: {error_data}")
                    error_message = "Error updating article: "
                    if isinstance(error_data, dict):
                        for key, value in error_data.items():
                            if isinstance(value, list):
                                error_message += f"{key}: {', '.join(value)} | "
                            else:
                                error_message += f"{key}: {value} | "
                    set_error_msg(error_message)
                except:
                    set_error_msg(f"Error updating article: {response.status_code}")
        except Exception as e:
            print(f"Error updating article: {e}")
            set_error_msg(f"Error: {str(e)}")
    
    return html.div(
        {"style": {
            "maxWidth": "800px",
            "margin": "0 auto",
            "padding": "20px"
        }},
        html.h1({"style": {"borderBottom": "2px solid #eee", "paddingBottom": "10px"}}, "Edit Article"),
        
        # Error message
        html.div({"style": {"color": "red", "marginBottom": "20px"}}, error_msg),
        
        # Title field
        html.div({"style": {"marginBottom": "20px"}},
            html.label({"style": {"display": "block", "marginBottom": "5px", "fontWeight": "bold"}}, "Title:"),
            html.input({
                "type": "text",
                "value": title,
                "onChange": lambda e: handle_input_change(e, set_title),
                "style": {
                    "width": "100%",
                    "padding": "10px",
                    "boxSizing": "border-box",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd"
                }
            })
        ),
        
        # Content field
        html.div({"style": {"marginBottom": "20px"}},
            html.label({"style": {"display": "block", "marginBottom": "5px", "fontWeight": "bold"}}, "Content:"),
            html.textarea({
                "value": content,
                "onChange": lambda e: handle_input_change(e, set_content),
                "style": {
                    "width": "100%",
                    "height": "300px",
                    "padding": "10px",
                    "boxSizing": "border-box",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd",
                    "resize": "vertical"
                }
            })
        ),
        
        # Tags field
        html.div({"style": {"marginBottom": "20px"}},
            html.label({"style": {"display": "block", "marginBottom": "5px", "fontWeight": "bold"}}, "Tags (comma separated):"),
            html.input({
                "type": "text",
                "value": tags,
                "onChange": lambda e: handle_input_change(e, set_tags),
                "style": {
                    "width": "100%",
                    "padding": "10px",
                    "boxSizing": "border-box",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd"
                }
            })
        ),
        
        # Buttons
        html.div({"style": {"display": "flex", "justifyContent": "space-between"}},
            html.button({
                "onClick": lambda _: set_page("home"),
                "style": {
                    "padding": "10px 20px",
                    "backgroundColor": "#95a5a6",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer"
                }
            }, "Cancel"),
            
            html.button({
                "onClick": update_article,
                "style": {
                    "padding": "10px 20px",
                    "backgroundColor": "#2196F3",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer"
                }
            }, "Update Article")
        )
    )