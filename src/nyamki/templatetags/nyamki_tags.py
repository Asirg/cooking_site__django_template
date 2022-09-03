from datetime import datetime
from django import template

from nyamki.models import Article, Category, Label, Keyword

register = template.Library()

@register.simple_tag()
def get_recipe_categories():
    return Category.objects.filter(for_article=0)

@register.simple_tag()
def get_recipe_labels():
    return Label.objects.all()

@register.simple_tag()
def get_recipe_keywords():
    return Keyword.objects.all()

@register.simple_tag()
def get_article_category():
    return Category.objects.filter(for_article=1)

@register.simple_tag()
def get_articles_list(type, count):
    queryset = Article.objects.filter(type__name_ru=type, name__isnull=False).order_by("date")[:count]
    return queryset

@register.filter()
def get_item(value, key):
    return value[key]

@register.filter()
def floatdot(value, count=1):
    return f"{value:.{count}f}"


html_answer = lambda username: f"""
                                  <img src="/media/answer.png" class="comment-header-answer-icon">
                                  <span class="comment-header-answer">{ username }</span>
                               """
html_editing = lambda content, comment_id:  f"""
                                                <a href="#formComment" onclick="EditingComment('{ content }', '{ comment_id }')" class="comment-action">
                                                    ● Редактировать
                                                </a>
                                            """
def template_comment(user_avatar, username, date, content, parent_username, comment_id, user_id, comment_user_id,   counter):
    hrml = f"""<div class="comment-wrapper">
                {"<span class='marker-depth'>●</span>" * counter}
                <img src="{ user_avatar}"  class="comment-user-avatar">
                <div class="comment-block">
                    <div class="comment-header">
                        { username }
                        { html_answer(parent_username) if parent_username else ""}
                        <span class="comment-header-date">● { datetime.strftime(date, "%y-%m-%d %H:%M:%S") }</span>
                    </div>
                    <div class="comment-content">{ content }</div>
                    <div class="comment-footer">
                        <a href="#formComment" onclick="addComment('{ username }', '{ comment_id }')" class="comment-action">
                            ● Ответить
                        </a>
                        { html_editing(content, comment_id) if user_id == comment_user_id else ""}
                    </div>
                </div>
            </div>
    """
    return hrml

@register.simple_tag()
def comments_tree(comments, user, parent=False, counter=0):
    html = ""
    
    for comment in comments.filter(parent__isnull=True) if not parent else comments:
        childs = comment.comment_set.all()

        html += template_comment(
            user_avatar = comment.user.profile.useravatar.image.url,
            username = user.username,
            date = comment.date ,
            content = comment.content,
            parent_username = comment.parent.user.username if comment.parent else False,
            comment_id = comment.id,
            user_id = user.id,
            comment_user_id = comment.user.id,
            counter=counter,
        )

        if childs:
            html += "<div class='comments_branch'>"
            html += comments_tree(childs, user, True, counter+1)
            html += "</div>"

    return html

# {% for comment in comments %}
#             <div class="comment-wrapper">
                
#                 <img src="{{comment.user.profile.useravatar.image.url}}"  class="comment-user-avatar">

#                 <div class="comment-block">

#                     <div class="comment-header">
#                         {{ user.username }}
#                         {% if comment.parent.user %}
#                             <img src="/media/answer.png" class="comment-header-answer-icon">
#                             <span class="comment-header-answer">
#                                 {{ comment.parent.user }}
#                             </span>
#                         {% endif %}
#                         <span class="comment-header-date">
#                             ● {{ comment.date }}
#                         </span>
#                     </div>
                    
#                     <div class="comment-content">
#                         {{ comment.content }}
#                     </div>

#                     <div class="comment-footer">
#                         <a href="#formComment" onclick="addComment('{{ comment.user.username }}', '{{ comment.id }}')" class="comment-action">
#                             ● Ответить
#                         </a>
#                         {% if user.id == comment.user.id %}
#                             <a href="#formComment" onclick="EditingComment('{{ comment.content }}', '{{ comment.id }}')" class="comment-action">
#                                 ● Редактировать
#                             </a>
#                         {% endif %}
#                     </div>

#                 </div>
#             </div>
#         {% endfor %}