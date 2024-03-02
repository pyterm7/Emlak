from django import template
register = template.Library()

@register.filter(name='cast2int')
def cast2int(value):
    try: 
        value = int(value)
        value = format(value, ',d')
        """
            # value = str(value)[::-1]
            # empty = ""
            # index = 1 
            # for char in value:
            #     empty += char 
            #     if index % 3 == 0 :
            #         empty+=","
            #     index += 1
            # return empty[::-1].strip(",")
        """
        return value
    except: return 0

@register.filter(name='exclude_page_param')
def exclude_page_param(value):
    if value.find("page") != -1:
        value = value[0:value.index("page")]
    if value.find("?") == -1: value += "?"
    else: value += "&"
    return value