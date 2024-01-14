import psutil
import socket
import platform

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


def getWindowsVersion(ip_address):
    try:
        # Establish a connection to the remote server
        with socket.create_connection((remote_ip, 22), timeout=1) as sock:
            # Check if the remote system is running Windows
            if platform.system() == 'Windows':
                # Retrieve the Windows version using psutil
                windows_version = platform.win32_ver()[0]
                return windows_version
            else:
                return "Remote system is not running Windows"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    remote_ip = ____  # TODO: Replace with IP address of the remote server

    if connectToRemoteServer(remote_ip):
        windows_version = getWindowsVersion(remote_ip)
        # TODO: change – build numbers are not ints
        if not windows_version.__contains__("Error"):
            print(f"Windows Version for {remote_ip}: {windows_version}")
        else:
            print(windows_version)
    else:
        print(f"Error connecting to the remote server at {remote_ip}")
