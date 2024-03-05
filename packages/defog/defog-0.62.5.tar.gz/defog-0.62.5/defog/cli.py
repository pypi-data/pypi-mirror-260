import datetime
import decimal
import pwinput
import json
import os
import re
import shutil
import subprocess
import sys
import requests
import time

import defog
from defog.util import get_feedback, parse_update
from prompt_toolkit import prompt

USAGE_STRING = """
Usage: defog <command>

Available commands:
    init\t\t\tSetup defog credentials and your database connection
    gen <table1> <table2>\tSpecify tables to generate schema for
    update <csv>\t\tupdate schema (path to CSV) to defog
    query\t\t\tRun a query
    deploy <gcp|aws>\t\tDeploy a defog server as a cloud function
    quota\t\t\tCheck your API quota limits
    docs\t\t\tPrint documentation
    serve\t\t\tServe a defog server locally
"""

home_dir = os.path.expanduser("~")


def main():
    if len(sys.argv) < 2:
        print(USAGE_STRING)
        sys.exit(1)
    if sys.argv[1] == "init":
        init()
    if sys.argv[1] == "gen":
        gen()
    elif sys.argv[1] == "update":
        update()
    elif sys.argv[1] == "query":
        query()
    elif sys.argv[1] == "deploy":
        deploy()
    elif sys.argv[1] == "quota":
        quota()
    elif sys.argv[1] == "docs":
        # TODO
        raise NotImplementedError("docs not implemented yet")
    elif sys.argv[1] == "serve":
        serve()
    elif sys.argv[1] == "serve-webserver":
        serve_webserver()
    elif sys.argv[1] == "serve-static":
        serve_static()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        print(USAGE_STRING)
        sys.exit(1)


