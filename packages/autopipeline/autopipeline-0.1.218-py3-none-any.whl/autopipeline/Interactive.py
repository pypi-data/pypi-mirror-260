import pandas as pd
import os
from openai import OpenAI
from .PipelineGen import pipeline_gen
from .Mapping import base_table_gen
from .Filter import check_vague


def load_data(dataframe, desc, desc_file=True):
    # Load DataFrame
    try:
        table = pd.read_csv(dataframe)  # or pd.read_excel for Excel files
    except Exception as e:
        print(f"Failed to load DataFrame: {e}")
        return
    if desc_file:
        try:
            with open(desc, 'r') as file:
                description = file.read()
        except:
            print(f"Failed to load description: {e}")
            return
    else:
        description = desc
    
    return table, description

def formalize_desc(d):
    res = ""
    for column_name, column_desc in d.items():
        res += "'" + column_name + "' column contains " 
        res += column_desc + "; "
        # if "column-value" in d and len(d["column-value"]) > 0:
        #     res += "IMPORTANT: the values in '"+d["column-name"]+"' column are "+d["column-desc"] + "; "
    return res

def pipeline(query, table_ptr, description, verbose = False, openai_key = "OPENAI_API_KEY", openai_org_id = "OPENAI_ORG"):
    # if openai_key != None:
    #     OPENAI_API_KEY=openai_key
    #     os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    #     openai.api_key = os.environ["OPENAI_API_KEY"]

    # if openai_org_id != None:
    #     OPENAI_ORGANIZATION = openai_org_id
    #     os.environ["OPENAI_ORG"] = OPENAI_ORGANIZATION
    #     openai.organization=os.environ["OPENAI_ORG"]
    client = OpenAI(api_key=os.environ.get(openai_key), organization=os.environ.get(openai_org_id))

    table = table_ptr.copy()
    columns = str(table.columns.tolist())

    print("********** Checking Query...")
    precheck, functions = check_vague(query, columns, description, verbose, client)
    # precheck = precheck["content"]
    precheck = precheck.content
    if verbose:
        print("########## Precheck Result:", precheck)
        print("\n")
    ls = precheck.split('#')
    res = ls[0]
    hint = ls[1]
    if res == "False":
        print("########## Feedback: ", hint)
        print("\n")
        if verbose: # print functions only when verbose
            print("\nThe supported function list is as follows: \n" + functions)
        print("Please Be More Detailed on Query.")
        print("\n")
        return None, table
    if "WARNING" in hint:
        warning_msg = "WARNING: "+hint.split("WARNING:")[1].strip()
        print("########## "+warning_msg)
        user_reponse = str(input("Proceed? [Y/n]"))
        if user_reponse == "Y":
            hint = hint.split("WARNING")[0].strip()
        else:
            return None, table
    print("********** Query Check Pass!")

    require_new, feedback, result, table = pipeline_gen(query, table, description, hint, verbose, table_type="pd")
    if require_new:
        print("########## Feedback: ", feedback)
        print("\n")
        print("Please Be More Detailed on Query.")
        print("\n")
    else:
        print("Succeed!")
        print("\n")
    return result, table

def interactive_pipeline(table, description):
    require_new = True
    # table, enum, description = base_table_gen()
    while require_new:
        print("-----------------------------")
        query = str(input("Please enter your query: "))
        print("\n")
        columns = str(table.columns.tolist())
        precheck, functions = check_vague(query, columns, description)
        precheck = precheck["content"]
        print("########## Precheck Result:", precheck)
        print("\n")
        ls = precheck.split('#')
        res = ls[0]
        hint = ls[1]
        if res == "False":
            print("########## Feedback: ", hint)
            print("\n")
            print("\nThe supported function list is as follows: \n" + functions)
            require_new = True
            continue
        require_new, feedback = pipeline_gen(query, table, description, table_type="pd")
        if require_new:
            print("########## Feedback: ", feedback)
            print("\n")


def _interactive_pipeline():
    # Prompt user for file path
    file_path = input("Please enter the file path for your DataFrame: ")

    # Load DataFrame
    try:
        table = pd.read_csv(file_path)  # or pd.read_excel for Excel files
    except Exception as e:
        print(f"Failed to load DataFrame: {e}")
        return
    
    # Prompt user for file path
    file_path = input("Please enter the description for your DataFrame: ")

    # Load DataFrame
    try:
        with open(file_path, 'r') as file:
            description = file.read()
    except:
        description = file_path
    require_new = True
    # table, enum, description = base_table_gen()
    while require_new:
        print("-----------------------------")
        query = str(input("Please enter your query: "))
        require_new, feedback = pipeline_gen(query, table, description, table_type="pd")
        if require_new:
            print("########## Feedback: ", feedback)
            print("\n")

if __name__ == "__main__":
    interactive_pipeline()