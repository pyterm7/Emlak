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