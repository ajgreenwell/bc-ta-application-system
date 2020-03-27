from django.utils.html import format_html


def ul(elements, style=""):
    lis = ''.join(['<li>{}</li>' for _ in elements])
    ul = f'<ul style="{style}">{lis}</ul>'
    return format_html(ul, *elements)


def link(content, href, style=""):
    link = '<a href={} target="_blank" style={}>{}</a>'
    return format_html(link, href, style, content)