def init():
    """
    Initialize defog by creating a config file at ~/.defog/connection.json
    """
    # print welcome message
    print("Welcome to \033[94mdefog.ai\033[0m!\n")
    # check if .defog/connection.json exists
    # if it does, ask if user wants to overwrite
    # if it doesn't, create it
    filepath = os.path.join(home_dir, ".defog", "connection.json")
    if os.path.exists(filepath):
        print(
            "It looks like you've already initialized defog. Do you want to re-enter your database credentials? (y/n)"
        )
        overwrite = prompt().strip()
        if overwrite.lower() != "y":
            print("We'll keep your existing config. No changes were made.")
            sys.exit(0)
        else:
            print("We'll create a new config file at ~/.defog/connection.json")
    else:
        print("We'll create a new config file at ~/.defog/connection.json")
        if not os.path.exists(os.path.join(home_dir, ".defog")):
            os.mkdir(os.path.join(home_dir, ".defog"))

    # prompt user for defog api key if not in environment variable
    if os.environ.get("DEFOG_API_KEY"):
        print(
            "We found your DEFOG_API_KEY in your environment variables. We'll use that."
        )
        api_key = os.environ.get("DEFOG_API_KEY")
    else:
        print(
            "Please enter your DEFOG_API_KEY. You can get it from https://defog.ai/accounts/dashboard/ and creating an account:"
        )
        api_key = prompt().strip()

    # prompt user for db_type
    print(
        "What database are you using? Available options are: "
        + ", ".join(defog.SUPPORTED_DB_TYPES)
    )
    db_type = prompt().strip()
    db_type = db_type.lower()
    while db_type not in defog.SUPPORTED_DB_TYPES:
        print(
            "Sorry, we don't support that database yet. Available options are: "
            + ", ".join(defog.SUPPORTED_DB_TYPES)
        )
        db_type = prompt().strip()
        db_type = db_type.lower()
    # depending on db_type, prompt user for appropriate db_creds
    if db_type == "postgres" or db_type == "redshift":
        print("Please enter your database host:")
        host = prompt().strip()
        # check if host has http:// or https:// and remove it if it does
        if host.startswith("http://") or host.startswith("https://"):
            host = host.split("://")[1]
        print("Please enter your database port:")
        port = prompt().strip()
        print("Please enter your database name:")
        database = prompt().strip()
        print("Please enter your database user:")
        user = prompt().strip()
        password = pwinput.pwinput(
            prompt="Please enter your database password. This won't be displayed as you're typing for privacy reasons"
        )
        db_creds = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        }

    elif db_type == "mysql":
        print("Please enter your database host:")
        host = prompt().strip()
        print("Please enter your database name:")
        database = prompt().strip()
        print("Please enter your database user:")
        user = prompt().strip()
        print("Please enter your database password:")
        password = pwinput.pwinput(prompt="Please enter your database password:")
        db_creds = {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
        }
    elif db_type == "snowflake":
        print("Please enter your database account:")
        account = prompt().strip()
        print("Please enter your database warehouse:")
        warehouse = prompt().strip()
        print("Please enter your database user:")
        user = prompt().strip()
        password = pwinput.pwinput(prompt="Please enter your database password:")
        db_creds = {
            "account": account,
            "warehouse": warehouse,
            "user": user,
            "password": password,
        }
    elif db_type == "databricks":
        print("Please enter your databricks host:")
        host = prompt().strip()
        token = pwinput.pwinput(prompt="Please enter your databricks token:")
        print("Please add your http_path:")
        http_path = prompt().strip()
        print("Please enter your schema name (this is usually 'default'):")
        schema = prompt().strip()
        db_creds = {
            "server_hostname": host,
            "access_token": token,
            "http_path": http_path,
            "schema": schema,
        }
    elif db_type == "bigquery":
        print("Please enter your bigquery json key's path:")
        json_key_path = prompt().strip()
        db_creds = {
            "json_key_path": json_key_path,
        }

    # write to filepath and print confirmation
    with open(filepath, "w") as f:
        data = {"api_key": api_key, "db_type": db_type, "db_creds": db_creds}
        json.dump(data, f, indent=4)
    print(f"Your configuration has been saved to {filepath}.")

    # prompt user for tables that they would like to register
    print(
        "We're going to register your tables' schema with defog. Just hit enter to skip if you would like to do this later. You can use `defog gen` to generate a schema for your tables later."
    )
    print(
        "Please enter the names of the tables you would like to register, separated by a space:"
    )
    table_names = prompt().strip()
    table_name_list = re.split(r"\s+", table_names.strip())
    # if input is empty, exit
    if table_name_list == [""]:
        print("No tables were registered. Exiting.")
        sys.exit(0)
    else:
        print(
            "Do you want to automatically scan these tables to determine which column might be categorical? The distinct values in each categorical column will be sent to our server. (y/n)"
        )
        scan_option = prompt().strip()
        if scan_option.lower() == "y" or scan_option.lower() == "yes":
            scan = True
        else:
            scan = False
        df = defog.Defog(api_key=api_key, db_type=db_type, db_creds=db_creds)
        filename = df.generate_db_schema(table_name_list, scan=scan)
        pwd = os.getcwd()
        print(
            "Your schema has been generated and is available as a CSV file in this folder at:\n"
        )
        print(f"\033[1m{pwd}/{filename}\033[0m\n")

    print(
        "You can give us more context about your schema by editing the CSV above. Refer to our cookbook on how to do this here: https://defog.notion.site/Cookbook-for-schema-definitions-1650a6855ea447fdb0be75d39975571b#2ba1d37e243e4da3b8f17590b4a3e4e3.\n\nOnce you're done, you can just hit enter to upload the data in the CSV to Defog. If you would like to exit instead, just enter `exit`."
    )
    upload_option = prompt().strip()
    if upload_option == "exit":
        print("Exiting.")
        sys.exit(0)
    else:
        print(
            "We are now uploading this schema to Defog. This might take up to 30 seconds..."
        )
        resp = df.update_db_schema(filename)
        if resp["status"] == "success":
            print("Your schema has been updated. You're ready to start querying!")
        else:
            print("There was an error updating your schema:")
            print(resp)
            print("Please try again, or contact us at founders@defog.ai")
            sys.exit(1)

    print(
        "You're all set! You can now start querying your database using `defog query`."
    )

    print(
        f"You get started, try entering a sample question here, like how many rows are in the table {table_name_list[0]}?"
    )

    query = prompt("Enter your query here: ")
    while query != "e":
        resp = df.run_query(query, retries=3)
        if not resp["ran_successfully"]:
            print(f"Your query did not run successfully. Please try again.")
        else:
            print("Your question generated the following query:\n")
            print(f"\033[1m{resp['query_generated']}\033[0m\n")
            print("Results:\n")
            # print results in tabular format using 'columns' and 'data' keys
            try:
                print_table(resp["columns"], resp["data"])
            except:
                print(resp)
        query = prompt("Enter another query, or type 'e' to exit: ")

    print("Exiting.")
    sys.exit(0)


def gen():
    """
    Generate a schema for a list of tables and print the link to the schema.
    """
    df = defog.Defog()  # load config from .defog/connection.json
    if len(sys.argv) < 3:
        print(
            "defog gen requires a list of tables to generate. Please enter the names of the tables whose schema you would like to generate, separated by a space:"
        )
        table_names = prompt().strip()
        table_name_list = re.split(r"\s+", table_names.strip())
    else:
        table_name_list = sys.argv[2:]

    if table_name_list == [""] or table_name_list == []:
        print("No tables were registered. Exiting.")
        sys.exit(0)
    print(
        "Do you want to automatically scan these tables to determine which column might be categorical? The distinct values in each column likely to be a categorical column will be sent to our server. (y/n)"
    )
    scan_option = prompt().strip()
    if scan_option.lower() == "y" or scan_option.lower() == "yes":
        scan = True
    else:
        scan = False

    filename = df.generate_db_schema(table_name_list, scan=scan)
    pwd = os.getcwd()
    print(
        "Your schema has been generated and is available at the following CSV file in this folder:\n"
    )
    print(f"\033[1m{pwd}/{filename}\033[0m\n")

    print("We are now uploading this auto-generated schema to Defog.")
    df.update_db_schema(filename)

    print(
        "If you modify the auto-generated schema, please run `defog update <csv_filename>` again to refresh the schema on Defog's servers."
    )


