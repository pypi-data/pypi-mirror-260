from databricks import sql
import pandas as pd
import json
import re
import time
import requests


def query_databricks_tables(query, cluster_type, endpoint, token, cluster_id):
    # STRING TYPE INPUT
    if not isinstance(query, str):
        raise Exception("Query needs to be a String Type!")

    ## GET COLUMNS NAMES FROM QUERY ##
    pattern = re.compile(r'\bSELECT\b(.*?)\bFROM\b', re.DOTALL | re.IGNORECASE)
    splitted_string = [n.strip() for n in re.search(pattern, query).group(1).strip().split(",")]
    columns = []
    new_pattern = re.compile(r'\bAS\s+(.*?)$', re.IGNORECASE)
    for n in splitted_string:
        columns.append(re.search(new_pattern, n).group(1).strip()) if re.search(new_pattern, n) else columns.append(n)
    #print(columns)

    select_star = False
    # IF THE QUERY IS SELECT *, NEED TO GET METADATA FROM TABLE
    if len(columns) == 1 and columns[0] == '*':
        select_star = True
        match = re.search(r'FROM (\S+)', query, re.IGNORECASE)
        if match:
            full_table_name = match.group(1)
            parts = full_table_name.split('.')
            if len(parts) == 2:
                schema, table = parts
            elif len(parts) == 3:
                _, schema, table = parts

    ## REST API CONFIG ##
    endpoint_id = endpoint.split("-")[1].split(".")[0]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    ## CHECK CLUSTERS TO START IF NEEDED ##
    if cluster_type.upper() == "ALL-PURPOSE":
        # ALL-PURPOSE CLUSTER INFOS #
        cluster_state_api = f"https://{endpoint}/api/2.0/clusters/get"
        cluster_start_api = f"https://{endpoint}/api/2.0/clusters/start"
        params = {
            "cluster_id": cluster_id
        }

        # All-Purpose Cluster
        http_path = f"sql/protocolv1/o/{endpoint_id}/{cluster_id}"

        # START ALL-PURPOSE CLUSTER ##
        response = requests.get(cluster_state_api, headers=headers, params=params)
        if response.json()["state"] != 'RUNNING':
            response = requests.post(cluster_start_api, headers=headers, json=params)
            if response.status_code == 200:
                print(f'Waiting cluster to start!')
                cluster_starting = True
                while cluster_starting:
                    time.sleep(120)
                    response = requests.get(cluster_state_api, headers=headers, params=params)
                    cluster_starting = response.json()["state"] != 'RUNNING'
                    print('Waiting, cluster is starting!')
                time.sleep(60)
                print('Waiting, cluster is installing libraries!')
            else:
                print("All-purpose cluster did not start, trying again!")
                query_databricks_tables(query, cluster_type, endpoint, token, cluster_id)
        else:
            print("All-purpose cluster is running!")

    elif cluster_type.upper() == "SQL":
        # SQL CLUSTER INFOS #
        warehouse_state_api = f"https://{endpoint}/api/2.0/sql/warehouses/{cluster_id}"
        warehouse_start_api = f"{warehouse_state_api}/start"

        # SQL Warehouse Cluster
        http_path = f"/sql/1.0/warehouses/{cluster_id}"

        # START SQL CLUSTER ##
        response = requests.get(warehouse_state_api, headers=headers)
        if response.json()["state"] != 'RUNNING':
            response = requests.post(warehouse_start_api, headers=headers, json={})
            if response.status_code == 200:
                print('Waiting cluster to start!')
                warehouse_starting = True
                while warehouse_starting:
                    time.sleep(120)
                    response = requests.get(warehouse_state_api, headers=headers)
                    warehouse_starting = response.json()["state"] != 'RUNNING'
                    print('Waiting, cluster is starting!')
            else:
                print("Warehouse cluster did not start, trying again!")
                query_databricks_tables(query, cluster_type, endpoint, token, cluster_id)
        else:
            print("Warehouse cluster is running!")

    else:
        raise Exception("Cluster type needs to be 'ALL-PURPOSE' or 'SQL'!")

    ## RUN QUERY AND BUILD PANDAS DATA FRAME TO RETURN ##
    try:
        with sql.connect(
                # DATABRICKS CONNECTION DETAILS
                server_hostname=endpoint,
                http_path=http_path,
                access_token=token
        ) as conn:

            with conn.cursor() as cursor:
                # GET COLUMN NAMES FROM TABLE METADATA IF THE QUERY IS SELECT *
                if select_star:
                    columns = [row["COLUMN_NAME"] for row in
                               cursor.columns(schema_name=schema, table_name=table).fetchall()]

                # BUILD PANDAS DATAFRAME AND RETURN
                print("Running query, waiting return!")
                return pd.DataFrame(
                    data=cursor.execute(query).fetchall(),
                    columns=columns
                )

    ## HANDLE EXCEPTIONS ##
    except Exception as e:
        raise Exception(e)
