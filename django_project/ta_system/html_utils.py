from django.utils.html import format_html


def ul(elements, style=""):
    lis = ''.join(['<li>{}</li>' for _ in elements])
    ul = f'<ul style="{style}">{lis}</ul>'
    return format_html(ul, *elements)


def ul_abbreviated(elements, style=""):
    ul_abbreviated = ul(elements, style)
    ul_abbreviated += '<div>{}</div>'
    return format_html(ul_abbreviated, '...')


def generate_ul(model_objects, display_func, style, max_to_display=None):
    if model_objects:
        object_names = [display_func(obj) for obj in model_objects]
        if max_to_display and len(object_names) > max_to_display:
            object_names = object_names[:max_to_display]
            return ul_abbreviated(object_names, style)
        return ul(object_names, style)
    return '---'


def link(content, href, style=""):
    link = '<a href={} target="_blank" style={}>{}</a>'
    return format_html(link, href, style, content)
