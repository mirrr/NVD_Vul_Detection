import requests
import mysql.connector
from mysql.connector import Error
from datetime import *

____ = 0


# Part 1: Make DB containing vuls
# TODO: check MariaDB credentials for user and password


def createDBconnection():
    # returns "connection" if success or None if fail
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            # password=____,
            database="cve_data"
        )
        if connection.is_connected():
            print("Connected to MariaDB")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# fetchCVEdata() ok


def fetchCVEdata(start_date, end_date):
    try:
        # Fetch data from the NVD API from url, with date jan 2023-now
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        # end_date = datetime.now().isoformat() + "Z"
        params = {'pubStartDate': start_date, 'pubEndDate': end_date}
        response = requests.get(url, params=params)
        data = response.json().get('vulnerabilities', {})
        return end_date, data
    except Error as e:
        print(f"Error: {e}")
        return None, None


# TODO: RESTORE BUILD NUMBER COLUMN

def createOrUpdateTable(connection, data):
    # Build table using "data", with entries from "earliestTimestamp" onwards
    try:
        cursor = connection.cursor()

        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cve_data (
                cve_id VARCHAR(255),
                description TEXT,
                published_date VARCHAR(255),
                last_modified_date VARCHAR(255),
                base_score VARCHAR(255),
                evaluator_solution VARCHAR(255),
                windows_version VARCHAR(255),
                PRIMARY KEY (cve_id, windows_version)
            )
        ''')

        # Insert data into the table
        for d in data:
            item = d["cve"]
            cve_id = item["id"]
            description = item["descriptions"]
            published_date = item["published"]
            last_modified_date = item["lastModified"]

            # Extracting additional fields; None if key not found
            base_score = item["metrics"].get(
                'cvssMetricV31', [{}])[0].get('cvssData', {}).get('baseScore', None)
            evaluator_solution = item.get('evaluatorSolution', None)

            windows_versions = set()
            for node in item.get('configurations', {}).get('nodes', []):
                for cpe_match in node.get('cpeMatch', []):
                    cpe_uri = cpe_match.get('criteria', '')
                    if 'microsoft:windows' in cpe_uri:
                        # TODO: how to get window version number
                        windows_versions.add(____)

            """
            # extract build numbers from builds?
            builds = set()
            for node in item.get('configurations', {}).get('nodes', []):
                for cpe_match in node.get('cpeMatch', []):
                    cpe_uri = cpe_match.get('criteria', '')
                    if 'Microsoft:windows' in cpe_uri and 'build' in cpe_uri:
                        builds.add(cpe_match.get('version', ''))
            
            for build_number in builds:"""
            for windows_version in windows_versions:
                cursor.execute('''
                        INSERT INTO cve_data
                        (cve_id, description, base_score, evaluator_solution, windows_version)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        description=VALUES(description),
                        published_date=VALUES(published_date),
                        last_modified_date=VALUES(last_modified_date),
                        base_score=VALUES(base_score),
                        evaluator_solution=VALUES(evaluator_solution)
                    ''', (cve_id, description, published_date, last_modified_date, base_score, evaluator_solution, windows_version))
        connection.commit()
        print("Data inserted into MariaDB table")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()


def getCVEsByBuildNumber(connection, build_number):
    # returns "list_of_cves" if success or None if fail
    try:
        cursor = connection.cursor(dictionary=True)

        # Select relevant CVEs for the specified build number
        cursor.execute(
            '''SELECT cve_id, base_score, evaluator_solution FROM cve_data WHERE build_number = %s''', (build_number,))
        # a list of dictionaries containing cve_ids
        dictionary_of_cves = cursor.fetchall()

        # convert list of dictionaries into an array containing only cve_ids
        list_of_cves = [[i["cve_id"], i["base_score"],
                        i["evaluator_solution"]] for i in dictionary_of_cves]

        return list_of_cves
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()


def displayTable(connection):
    # returns "cve_data" if success or None if fail
    try:
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM cve_data''')
        # a list of dictionaries containing cve_ids
        cve_data = cursor.fetchall()
        return cve_data
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()


# Part 3: Update vul table


def resolveVul(connection, cveID, build_number):
    # receives a cveID and buildNumber to be resolved and removed from database
    '''
    VUL can be removed from list once resolved from all impacted devices of that build.
    Manually remove from list by removing via (cve_id, build_number) primary key pair
    '''
    # removing build number from build_numbers list
    try:
        cursor = connection.cursor()
        # for VUl in cve_data, if exists in (cveID, build_number) then remove
        cursor.execute('''
                    DELETE FROM cve_data WHERE cve_id = %s AND build_number = %s
                ''', (cveID, build_number))
        connection.commit()
        print("vul with (cve_id, build_number) pair (%s,%s) has been removed from MariaDB table",
              (cveID, build_number))
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
