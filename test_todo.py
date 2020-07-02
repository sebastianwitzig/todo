import os, random, requests, sys, unittest
from typing import Dict, Optional

from faker import Faker

from app.todo_app.enumerations import Status

faker = Faker()


class TestToDoAPI(unittest.TestCase):

    ENDPOINT = 'http://localhost:8000/todos/'

    def setUp(self):
        access_token = os.environ.get('TODO_ACCESS_TOKEN') \
            or input('Please type in your access token to test:')
        self.headers = {'Authorization': f'Token {access_token}'}
        self._create_dummy_data()

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
