import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestEmployeeEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.employeeService.save')
    def test_create_employee(self, mock_save):
        name = fake.name()
        position = fake.job()
        mock_employee = MagicMock()
        mock_employee.id = 1
        mock_employee.name = name
        mock_employee.position = position
        mock_save.return_value = mock_employee

        payload = {
                "name": name,
                "position": position
            }
        
        response = self.app.post('/employees/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_employee.id)

    @patch('services.employeeService.save')
    def test_missing_position_payload(self, mock_save):
        name = fake.name()
        mock_employee = MagicMock()
        mock_employee.id = 1
        mock_employee.name = name
        mock_save.return_value = mock_employee

        payload = {
            "name": name
        }

        response = self.app.post('/employees/', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn('position', response.json)

    @patch('services.employeeService.save')
    def test_extra_data_employee(self, mock_save):
        name = fake.name()
        position = fake.job()
        mock_employee = MagicMock()
        mock_employee.id = 1
        mock_employee.name = name
        mock_employee.position = position
        mock_save.return_value = mock_employee

        payload = {
                "name": name,
                "position": position
            }
        
        response = self.app.post('/employees/', json=payload)

        self.assertEqual(response.status_code, 400)