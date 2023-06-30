from django import template

register = template.Library()

bad_words = {
    'Редиска': 'Ре*****',
    'редиска': 'ре*****'
}


@register.filter()
def censor(value):
    text = value
    for r in bad_words.items():
        text = text.replace(r[0], r[1])
    return text