def update():
    """
    Update the schema in defog with a new schema using the url provided.
    """
    # check for 3rd arg (url), if not there, prompt user for url
    if len(sys.argv) < 3:
        print(
            "defog update requires a CSV that contains your Database metadata. Please enter the path to the CSV you would like to update:"
        )
        filename = prompt().strip()
    else:
        filename = sys.argv[2]
    # load config from .defog/connection.json
    df = defog.Defog()
    # upload schema to defog
    resp = df.update_db_schema(filename)
    if resp["status"] == "success":
        print("Your schema has been updated. You're ready to start querying!")
    else:
        print("There was an error updating your schema:")
        print(resp)
        print("Please try again, or contact us at founders@defog.ai")


def query():
    """
    Run a query and print the results alongside the generated SQL query.
    """
    df = defog.Defog()  # load config from .defog/connection.json
    if len(sys.argv) < 3:
        print("defog query requires a query. Please enter your query:")
        query = prompt().strip()
    else:
        query = sys.argv[2]

    user_question = ""
    sql_generated = ""
    while True:
        if query == "e":
            print("Exiting.")
            sys.exit(0)
        elif query == "":
            print("Your query cannot be empty.")
            query = prompt("Enter a query, or type 'e' to exit: ")
        user_question = query
        resp = df.run_query(query, retries=3)
        if not resp["ran_successfully"]:
            if "query_generated" in resp:
                print("Defog generated the following query to answer your question:\n")
                print(f"\033[1m{resp['query_generated']}\033[0m\n")

                print(
                    f"However, your query did not run successfully. The error message generated while running the query on your database was\n\n\033[1m{resp['error_message']}\033[0m\n."
                )

                print(
                    f"If you continue to get these errors, please consider updating the metadata in your schema by editing the google CSV generated and running `defog update <path/to/csv>`, or by updating your glossary.\n"
                )
            else:
                print(
                    f"Defog was unable to generate a query for your question. The error message generated while running the query on your database was\n\n\033[1m{resp.get('error_message')}\033[0m\n."
                )
        else:
            sql_generated = resp.get("query_generated")
            print("Defog generated the following query to answer your question:\n")
            print(f"\033[1m{resp['query_generated']}\033[0m\n")

            reason_for_query = resp.get("reason_for_query")
            if reason_for_query:
                reason_for_query = reason_for_query.replace(". ", "\n\n")

                print("This was its reasoning for generating this query:\n")
                print(f"\033[1m{reason_for_query}\033[0m\n")
            else:
                reason_for_query = ""

            print("Results:\n")
            # print results in tabular format using 'columns' and 'data' keys
            try:
                print_table(resp["columns"], resp["data"])
            except:
                print(resp)

            print()
            get_feedback(df.api_key, df.db_type, user_question, sql_generated)
        query = prompt("Please enter another query, or type 'e' to exit: ")


