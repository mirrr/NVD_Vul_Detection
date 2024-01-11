from HostServer import *
from CVEdata import *
from dateutil.relativedelta import relativedelta

# date_since_last_update initialized as 1/1/2023
last_update = datetime(2023, 1, 1)


# Part 1: Make DB containing vuls

# TODO: breaks down fetchCVEdata() into chunks if date range too big
def buildDB():
    connection = createDBconnection()
    if not connection:
        print("Failed to connect to MariaDB.")
        return None, None

    # updates date_since_last_update
    end_date = datetime.now()

    while last_update < end_date:
        # increment last_update by 4 months
        start_add_4m = last_update + relativedelta(months=4)
        # gets data using smaller of start_add_4m VS end_date
        last_update, cve_data = fetchCVEdata(
            last_update, min(end_date, start_add_4m))
        # createOrUpdateTable()
        if cve_data:
            createOrUpdateTable(connection, cve_data)

    """ last_update, cve_data = fetchCVEdata(last_update, end_date)
    if not cve_data:
        print("No CVE data available.")
        return None, None"""

    createOrUpdateTable(connection, cve_data)

    return connection, cve_data


# Part 2: Access host inventory + Return # of impacted assets (laptops)
'''
1. Which parameter "p" to match host inventory to CVEs?
==> call CrowdStrike API to get parameter "p"
==> get all "p's" and return
          a) # of impacted assets
          b) # of impacted assets per CVE?
'''


# TODO: depends on being able to find CVEs based on build number
def getCVEsbyIPaddress(db_connection, ip_address):
    try:
        if connectToRemoteServer(ip_address):
            build_number = getBuildNumber(ip_address)
            list_of_cves = getCVEsByBuildNumber(db_connection, build_number)
            return list_of_cves
    except Error as e:
        print("unable to connect to remote server at %s", ip_address)
        print(f"Error: {e}")
        return None


# Part 3: Update vul table
# TODO: depends on being able to find CVEs based on build number

def main():
    # lowkey might not need cve_data ==> remove from returns in buildDB()?
    connection, cve_data = buildDB(last_update)

    # displayTable(cve_data)

    # Close the database connection
    if connection.is_connected():
        connection.close()
        print("Connection to MariaDB closed.")


if __name__ == "__main__":
    main()
