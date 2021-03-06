from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_property(obj, key):
    # print(obj.fields)
    return getattr(obj, key, None)
