import unittest
from inmemorydbadapter import InMemoryDBAdapter
from demo_surveys import demo_data

class TestInMemoryDBAdapter(unittest.TestCase):
    def setUp(self):
        self.session = {}
        self.adapter = InMemoryDBAdapter(self.session)
    
    def test_initialization(self):
        self.assertEqual(self.adapter.current_id, len(demo_data["surveys"]) + 1)
    
    def test_get_table_existing(self):
        self.session["surveys"] = [{"test": "data"}]
        table = self.adapter.get_table("surveys")
        self.assertEqual(table, [{"test": "data"}])
    
    def test_get_table_new(self):
        table = self.adapter.get_table("new_table")
        self.assertEqual(table, [])
        self.assertIn("new_table", self.session)
    
    def test_find_by_id_found(self):
        objects = [{"id": "1"}, {"id": "2"}]
        result = self.adapter.find_by_id(objects, "1")
        self.assertEqual(result, {"id": "1"})
    
    def test_find_by_id_not_found(self):
        objects = [{"id": "1"}]
        result = self.adapter.find_by_id(objects, "2")
        self.assertIsNone(result)
    
    def test_add_survey_with_name(self):
        new_survey = self.adapter.add_survey("Test Survey")
        self.assertEqual(new_survey["name"], "Test Survey")
        self.assertEqual(new_survey["id"], str(len(demo_data["surveys"]) + 1))
        self.assertEqual(len(self.adapter.get_table("surveys")), 1)
    
    def test_add_survey_without_name(self):
        new_survey = self.adapter.add_survey(None)
        expected_name = f"{demo_data['default_name']} {self.adapter.current_id - 1}"
        self.assertEqual(new_survey["name"], expected_name)
    
    def test_post_results_new_post(self):
        post_id = "123"
        test_data = {"answer": 42}
        self.adapter.post_results(post_id, test_data)
        results = self.adapter.get_results(post_id)
        self.assertEqual(len(results["data"]), 1)
        self.assertEqual(results["data"][0], test_data)
    
    def test_post_results_existing_post(self):
        post_id = "123"
        self.adapter.post_results(post_id, {"data": 1})
        self.adapter.post_results(post_id, {"data": 2})
        results = self.adapter.get_results(post_id)
        self.assertEqual(len(results["data"]), 2)
    
    def test_get_results_not_exists(self):
        results = self.adapter.get_results("non_existent")
        self.assertIsNone(results)
    
    def test_delete_survey_exists(self):
        survey = {"id": "1", "name": "Test"}
        self.adapter.get_table("surveys").append(survey)
        result = self.adapter.delete_survey("1")
        self.assertEqual(result, survey)
        self.assertEqual(len(self.adapter.get_table("surveys")), 0)
    
    def test_delete_survey_not_exists(self):
        result = self.adapter.delete_survey("999")
        self.assertIsNone(result)
    
    def test_store_survey_update(self):
        survey = {"id": "1", "name": "Old", "json": "{}"}
        self.adapter.get_table("surveys").append(survey)
        updated = self.adapter.store_survey("1", "New", '{"new": "data"}')
        self.assertEqual(updated["json"], '{"new": "data"}')
    
    def test_store_survey_create(self):
        survey = self.adapter.store_survey("100", "New Survey", "{}")
        self.assertEqual(survey["name"], "New Survey")
        self.assertIn(survey, self.adapter.get_table("surveys"))
    
    def test_change_name_exists(self):
        survey = {"id": "1", "name": "Old"}
        self.adapter.get_table("surveys").append(survey)
        self.adapter.change_name("1", "New")
        self.assertEqual(survey["name"], "New")
    
    def test_change_name_not_exists(self):
        result = self.adapter.change_name("999", "New")
        self.assertIsNone(result)
    
    def test_get_surveys_initial_load(self):
        surveys = self.adapter.get_surveys()
        self.assertEqual(len(surveys), len(demo_data["surveys"]))
        self.assertEqual(len(self.session["results"]), len(demo_data["results"]))
    
    def test_get_surveys_subsequent_calls(self):
        self.adapter.get_surveys()
        new_survey = self.adapter.add_survey("Test")
        surveys = self.adapter.get_surveys()
        self.assertIn(new_survey, surveys)
    
    def test_get_survey_exists(self):
        self.adapter.get_surveys()
        survey = self.adapter.get_survey("1")
        self.assertEqual(survey["id"], "1")
    
    def test_get_survey_not_exists(self):
        survey = self.adapter.get_survey("999")
        self.assertIsNone(survey)

if __name__ == '__main__':
    unittest.main()