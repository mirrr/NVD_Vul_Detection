import psutil
import socket

____ = 0


def connectToRemoteServer(ip_address):
    try:
        # Create a connection to the remote server
        connection = psutil._psplatform.socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip_address, 445))
        connection.close()
        # if connection is possible, then must be a valid, connectable remote server
        return True
    except Exception as e:
        return False


def getBuildNumber(ip_address):
    try:
        # Use psutil to get system information from the remote server
        system_info = psutil.win_service_get("OSPPSVC", ip_address=ip_address)
        build_number = system_info["version_info"]["build"]
        return build_number
    except Exception as e:
        return f"Error retrieving Windows build number: {str(e)}"


if __name__ == "__main__":
    remote_ip = ____  # TODO: Replace with IP address of the remote server

    if connectToRemoteServer(remote_ip):
        build_number = getBuildNumber(remote_ip)
        # TODO: change – build numbers are not ints
        if not build_number.__contains__("Error"):
            print(f"Windows Build Number for {remote_ip}: {build_number}")
        else:
            print(build_number)
    else:
        print(f"Error connecting to the remote server at {remote_ip}")
