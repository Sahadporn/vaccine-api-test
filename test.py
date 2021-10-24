import unittest
import requests

domain = "https://wcg-apis.herokuapp.com"
URL = domain + "/report_taken"


class reportTest(unittest.TestCase):
    """
    Unittest for ReportTaken api from World Class Government.
    """

    def create_payload(
        self, vaccine_name, citizen_id="1139465027391", option="walk-in"
    ):
        """
        Create payload to send to ReportTaken api.

        Args:
            vaccine_name (str): name of the vaccine which is going to be taken
            citizen_id (str): ID of each citizen. Defaults to "1139465027391".
            option (str): method to get vaccinated, can be walk-in or reserve. Defaults to "walk-in".

        Returns:
            json: json data for ReportTaken api
        """
        return {
            "citizen_id": citizen_id,
            "vaccine_name": vaccine_name,
            "option": option,
        }

    def get_feedback(self, response):
        """
        Get feedback from json response

        Args:
            response(Response): response from post request

        Returns:
            Response: string feedback from request
        """
        return response.json()["feedback"]

    def setUp(self):
        self.payload = {
            "citizen_id": "1139465027391",
            "name": "Anne",
            "surname": "Pytho",
            "birth_date": "6 Jan 1998",
            "occupation": "office worker",
            "address": "928 Sherman St.",
        }
        requests.post(domain + "/registration", data=self.payload)

    def test_report_sent(self):
        """
        Test report successfully sent for walk-in.
        """
        response = requests.post(URL, data=self.create_payload("Astra"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_feedback(response), "report success!")

    def test_not_enough_key(self):
        """
        Test missing query parameter.
        """
        response = requests.post(URL, data={"citizen_id": "1139465027391", "option": "walk-in"})
        self.assertEqual(response.status_code, 400)
    

    def test_invalid_vaccine_name(self):
        """
        Test invalid vaccine name input.
        """
        response = requests.post(URL, data=self.create_payload("Astro"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_feedback(response), "report failed: invalid vaccine name"
        )

    def test_unregistered_id(self):
        """
        Test report send from unregistered citizen ID.
        """
        response = requests.post(
            URL,
            data=self.create_payload(vaccine_name="Astra", citizen_id="1139465027322"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_feedback(response), "report failed: citizen ID is not registered"
        )

    def test_invalid_id(self):
        """
        Test invalid citizen ID.
        """
        response = requests.post(URL, data=self.create_payload(vaccine_name="Astra", citizen_id="113946502739"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_feedback(response), "report failed: invalid citizen ID"
        )

    def test_report_available_vaccine(self):
        """
        Test report for second dose vaccine.
        """
        requests.post(URL, data=self.create_payload(vaccine_name="Astra"))
        response = requests.post(URL, data=self.create_payload(vaccine_name="Astra"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_feedback(response), "report success!")

    def test_report_unavailable_vaccine(self):
        """
        Test report for second dose vaccine with invalid vaccination orders.
        """
        requests.post(URL, data=self.create_payload(vaccine_name="Astra"))
        response = requests.post(URL, data=self.create_payload(vaccine_name="Sinovac"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_feedback(response),
            "reservation failed: your available vaccines are only ['Astra', 'Pfizer']",
        )

    def test_empty_second_dose(self):
        """
        Test sending invalid second dose.
        """
        requests.post(URL, data=self.create_payload(vaccine_name="Astra"))
        response = requests.post(URL, data=self.create_payload(vaccine_name=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_feedback(response),
            "report failed: missing some attribute",
        )

    def test_is_reserved(self):
        """
        Test when already registered citizen request as a walk-in.
        """
        self.reserve = {
            "citizen_id": "1139465027391",
            "site_name": "Waterfall",
            "vaccine_name": "Astra",
        }
        requests.post(domain + "/reservation", data=self.reserve)
        response = requests.post(URL, data=self.create_payload(vaccine_name="Sinovac"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_feedback(response),
            "report failed: before walk-in, citizen need to cancel other reservation",
        )

    def test_reserve_option(self):
        """
        Test report taken from reserved citizen successfully.
        """
        self.reserve = {
            "citizen_id": "1139465027391",
            "site_name": "Waterfall",
            "vaccine_name": "Astra",
        }
        requests.post(domain + "/reservation", data=self.reserve)
        response = requests.post(
            URL, data=self.create_payload(vaccine_name="Astra", option="reserve")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_feedback(response), "report success!")

    def tearDown(self):
        requests.delete(domain + "/citizen", data=self.payload)


if __name__ == "__main__":
    unittest.main()
