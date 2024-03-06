import unittest

from src.hook import CustomHook, Request

class TestCustomHook(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_before_request(self):
        hook = CustomHook()

        request = Request("GET", "https://api.example.com", {
            "Content-Type": "application/json",
        })

        hook.before_request(request)

        # Assert the header is set
        self.assertTrue(request.headers["Content-Type"] is not None)
        self.assertEqual(request.headers["Content-Type"], "application/json")


if __name__ == '__main__':
    unittest.main()
