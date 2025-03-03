import copy

from demo_surveys import demo_data

class InMemoryDBAdapter:
    def __init__(self, session):
        self.session = session
        self.current_id = len(demo_data["surveys"]) + 1

    def get_table(self, table_name):
        if table_name not in self.session:
            self.session[table_name] = []
        return self.session[table_name]

    def get_objects_from_storage(self, table_name):
        table = self.get_table(table_name)
        return table

    def find_by_id(self, objects, obj_id):
        for obj in objects:
            if obj.get("id") == str(obj_id):
                return obj
        return None

    def add_survey(self, name):
        table = self.get_table("surveys")
        new_name = name or f"{demo_data['default_name']} {self.current_id}"
        new_obj = {
            "id": str(self.current_id),
            "name": new_name,
            "json": "{}"
        }
        self.current_id += 1
        table.append(new_obj)
        return new_obj

    def post_results(self, post_id, json_data):
        table = self.get_table("results")
        results = self.find_by_id(table, post_id)
        if not results:
            results = {
                "id": post_id,
                "data": []
            }
            table.append(results)
        results["data"].append(json_data)
        return {}

    def get_results(self, post_id):
        table = self.get_table("results")
        results = self.find_by_id(table, post_id)
        return results if results else None

    def delete_survey(self, survey_id):
        table = self.get_table("surveys")
        survey = self.find_by_id(table, survey_id)
        if survey:
            table.remove(survey)
        return survey if survey else None

    def store_survey(self, survey_id, name, json_data=None):
        table = self.get_table("surveys")
        survey = self.find_by_id(table, survey_id)
        if survey:
            survey["json"] = json_data
        else:
            survey = {
                "id": survey_id,
                "name": name or str(survey_id),
                "json": json_data
            }
            table.append(survey)
        return survey

    def change_name(self, survey_id, name=None):
        table = self.get_table("surveys")
        survey = self.find_by_id(table, survey_id)
        if survey:
            survey["name"] = name
        return survey

    def get_surveys(self):
        objects = self.get_objects_from_storage("surveys")
        if not objects:
            surveys_table = self.get_table("surveys")
            results_table = self.get_table("results")
            
            for survey in demo_data["surveys"]:
                copied_survey = copy.deepcopy(survey)
                surveys_table.append(copied_survey)
            
            for result in demo_data["results"]:
                copied_result = copy.deepcopy(result)
                results_table.append(copied_result)
            
            return self.get_objects_from_storage("surveys")
        return objects
        

    def get_survey(self, survey_id):
        return self.find_by_id(self.get_surveys(), survey_id)
