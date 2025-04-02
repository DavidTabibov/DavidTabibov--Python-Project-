import sys
from pathlib import Path

# מוסיף את התיקייה הנוכחית לנתיבי החיפוש של Python
sys.path.insert(0, str(Path(__file__).parent))

import reactpy
from reactpy import html, hooks, run
from Navigation import Navigation
from Home import Home
from ArticleDetail import ArticleDetail
from Login import Login
from Register import Register
from CreateArticle import CreateArticle
from EditArticle import EditArticle

@reactpy.component
def App():
    page, set_page = hooks.use_state("home")
    selected_article, set_selected_article = hooks.use_state(None)
    token, set_token = hooks.use_state(None)
    user, set_user = hooks.use_state(None)
    
    def login_user(token_data, user_data):
        set_token(token_data)
        set_user(user_data)
        
    def logout_user():
        set_token(None)
        set_user(None)
    
    def render_page():
        if page == "home":
            return Home(set_page, set_selected_article, token, user)
        elif page == "article_detail":
            return ArticleDetail(selected_article, set_page, token, user)
        elif page == "login":
            return Login(set_page, login_user)
        elif page == "register":
            return Register(set_page, login_user)
        elif page == "create_article":
            return CreateArticle(set_page, token)
        elif page == "edit_article":
            return EditArticle(selected_article, set_page, token)
        else:
            return html.div("Page not found.")
    
    return html.div(
        Navigation(page, set_page, user, logout_user),
        render_page()
    )

if __name__ == "__main__":
    run(App, port=3000)