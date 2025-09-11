from django import template
register = template.Library()

@register.filter
def get_user_by_email(users, email):
    for u in users:
        if u.email == email:
            return u
    return None
