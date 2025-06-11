from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """辞書からキーで値を取得する"""
    if dictionary and key in dictionary:
        return dictionary.get(key)
    return 0

@register.filter
def attr(obj, attr_name):
    """オブジェクトの属性を動的に取得する"""
    return getattr(obj, attr_name, None)
