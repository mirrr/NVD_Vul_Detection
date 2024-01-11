from HostServer import *
import unittest

____ = 0


class TestHostServer(unittest.TestCase):
    # No ip address provided
    def test_missing_remote_ip(self):
        remote_ip = None
        assert connectToRemoteServer(remote_ip) == False
        build_number = getBuildNumber(remote_ip)
        assert build_number.__contains__("Error")

    # TODO: replace ____ with invalid ip address
    def test_unsuccessful_connection(self):
        remote_ip = '____'
        assert connectToRemoteServer(remote_ip) == False

    # Improperly formated ip address provided
    def test_invalid_remote_ip_format(self):
        # Invalid bc string
        remote_ip = 'invalid_ip'
        assert connectToRemoteServer(remote_ip) == False
        build_number = getBuildNumber(remote_ip)
        assert build_number.__contains__("Error")
        # Invalid bc contains number above 255 in it is invalid
        remote_ip = '127.0.256.0'
        assert connectToRemoteServer(remote_ip) == False
        build_number = getBuildNumber(remote_ip)
        assert build_number.__contains__("Error")
        # Invalid bc contains more than 3 dots is invalid
        remote_ip = '127.0.0.0.'
        assert connectToRemoteServer(remote_ip) == False
        build_number = getBuildNumber(remote_ip)
        assert build_number.__contains__("Error")

    """ #TODO: replace ____ with valid ip address
    def test_successful_connection_and_build_number(self):
        remote_ip = '____'
        assert connectToRemoteServer(remote_ip) == True
        build_number = getBuildNumber(remote_ip)
        assert not build_number.__contains__("Error")


    # TODO: replace ____ with valid ip address, but build number retrieval errors
    def test_error_in_build_number_retrieval(self):
        remote_ip = '____'
        assert connectToRemoteServer(remote_ip) == True
        build_number = getBuildNumber(remote_ip)
        assert build_number.__contains__("Error")

    """
