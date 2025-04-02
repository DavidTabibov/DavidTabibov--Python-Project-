import reactpy
from reactpy import html, hooks
import requests

API_BASE = "http://localhost:8000/api"

@reactpy.component
def Comments(article_id, token=None, user=None):
    comments, set_comments = hooks.use_state([])
    new_comment, set_new_comment = hooks.use_state("")
    editing_comment, set_editing_comment = hooks.use_state(None)
    edited_content, set_edited_content = hooks.use_state("")
    error_msg, set_error_msg = hooks.use_state("")

    def handle_input_change(e, setter):
        if isinstance(e, dict) and 'target' in e and 'value' in e['target']:
            setter(e['target']['value'])
        else:
            setter(e)

    def fetch_comments():
        try:
            url = f"{API_BASE}/articles/{article_id}/comments/"
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token.get('access')}"
                
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"Comments data: {data}")
                set_comments(data)
            else:
                set_comments([])
        except Exception as e:
            print("Error fetching comments:", e)
            set_comments([])

    hooks.use_effect(fetch_comments, [article_id])

    def add_comment(e):
        if not token:
            set_error_msg("You must be logged in to add a comment")
            return
            
        if not new_comment.strip():
            set_error_msg("Comment content cannot be empty")
            return
            
        try:
            url = f"{API_BASE}/articles/{article_id}/comments/"
            headers = {"Authorization": f"Bearer {token.get('access')}"}
            payload = {
                "content": new_comment
                # article_id לא נשלח - הבאקאנד יטפל בזה
            }
            
            print(f"Sending comment: {payload}")
            response = requests.post(url, json=payload, headers=headers)
            print(f"Comment response: {response.status_code}")
            
            if response.status_code in [200, 201]:
                set_new_comment("")
                set_error_msg("")
                # רענון התגובות לאחר הוספה
                fetch_comments()
            else:
                try:
                    error_data = response.json()
                    print(f"Error data: {error_data}")
                    error_message = f"Error adding comment: {error_data}"
                    set_error_msg(error_message)
                except:
                    set_error_msg(f"Error adding comment: {response.status_code}")
        except Exception as e:
            print("Error adding comment:", e)
            set_error_msg(f"Error adding comment: {str(e)}")

    def start_edit(comment):
        set_editing_comment(comment.get("id"))
        set_edited_content(comment.get("content", ""))

    def save_edit():
        if not edited_content.strip():
            set_error_msg("Comment content cannot be empty")
            return
            
        try:
            # שינוי ה-URL לכלול /update/ בסוף
            url = f"{API_BASE}/comments/{editing_comment}/update/"
            headers = {"Authorization": f"Bearer {token.get('access')}"}
            payload = {"content": edited_content}
            
            response = requests.put(url, json=payload, headers=headers)
            if response.status_code in [200, 204]:
                set_editing_comment(None)
                set_edited_content("")
                set_error_msg("")
                # רענון התגובות לאחר עריכה
                fetch_comments()
            else:
                set_error_msg(f"Error editing comment: {response.text}")
        except Exception as e:
            print("Error editing comment:", e)
            set_error_msg(f"Error editing comment: {str(e)}")

    def cancel_edit():
        set_editing_comment(None)
        set_edited_content("")

    def delete_comment(comment_id):
        try:
            # שינוי ה-URL לכלול /delete/ בסוף
            url = f"{API_BASE}/comments/{comment_id}/delete/"
            headers = {"Authorization": f"Bearer {token.get('access')}"}
            
            response = requests.delete(url, headers=headers)
            if response.status_code in [200, 204]:
                # רענון התגובות לאחר מחיקה
                fetch_comments()
            else:
                set_error_msg(f"Error deleting comment: {response.text}")
        except Exception as e:
            print("Error deleting comment:", e)
            set_error_msg(f"Error deleting comment: {str(e)}")

    def can_edit_delete(comment):
        # בדיקה אם המשתמש יכול לערוך או למחוק תגובה (היוצר או מנהל)
        if not user:
            return False
        return comment.get("user") == user.get("username") or user.get("is_staff", False)

    comment_items = []
    for index, comment in enumerate(comments):
        if editing_comment == comment.get("id"):
            # טופס עריכה
            comment_items.append(
                html.li(
                    {"key": comment.get("id", index), "style": {"marginBottom": "1rem", "padding": "1rem", "backgroundColor": "#f9f9f9", "borderRadius": "4px"}},
                    html.div(
                        {},
                        html.div(
                            {"style": {"display": "flex", "justifyContent": "space-between", "marginBottom": "0.5rem"}},
                            html.strong({}, comment.get("user", "Anonymous")),
                            html.span({}, comment.get("created_at", ""))
                        ),
                        html.textarea({
                            "value": edited_content,
                            "onChange": lambda e: handle_input_change(e, set_edited_content),
                            "style": {"width": "100%", "minHeight": "60px", "padding": "0.5rem", "marginBottom": "0.5rem"}
                        }),
                        html.div(
                            {},
                            html.button({
                                "onClick": lambda e: save_edit(), 
                                "style": {
                                    "marginRight": "0.5rem",
                                    "padding": "0.3rem 0.7rem",
                                    "backgroundColor": "#4CAF50",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "4px",
                                    "cursor": "pointer"
                                }
                            }, "Save"),
                            html.button({
                                "onClick": lambda e: cancel_edit(), 
                                "style": {
                                    "padding": "0.3rem 0.7rem",
                                    "backgroundColor": "#ccc",
                                    "border": "none",
                                    "borderRadius": "4px",
                                    "cursor": "pointer"
                                }
                            }, "Cancel")
                        )
                    )
                )
            )
        else:
            # תצוגת תגובה רגילה
            comment_items.append(
                html.li(
                    {"key": comment.get("id", index), "style": {"marginBottom": "1rem", "padding": "1rem", "backgroundColor": "#f9f9f9", "borderRadius": "4px"}},
                    html.div(
                        {},
                        html.div(
                            {"style": {"display": "flex", "justifyContent": "space-between", "marginBottom": "0.5rem"}},
                            html.strong({}, comment.get("user", "Anonymous")),
                            html.span({}, comment.get("created_at", ""))
                        ),
                        html.p({}, comment.get("content", "")),
                        html.div(
                            {"style": {"textAlign": "right"}},
                            html.button({
                                "onClick": lambda e, c=comment: start_edit(c), 
                                "style": {
                                    "marginRight": "0.5rem",
                                    "padding": "0.3rem 0.7rem",
                                    "backgroundColor": "#2196F3",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "4px",
                                    "cursor": "pointer",
                                    "display": "inline-block" if can_edit_delete(comment) else "none"
                                }
                            }, "Edit"),
                            html.button({
                                "onClick": lambda e, id=comment.get("id"): delete_comment(id), 
                                "style": {
                                    "padding": "0.3rem 0.7rem",
                                    "backgroundColor": "#f44336",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "4px",
                                    "cursor": "pointer",
                                    "display": "inline-block" if can_edit_delete(comment) else "none"
                                }
                            }, "Delete")
                        ) if token else html.div({})
                    )
                )
            )

    return html.div(
        {},
        html.h2({"style": {"borderBottom": "2px solid #eee", "paddingBottom": "0.5rem"}}, "Comments"),
        
        # רשימת תגובות
        html.div(
            {"style": {"marginBottom": "2rem"}},
            html.ul(
                {"style": {"listStyleType": "none", "padding": "0"}},
                comment_items
            ) if comments else html.p({}, "No comments yet.")
        ),
        
        # טופס להוספת תגובה
        html.div(
            {"style": {"marginTop": "2rem", "display": "block" if token else "none"}},
            html.h3({}, "Add Comment"),
            html.textarea({
                "placeholder": "Write your comment here...",
                "value": new_comment,
                "onChange": lambda e: handle_input_change(e, set_new_comment),
                "style": {"width": "100%", "minHeight": "100px", "padding": "0.5rem", "marginBottom": "0.5rem"}
            }),
            html.button({
                "onClick": add_comment, 
                "style": {
                    "padding": "0.5rem 1rem",
                    "backgroundColor": "#4CAF50",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer"
                }
            }, "Submit Comment"),
            html.div({"style": {"color": "red", "marginTop": "0.5rem"}}, error_msg)
        ),
        
        # הודעה למשתמשים לא מחוברים
        html.div(
            {"style": {"marginTop": "2rem", "display": "block" if not token else "none"}},
            html.p({}, "You must be logged in to comment")
        )
    )