import glob
import os
import re

from memex import MemexSession


def extract_variables(content):
    variables = re.findall(r"\{(\w+)\}", content)
    return sorted(set(variables), key=variables.index)


def bootstrap_project(project_path):
    session = MemexSession()

    # Handle markdown files in the prompts directory
    for md_file_path in glob.glob(os.path.join(project_path, "prompts", "*.md")):
        with open(md_file_path, "r") as md_file:
            content = md_file.read()
        name = os.path.splitext(os.path.basename(md_file_path))[0]
        variables = extract_variables(content)
        print(f"Saving prompt as function: {name}")
        session.save_prompt_as_function(name, content, variables)

    # Handle SQL files in the queries directory
    for sql_file_path in glob.glob(os.path.join(project_path, "queries", "*.sql")):
        with open(sql_file_path, "r") as sql_file:
            query = sql_file.read()
        name = os.path.splitext(os.path.basename(sql_file_path))[0]
        print(f"Saving query: {name}")
        session.save_query({"name": name, "query": query})

    file_types = ["*.csv", "*.parquet"]
    # Handle files in the data directory
    for file_type in file_types:
        for csv_file_path in glob.glob(os.path.join(project_path, "data", file_type)):
            with open(csv_file_path, "rb") as csv_file:
                file_name = os.path.basename(csv_file_path)
                print(f"Uploading dataset: {file_name}")
                session.upload_dataset(csv_file, file_name)
