import re
import inspect
from .util import formalize_desc, check_alias
import autopipeline

def wrapper(callback_name, input_vars, para_dict, desc_dict, enum, description, verbose, dot, client):

    callback = autopipeline._callbacks[callback_name]
    if not (callback and callable(callback)):
        print("Function " + callback_name+ " undefined.")

    # check_alias
    new_description = formalize_desc(desc_dict)
    matches = re.findall(r"\[(.*?)\]", new_description)
    para_ls = []
    for match in matches:
        para_ls.append(para_dict[match])

    replacement_iter = iter(para_ls)

    # Function to get the next replacement value
    def replacement(match):
        return next(replacement_iter, '')

    # Use re.sub with a function as the replacement
    new_description = re.sub(r"\[.*?\]", replacement, new_description)

    col = check_alias(enum, description, new_description, verbose, client)
    if len(col) > 0:
        for para_key in para_dict:
            dot.edge(para_dict[para_key], col, callback_name)
        return table, enum, description, dot

    table = callback(*input_vars)
    enum = list(table.columns)
    description += " " + new_description
    new_cols = list(desc_dict.keys())
    for new_col in new_cols:
        matches = re.findall(r"\[(.*?)\]", new_col)
        para_ls = []
        for match in matches:
            para_ls.append(para_dict[match])
        replacement_iter = iter(para_ls)
        new_col = re.sub(r"\[.*?\]", replacement, new_col)
        for para_key in para_dict:
            dot.edge(para_dict[para_key], new_col, callback_name)

    return table, enum, description, dot
