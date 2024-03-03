import requests
import json

class BrainbaseTypes:
    SHORT_TEXT = "ShortText"
    LONG_TEXT = "LongText"
    NUMBER = "Number"
    OPTION = "Option"

class Brainbase:
    def __init__(self, api_key, base_url='https://w4kgrml6rd.execute-api.us-east-1.amazonaws.com/default/brainbase-api'):
        self.api_key = api_key
        self.base_url = base_url

    def _post(self, data, file_path=None):
        json_data = json.dumps(data)

        files = {
            'file': (file_path.split("/")[-1], open(file_path, 'rb')) if file_path else None,
            'data': (None, json_data, 'application/json')
        }

        headers = {"x-api-key": self.api_key}
        response = requests.post(self.base_url, files=files, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.text}")

    def create_table(self, name, features):
        data = {
            'name': name,
            'features': features,
            'op': '/table/create'
        }
        response = self._post(data)
        return Table(self.api_key, response['data']['id'], self.base_url)

    def table(self, table_id):
        return Table(self.api_key, table_id, self.base_url)

class RowGroup:
    def __init__(self, api_key, table_id, row_ids=None, base_url='https://w4kgrml6rd.execute-api.us-east-1.amazonaws.com/default/brainbase-api'):
        self.api_key = api_key
        self.table_id = table_id
        self.row_ids = row_ids or []
        self.base_url = base_url
        self._brainbase = Brainbase(api_key, base_url)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return RowGroup(self.api_key, self.table_id, self.row_ids[key], self.base_url)
        elif isinstance(key, int):
            if key < 0:
                key += len(self.row_ids)
            if key < 0 or key >= len(self.row_ids):
                raise IndexError("Row index out of range")
            return Row(self.api_key, self.table_id, self.row_ids[key], None, self.base_url)
        else:
            raise TypeError("Row indices must be integers or slices, not {}".format(type(key).__name__))

    def __len__(self):
        return len(self.row_ids)

    def append(self, row):
        if isinstance(row, Row):
            self.row_ids.append(row.row_id)
        else:
            raise TypeError("Can only append Row objects to RowGroup")

    def extend(self, rows):
        if all(isinstance(row, Row) for row in rows):
            self.row_ids.extend(row.row_id for row in rows)
        else:
            raise TypeError("Can only extend RowGroup with Row objects")

# Modify the Table class to inherit from RowGroup
class Table(RowGroup):
    def __init__(self, api_key, table_id, base_url='https://w4kgrml6rd.execute-api.us-east-1.amazonaws.com/default/brainbase-api'):
        self.api_key = api_key
        self.table_id = table_id
        self.base_url = base_url
        self._brainbase = Brainbase(api_key, base_url)

    def _post(self, data, file_path=None):
        return self._brainbase._post(data, file_path)

    def insert(self, file_path):
        data = {
            'id': self.table_id,
            'op': '/table/insert',
        }
        response = self._post(data, file_path)
        print(response)
        return Row(self.api_key, self.table_id, response['data']['id'], None, self.base_url)

    def add_columns(self, columns):
        data = {
            'id': self.table_id,
            'columns': columns,
            'op': '/table/add-columns'
        }
        return self._post(data)

    def add_action(self, name, code):
        data = {
            'id': self.table_id,
            'op': '/action/create',
            'name': name,
            'code': code
        }
        return self._post(data)

    def add_trigger(self, name, trigger, code):
        data = {
            'id': self.table_id,
            'op': '/trigger/create',
            'name': name,
            'trigger': trigger,
            'code': code
        }
        return self._post(data)

    def row(self, id):
        return Row(api_key=self.api_key, table_id=self.table_id, row_id=id, base_url=self.base_url)

class Row:
    def __init__(self, api_key, table_id, row_id, data=None, base_url='https://w4kgrml6rd.execute-api.us-east-1.amazonaws.com/default/brainbase-api'):
        self.api_key = api_key
        self.table_id = table_id
        self.row_id = row_id
        self.data = data
        self.base_url = base_url
        self._brainbase = Brainbase(api_key, base_url)

    def _post(self, data):
        return self._brainbase._post(data)

    def read(self):
        data = {
            "op": "/table/read-from",
            "id": self.table_id,
            "row_id": self.row_id
        }
        return self._post(data)

    def populate(self, column_keys):
        data = {
            "op": "/row/populate",
            "id": self.table_id,
            "row_id": self.row_id,
            "column_keys": column_keys
        }
        return self._post(data)