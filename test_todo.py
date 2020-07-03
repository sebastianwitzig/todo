import os, random, requests, sys, unittest
from datetime import date
from typing import Dict, Optional

from faker import Faker

from app.todo_app.enumerations import Status

faker = Faker()

print('Attention: All todos of the test user will be deleted!')
access_token = os.environ.get('TODO_ACCESS_TOKEN') \
    or input('Please type in your access token to test:')

class TestToDoAPI(unittest.TestCase):

    ENDPOINT = 'http://localhost:8000/todos/'

    def setUp(self):
        self.headers = {'Authorization': f'Token {access_token}'}
        self._create_dummy_data()

        # clean up test users todos
        response = requests.get(self.ENDPOINT, headers=self.headers)

        # delete todos
        for todo in response.json():
            response = requests.delete(
                self.ENDPOINT + f'{todo["id"]}/',
                headers=self.headers,
            )

    def _create_dummy_data(self):
        """Creates a list of dicts with dummy TODO data in self.todos."""
        self.todos = []
        for _ in range(10):
            todo = {
                'title': faker.sentence(),
                'description': '',
                'state': 0,
                'due_date': None,
            }

            self.todos.append(todo)
        self._manipulate_dummy_data()

    def _manipulate_dummy_data(self):
        """Manipulates randomly self.todos entries with dummy TODO data."""
        for todo in self.todos:
            todo['title'] = random.choice(
                (todo['title'], faker.sentence())
            )
            todo['description'] = random.choice(
                (todo['title'], faker.paragraph())
            )
            todo['state'] = random.choice(
                (todo['state'], *Status.get_values())
            )
            todo['due_date'] = random.choice(
                (todo['due_date'], faker.date())
            )

    def test_todo(self):
        # create todos
        for todo in self.todos:
            response = requests.post(self.ENDPOINT, todo, headers=self.headers)
            self.assertEqual(response.status_code, 201)
            created_todo = response.json()
            todo['id'] = created_todo['id']
            self.assertEqual(created_todo, todo)

        # list todos
        response = requests.get(self.ENDPOINT, headers=self.headers)
        self.assertCountEqual(self.todos, response.json())

        # update todos
        self._manipulate_dummy_data()
        for todo in self.todos:
            response = requests.patch(
                f'{self.ENDPOINT}{todo["id"]}/',
                todo,
                headers=self.headers,
            )
            self.assertEqual(response.status_code, 200)
            updated_todo = response.json()
            self.assertEqual(updated_todo, todo)

        # check update
        response = requests.get(self.ENDPOINT, headers=self.headers)
        self.assertCountEqual(self.todos, response.json())

        # delete todos
        for todo in self.todos:
            response = requests.delete(
                self.ENDPOINT + f'{todo["id"]}/',
                headers=self.headers,
            )

        # check deletion
        response = requests.get(self.ENDPOINT, headers=self.headers)
        self.assertEqual(len(response.json()), 0)

    def test_filters(self):
        test_cases = [
            {
                'field': 'title',
                'search_field': 'title',
                'value': 'Wash car',
                'search': 'car',
                'other_values': ['Clean House', 'Go shopping'],
                'output_asc': ['Clean House', 'Go shopping', 'Wash car'],
            },
            {
                'field': 'description',
                'search_field': 'description',
                'value': 'Wash the car',
                'search': 'wash',
                'other_values': ['Clean all rooms', 'Buy food'],
                'output_asc': ['Buy food', 'Clean all rooms', 'Wash the car'],
            },
            {
                'field': 'due_date',
                'search_field': 'due_date',
                'value': date(2017, 2, 13),
                'search': date(2017, 2, 13).isoformat(),
                'other_values': [
                    date(2017, 2, 14).isoformat(),
                    date(2017, 2, 15).isoformat(),
                ],
                'output_asc': [
                    date(2017, 2, 13).isoformat(),
                    date(2017, 2, 14).isoformat(),
                    date(2017, 2, 15).isoformat(),
                ],
            },
            {
                'field': 'state',
                'search_field': 'state',
                'value': int(Status.TODO),
                'search': int(Status.TODO),
                'other_values': [
                    int(Status.DONE),
                    int(Status.IN_PROGRESS),
                ],
                'output_asc': [
                    int(Status.TODO),
                    int(Status.IN_PROGRESS),
                    int(Status.DONE),
                ],
            },
        ]
        for test_case in test_cases:
            self._test_filter(test_case)

    def _test_filter(self, case: Dict):
        """Tests filters according to given case.

        Args:
            case:  test case with structure:
                   {
                       'field': 'title',
                       'value': 'Carwash',
                       'search': 'car',
                       'other_values': ['Clean House', 'Go shopping'],
                   }
        """

        # create Todos
        todo = self.todos[0]
        todo[case['field']] = case['value']
        response = requests.post(self.ENDPOINT, todo, headers=self.headers)
        todo_id = response.json()['id']

        for index, value in enumerate(case['other_values']):
            todo = self.todos[index + 1]
            todo[case['field']] = value
            response = requests.post(self.ENDPOINT, todo, headers=self.headers)

        # test filter
        response = requests.get(
            f'{self.ENDPOINT}?{case["search_field"]}={case["search"]}',
            headers=self.headers,
        )
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(todo_id, response.json()[0]['id'])

        # test ordering
        response = requests.get(
            f'{self.ENDPOINT}?ordering={case["field"]}',
            headers=self.headers,
        )
        self.assertEqual(len(response.json()), 3)
        for value, expected in zip(response.json(), case['output_asc']):
            self.assertEqual(value[case['field']], expected)

        # clean up
        response = requests.get(self.ENDPOINT, headers=self.headers)

        # delete todos
        for todo in response.json():
            response = requests.delete(
                self.ENDPOINT + f'{todo["id"]}/',
                headers=self.headers,
            )
