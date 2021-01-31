from fuzzywuzzy import fuzz


def validation(g, a):
    while g:
        g = g.lower()
        a = a.lower()
        g, a = clean_chars(g, a)
        g = check_prefix(g)
        a = split_answer(a)
        if not final_check(g, a):
            return False
        return True
    return False


def check_prefix(g):
    prefix = ['what is ', 'who is ', 'where is ']
    for ans in prefix:
        if g.lower().startswith(ans):
            return g.replace(ans, '')
    return False


def clean_chars(g, a):
    g = g.translate({ord(i): None for i in "\"?!@#$%^&*()-_=+/\\[]{};:`~"})
    a = a.replace('&', 'and')
    a = a.replace(' acceptable)', '')
    a = a.replace(' accepted)', '')
    a = a.translate({ord(i): None for i in "\"?!@#$%^&*)-_=+\\[]{};:`~"})
    return g, a


def split_answer(a):
    if '(' in a:
        a = a.split('(')
    elif '/' in a:
        a = a.split('/')
    return a


def final_check(g, a):
    if isinstance(a, list):
        for ans in a:
            if fuzz.ratio(g, ans) > 80 or fuzz.token_set_ratio(g, ans) > 90:
                return True
    else:
        if fuzz.ratio(g, a) > 80 or fuzz.token_set_ratio(g, a) > 90:
            return True
    return False
