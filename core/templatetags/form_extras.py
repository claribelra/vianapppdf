from django import template

register = template.Library()

def add_class(field, error_class):
    css = field.field.widget.attrs.get('class', '')
    if error_class:
        css = (css + ' ' + error_class).strip()
    return field.as_widget(attrs={**field.field.widget.attrs, 'class': css})

register.filter('add_class', add_class)
