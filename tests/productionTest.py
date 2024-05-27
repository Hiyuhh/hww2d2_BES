import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestProductionEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.productionService.save')
    def test_create_production(self, mock_save):
        product_id = fake.random_digit_not_null()
        quantity_produced = fake.pyint()
        date_produced = fake.date_this_year()
        mock_production = MagicMock()
        mock_production.id = 1
        mock_production.product_id = product_id
        mock_production.quantity_produced = quantity_produced
        mock_production.date_produced = date_produced
        mock_save.return_value = mock_production

        payload = {
                "product_id": product_id,
                "quantity_produced": quantity_produced,
                "date_produced": date_produced
            }
        
        response = self.app.post('/productions/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_production.id)

    @patch('services.productionService.save')
    def test_missing_date_produced_payload(self, mock_save):
        product_id = fake.random_digit_not_null()
        quantity_produced = fake.pyint()
        mock_production = MagicMock()
        mock_production.id = 1
        mock_production.product_id = product_id
        mock_production.quantity_produced = quantity_produced
        mock_save.return_value = mock_production

        payload = {
                "product_id": product_id,
                "quantity_produced": quantity_produced,
            }

        response = self.app.post('/productions/', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn('date_produced', response.json)

    @patch('services.productionService.save')
    def test_extra_data_production(self, mock_save):
        product_id = fake.random_digit_not_null()
        quantity_produced = fake.pyint()
        date_produced = fake.date_this_year()
        mock_production = MagicMock()
        mock_production.id = 1
        mock_production.product_id = product_id
        mock_production.quantity_produced = quantity_produced
        mock_production.date_produced = date_produced
        mock_save.return_value = mock_production

        payload = {
                "product_id": product_id,
                "quantity_produced": quantity_produced,
                "date_produced": date_produced,
            }
        
        response = self.app.post('/productions/', json=payload)

        self.assertEqual(response.status_code, 400)