def deploy():
    """
    Deploy a cloud function that can be used to run queries.
    """
    # check args for gcp or aws
    if len(sys.argv) < 3:
        print("defog deploy requires a cloud provider. Please enter 'gcp' or 'aws':")
        cloud_provider = prompt().strip().lower()
    else:
        cloud_provider = sys.argv[2].lower()

    if len(sys.argv) >= 4:
        function_name = sys.argv[3]
    else:
        function_name = f"defog-{cloud_provider}"

    # load config from .defog/connection.json
    df = defog.Defog()

    if cloud_provider == "gcp":
        # base64 encode defog credentials for ease of passing around in cli
        creds64_str = df.to_base64_creds()
        source_path = os.path.join(defog.__path__[0], "gcp")
        cmd = [
            "gcloud",
            "functions",
            "deploy",
            function_name,
            "--runtime",
            "python310",
            "--region",
            "us-central1",
            "--source",
            source_path,
            "--entry-point",
            "defog_query_http",
            "--max-instances",
            "1",
            "--set-env-vars",
            f"DEFOG_CREDS_64={creds64_str}",
            "--trigger-http",
            "--gen2",
            "--allow-unauthenticated",
        ]
        try:
            cmd_str = " ".join(cmd)
            print(f"executing gcloud command:\n{cmd_str}")
            subprocess.check_call(cmd)
            print("gcloud command executed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error deploying Cloud Function:\n{e}")
    elif cloud_provider == "aws":
        # base64 encode defog credentials for ease of passing around in cli
        creds64_str = df.to_base64_creds()
        # get base config from defog package, add env vars
        base_config_path = os.path.join(defog.__path__[0], "aws", "base_config.json")
        with open(base_config_path, "r") as f:
            chalice_config = json.load(f)
        chalice_config["environment_variables"] = {"DEFOG_CREDS_64": creds64_str}
        chalice_config = parse_update(
            sys.argv[3:], ["app_name", "version"], chalice_config
        )
        aws_path = os.path.join(home_dir, ".defog", "aws")
        chalice_path = os.path.join(aws_path, ".chalice")
        if not os.path.exists(chalice_path):
            print(f"creating {chalice_path}")
            os.makedirs(chalice_path)
        chalice_config_path = os.path.join(chalice_path, "config.json")
        # save to .defog/aws/.chalice/config.json
        with open(chalice_config_path, "w") as f:
            json.dump(chalice_config, f)
        # copy over app.py and requirements.txt to .defog/aws
        app_path = os.path.join(defog.__path__[0], "aws", "app.py")
        req_path = os.path.join(defog.__path__[0], "aws", "requirements.txt")
        shutil.copy(app_path, aws_path)
        shutil.copy(req_path, aws_path)

        # deploy with chalice
        try:
            print("deploying with Chalice...")
            os.chdir(aws_path)
            subprocess.check_call(["chalice", "deploy"])
            os.chdir("../..")
            print("deployed aws lambda successfully with Chalice.")
            print(f"You can find the chalice deployment artifacts in {aws_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error deploying with Chalice:\n{e}")
    else:
        raise ValueError("Cloud provider must be 'gcp' or 'aws'.")


def quota():
    """
    Check your current usage and quota.
    """
    df = defog.Defog()
    resp = df.get_quota()
    if resp["ran_successfully"]:
        if resp["premium"]:
            print(f"You are currently on the premium plan with unrestricted usage.")
            print(f"Your current usage is {resp['queries_made']} queries.")
        else:
            print(
                f"You are currently on the free plan with {1000-resp['queries_made']} queries remaining for the month."
            )
            print(f"Your current usage is {resp['queries_made']} queries.")
    else:
        print(f"Failed to get quota")


# helper function to format different field types into strings
def to_str(field) -> str:
    if isinstance(field, str):
        return field
    elif isinstance(field, int):
        return str(field)
    elif isinstance(field, float):
        return str(field)
    elif isinstance(field, datetime.datetime):
        return field.strftime("%Y-%m-%d")
    elif isinstance(field, datetime.date):
        return field.strftime("%Y-%m-%d")
    elif isinstance(field, datetime.timedelta):
        return str(field)
    elif isinstance(field, datetime.time):
        return field.strftime("%H:%M:%S")
    elif isinstance(field, list):
        return str(field)
    elif isinstance(field, dict):
        return str(field)
    elif isinstance(field, bool):
        return str(field)
    elif isinstance(field, decimal.Decimal):
        return str(field)
    elif field is None:
        return "NULL"
    else:
        raise ValueError(f"Unknown type: {type(field)}")


# helper function to print results in tabular format
def print_table(columns, data):
    # Calculate the maximum width of each column, including headers
    data_header = data + [tuple(columns)]
    column_widths = [
        max(len(to_str(row[i])) for row in data_header) for i in range(len(columns))
    ]

    # Print the table headers
    for i, column in enumerate(columns):
        print(column.ljust(column_widths[i]), end=" | ")
    print()

    # Print the table divider
    for i, column_width in enumerate(column_widths):
        print("-" * column_width, end="-+-" if i < len(column_widths) - 1 else "-|\n")

    # Print the table data
    for row in data:
        for i, value in enumerate(row):
            print(to_str(value).ljust(column_widths[i]), end=" | ")
        print()


def serve_webserver():
    from defog.serve import app
    import uvicorn

    uvicorn.run(app, host="localhost", port=1235)


def serve_static():
    import http.server
    import socketserver
    import webbrowser

    port = 8002
    directory = os.path.join(defog.__path__[0], "static")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    webbrowser.open(f"http://localhost:{port}")
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving at port {port}")
        print(f"Static folder is {directory}")
        httpd.serve_forever()


def serve():
    """
    Serve a defog server locally.
    """
    print("Starting defog server...")
    print("Serving webserver...")
    webserver_process = subprocess.Popen(["defog", "serve-webserver"])
    time.sleep(2)

    print("Serving static files...")
    static_process = subprocess.Popen(["defog", "serve-static"])

    print("Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        static_process.terminate()
        webserver_process.terminate()
        sys.exit(0)


if __name__ == "__main__":
    main()
