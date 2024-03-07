import re
from .util import formalize_desc, check_alias

def wrapper(callback, input_vars, desc_dict, enum, description, verbose, dot, client):

    # check_alias
    new_description = formalize_desc(desc_dict)
    matches = re.findall(r"\[(.*?)\]", new_description)
    para_ls = []
    for match in matches:
        para_ls.append(input_vars[match])

    replacement_iter = iter(para_ls)

    # Function to get the next replacement value
    def replacement(match):
        return next(replacement_iter, '')

    # Use re.sub with a function as the replacement
    new_description = re.sub(r"\[.*?\]", replacement, new_description)

    col = check_alias(enum, description, new_description, verbose, client)
    if len(col) > 0:
        for i in range(1, len(input_vars)):
            dot.edge(input_vars[i], col, callback.__name__)
        return table, enum, description, dot

    table = callback(*input_vars)
    enum = list(table.columns)
    description += " " + new_description
    new_cols = list(desc_dict.keys())
    for new_col in new_cols:
        for i in range(1, len(input_vars)):
            dot.edge(input_vars[i], new_col, callback.__name__)

    return table, enum, description, dot
