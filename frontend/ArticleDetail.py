import reactpy
from reactpy import html
from Comments import Comments

@reactpy.component
def ArticleDetail(selected_article, set_page, token=None, user=None):
    if not selected_article:
        return html.div({}, "No article selected.")
    
    return html.div(
        {"style": {"padding": "1rem"}},
        html.h1({"style": {"marginBottom": "1rem"}}, selected_article.get("title", "No Title")),
        html.div(
            {"style": {"marginBottom": "1rem", "color": "#666"}},
            f"Posted by: {selected_article.get('author', 'Anonymous')}"
        ),
        html.div(
            {"style": {"marginBottom": "2rem", "lineHeight": "1.6"}},
            selected_article.get("content", "No content")
        ),
        Comments(selected_article.get("id"), token, user),
        html.button({
            "onClick": lambda e: set_page("home"), 
            "style": {
                "marginTop": "2rem",
                "padding": "0.5rem 1rem",
                "backgroundColor": "#ccc",
                "border": "none",
                "borderRadius": "4px",
                "cursor": "pointer"
            }
        }, "Back to Home")
    )
