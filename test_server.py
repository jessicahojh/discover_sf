from unittest import TestCase
from server import app


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):

        pass


    def test_home_page(self):
      """Some non-database test..."""

      result = self.client.get("/")
      self.assertEqual(result.status_code, 200)
      self.assertIn('<h1>San Francisco </h1>', result.data)



# class TestFlaskRoutes(unittest.TestCase):
#     """Test Flask routes."""

#     def test_home_page(self):
#         """Make sure home page returns correct HTML."""

#         # Create a test client
#         client = server.app.test_client()
#         server.app.config['TESTING'] = True #print all Flask errors to the console

#         # Use the test client to make requests
#         result = client.get('/')

#         # Compare result.data with assert method
#         self.assertIn(b'<h1>San Francisco </h1>', result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"user_id": 4, "password": "python"},
                                  follow_redirects=True)
        self.assertIn(b" ", result.data)


    def test_neighborhoods_page(self):

        pass


    def test_specific_neighborhood_page(self):

        pass


    def test_restaurants_page(self):

        pass


    def test_list_places_page(self):

        pass


    def test_specific_places_page(self):

        pass

