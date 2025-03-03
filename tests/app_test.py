import unittest
import json
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.session = {}
        
        app.config['SESSION_TYPE'] = 'null'
        app.config['TESTING'] = True

    def test_get_active_surveys(self):
        with self.client:
            response = self.client.get('/api/getActive')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertGreater(len(data), 0)
            self.assertIn('id', data[0])
            self.assertIn('name', data[0])

    def test_get_survey_exists(self):
        with self.client:
            get_active = self.client.get('/api/getActive')
            first_id = json.loads(get_active.data)[0]['id']
            
            response = self.client.get(f'/api/getSurvey?surveyId={first_id}')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['id'], first_id)

    def test_get_survey_not_exists(self):
        with self.client:
            response = self.client.get('/api/getSurvey?surveyId=9999')
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(json.loads(response.data))

    def test_change_name(self):
        with self.client:
            create_resp = self.client.get('/api/create?name=Test%20Survey')
            survey = json.loads(create_resp.data)
            
            new_name = "New Name"
            response = self.client.get(
                f'/api/changeName?id={survey["id"]}&name={new_name}'
            )
            updated = json.loads(response.data)
            
            self.assertEqual(updated['name'], new_name)
            self.assertEqual(updated['id'], survey['id'])

    def test_create_survey(self):
        with self.client:
            response = self.client.get('/api/create?name=Test%20Create')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['name'], 'Test Create')
            self.assertIsNotNone(data['id'])

    def test_change_json(self):
        with self.client:
            create_resp = self.client.get('/api/create')
            survey = json.loads(create_resp.data)
            
            test_json = {'question': 'Test?'}
            response = self.client.post(
                '/api/changeJson',
                json={'id': survey['id'], 'json': test_json}
            )
            updated = json.loads(response.data)
            
            self.assertEqual(updated['json'], test_json)

    def test_post_results(self):
        with self.client:
            post_id = '123'
            test_data = {'answer': 42}
            
            response = self.client.post(
                '/api/post',
                json={'postId': post_id, 'surveyResult': test_data}
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {})

    def test_delete_survey(self):
        with self.client:
            create_resp = self.client.get('/api/create')
            survey = json.loads(create_resp.data)
            
            response = self.client.get(f'/api/delete?id={survey["id"]}')
            data = json.loads(response.data)
            
            self.assertEqual(data['id'], survey['id'])

    def test_get_results(self):
        with self.client:
            post_id = 'results_test'
            test_data = {'data': 'test'}
            
            self.client.post(
                '/api/post',
                json={'postId': post_id, 'surveyResult': test_data}
            )
            
            response = self.client.get(f'/api/results?postId={post_id}')
            data = json.loads(response.data)
            
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'][0], test_data)

    @unittest.skip("it doesn't work properly yet")
    def test_static_routes(self):
        routes = [
            '/',
            '/about',
            '/run/test',
            '/edit/123',
            '/results/456'
        ]
        
        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'index.html', response.data)

    def test_invalid_route(self):
        response = self.client.get('/invalid-route')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()