from CVEdata import *
import unittest


class TestCVEdata(unittest.TestCase):

    def test(self):
        # TODO: what is <Response [200]> VS <Response [404]>
        # span of 4 months is ok
        start_date = datetime(2023, 1, 1).isoformat() + "Z"
        end_date = datetime(2023, 5, 1).isoformat() + "Z"
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        #end_date = datetime.now().isoformat() + "Z"
        params = {'pubStartDate': start_date, 'pubEndDate': end_date}
        response = requests.get(url, params=params)
        print(response.status_code)

    def testDBconnection(self):
        print(createDBconnection())


"""
    def testfetchCVEdataFail(self):
        bad_start_date = datetime(2025, 1, 1).isoformat() + "Z"
        print(bad_start_date)
        print(fetchCVEdata(bad_start_date))
        #assert fetchCVEdata(bad_start_date) == None, None

    def testfetchCVEdataSuccess(self):
        start_date = datetime(2024, 1, 1).isoformat() + "Z"
        data_from_2024_onwards = fetchCVEdata(start_date)
        print(data_from_2024_onwards)"""
