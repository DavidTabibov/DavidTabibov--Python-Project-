import reactpy
from reactpy import html, hooks
import requests

API_BASE = "http://localhost:8000/api"

@reactpy.component
def Home(set_page, set_selected_article, token=None, user=None):
    articles, set_articles = hooks.use_state([])
    query, set_query = hooks.use_state("")
    displayed_count, set_displayed_count = hooks.use_state(3)
    error, set_error = hooks.use_state("")

    def handle_input_change(e, setter):
        if isinstance(e, dict) and 'target' in e and 'value' in e['target']:
            setter(e['target']['value'])
        else:
            setter(e)

    def fetch_articles():
        try:
            url = f"{API_BASE}/articles/"
            if query:
                url += f"?search={query}"
            
            print(f"Fetching from URL: {url}")
            
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token.get('access')}"  # תוקנה כאן, הסוגר המיותר הוסר
                
            response = requests.get(url, headers=headers)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Received data: {data}")
                set_articles(data)
                set_error("")
            else:
                print(f"Error response: {response.text}")
                set_articles([])
                set_error(f"Error loading articles: {response.status_code}")
        except Exception as e:
            print(f"Exception fetching articles: {e}")
            set_articles([])
            set_error(f"Error: {str(e)}")

    hooks.use_effect(fetch_articles, [query])

    def on_article_click(article):
        set_selected_article(article)
        set_page("article_detail")

    def on_load_more(e):
        set_displayed_count(displayed_count + 3)
        
    def create_article(e):
        set_page("create_article")
    
    def edit_article(article):
        set_selected_article(article)
        set_page("edit_article")
        
    def delete_article(article_id):
        if not token:
            set_error("You must be logged in to delete articles")
            return
            
        try:
            url = f"{API_BASE}/articles/{article_id}/"
            headers = {"Authorization": f"Bearer {token.get('access')}"}
            
            response = requests.delete(url, headers=headers)
            if response.status_code in [200, 204]:
                # Refresh articles after deletion
                fetch_articles()
                set_error("Article deleted successfully")
            else:
                set_error(f"Error deleting article: {response.status_code}")
        except Exception as e:
            print(f"Error deleting article: {e}")
            set_error(f"Error: {str(e)}")

    # Check if user is admin
    is_admin = user and user.get('is_staff', False)

    # Create admin controls
    admin_controls = None
    if is_admin:
        admin_controls = html.div(
            {"style": {"marginBottom": "20px"}},
            html.button({
                "onClick": create_article,
                "style": {
                    "padding": "10px 15px",
                    "backgroundColor": "#4CAF50",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "fontSize": "16px"
                }
            }, "Create New Article")
        )

    # Improved article list rendering with better styling
    article_items = []
    for i, article in enumerate(articles[:displayed_count]):
        # Create admin buttons
        admin_buttons = []
        if is_admin:
            admin_buttons = [
                html.button({
                    "onClick": lambda e, a=article: edit_article(a),
                    "style": {
                        "padding": "5px 10px",
                        "backgroundColor": "#2196F3",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "4px",
                        "cursor": "pointer",
                        "marginRight": "10px"
                    }
                }, "Edit"),
                html.button({
                    "onClick": lambda e, id=article.get("id"): delete_article(id),
                    "style": {
                        "padding": "5px 10px",
                        "backgroundColor": "#f44336",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "4px",
                        "cursor": "pointer"
                    }
                }, "Delete")
            ]
            
        article_items.append(
            html.div(
                {"key": i, "style": {
                    "marginBottom": "20px",
                    "padding": "20px",
                    "border": "1px solid #e0e0e0",
                    "borderRadius": "5px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "backgroundColor": "white"
                }},
                html.div(
                    {"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center"}},
                    html.h3(
                        {"onClick": lambda e, a=article: on_article_click(a),
                         "style": {
                             "cursor": "pointer", 
                             "color": "#2c3e50",
                             "marginTop": "0",
                             "marginBottom": "10px"
                         }},
                        article.get("title", "No Title")
                    ),
                    html.div({}, admin_buttons) if is_admin else html.div({})
                ),
                html.div(
                    {"style": {"fontSize": "14px", "color": "#7f8c8d", "marginBottom": "10px"}},
                    f"Author: {article.get('author', 'Unknown')} | Published: {article.get('pub_date', '').split('T')[0] if article.get('pub_date') else ''}"
                ),
                html.p(
                    {"style": {"marginBottom": "0", "lineHeight": "1.5"}},
                    article.get("content", "")[:150] + ("..." if len(article.get("content", "")) > 150 else "")
                )
            )
        )

    return html.div(
        {"style": {
            "maxWidth": "800px", 
            "margin": "0 auto",
            "padding": "0 20px"
        }},
        html.h1(
            {"style": {
                "borderBottom": "2px solid #eee",
                "paddingBottom": "10px",
                "marginBottom": "20px",
                "color": "#2c3e50"
            }}, 
            "Latest Articles"
        ),
        html.div({"style": {"color": "red", "marginBottom": "10px"}}, error),
        
        # Add admin controls
        admin_controls,
        
        html.div(
            {"style": {
                "marginBottom": "20px",
                "display": "flex"
            }},
            html.input({
                "type": "text",
                "placeholder": "Search articles...",
                "value": query,
                "onChange": lambda e: handle_input_change(e, set_query),
                "style": {
                    "padding": "10px",
                    "borderRadius": "4px",
                    "border": "1px solid #ddd",
                    "width": "100%",
                    "fontSize": "16px"
                }
            })
        ),
        html.div({}, article_items) if articles else html.div(
            {"style": {
                "padding": "20px", 
                "textAlign": "center", 
                "backgroundColor": "#f9f9f9", 
                "borderRadius": "5px"
            }}, 
            "No articles found. Please check the server connection."
        ),
        html.div(
            {"style": {"textAlign": "center", "marginTop": "20px", "marginBottom": "40px"}},
            html.button({
                "onClick": on_load_more, 
                "style": {
                    "padding": "10px 20px",
                    "backgroundColor": "#3498db",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "fontSize": "16px"
                }
            }, "Load More")
            if len(articles) > displayed_count else html.div({})
        )
    )
