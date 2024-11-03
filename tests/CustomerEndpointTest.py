import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, request
from flask_restful import Api
from http import HTTPStatus
from flaskr.endpoint.Customer import Customer


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Customer, '/customer/<string:action>')
        self.client = self.app.test_client()

    @patch('flaskr.application.customer_service.CustomerService.get_base_plan_suscription_rate')
    def test_get_rate_by_customer_success(self, mock_get_rate):
        mock_get_rate.return_value = 99.99
        response = self.client.get('/customer/getRateByCustomer?customer_id=1234')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {'basic_monthly_rate': 99.99})
        mock_get_rate.assert_called_once_with('1234')

    @patch('flaskr.application.customer_service.CustomerService.list_customers')
    def test_get_customer_list_success(self, mock_list_customers):
        mock_list_customers.return_value = [
            MagicMock(to_dict=lambda: {'id': '1', 'name': 'Customer1'}),
            MagicMock(to_dict=lambda: {'id': '2', 'name': 'Customer2'})
        ]
        response = self.client.get('/customer/getCustomerList')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, [
            {'id': '1', 'name': 'Customer1'},
            {'id': '2', 'name': 'Customer2'}
        ])
        mock_list_customers.assert_called_once()

    @patch('flaskr.application.customer_service.CustomerService.get_base_plan_issue_fee')
    def test_get_issue_fee_by_customer_success(self, mock_get_issue_fee):
        mock_get_issue_fee.return_value = 50.0
        response = self.client.get('/customer/get_issue_fee_by_customer?customer_id=1234')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {'issue_fee': 50.0})
        mock_get_issue_fee.assert_called_once_with('1234')

    @patch('flaskr.application.customer_service.CustomerService.get_channel_by_plan')
    def test_get_channel_by_plan_success(self, mock_get_channel_by_plan):
        mock_get_channel_by_plan.return_value = [
            MagicMock(to_dict=lambda: {'id': '1', 'name': 'Channel1'}),
            MagicMock(to_dict=lambda: {'id': '2', 'name': 'Channel2'})
        ]
        response = self.client.get('/customer/getChannelByPlan?plan_id=5678')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, [
            {'id': '1', 'name': 'Channel1'},
            {'id': '2', 'name': 'Channel2'}
        ])
        mock_get_channel_by_plan.assert_called_once_with('5678')

    @patch('flaskr.application.customer_service.CustomerService.get_customer_by_id')
    def test_get_customer_by_id_success(self, mock_get_customer_by_id):
        mock_get_customer_by_id.return_value = MagicMock(to_dict=lambda: {'id': '1', 'name': 'Customer1'})
        response = self.client.get('/customer/getCustomerById?customer_id=1234')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {'id': '1', 'name': 'Customer1'})
        mock_get_customer_by_id.assert_called_once_with('1234')

    @patch('flaskr.application.customer_service.CustomerService.get_plan_by_id')
    def test_get_plan_by_id_success(self, mock_get_plan_by_id):
        mock_get_plan_by_id.return_value = MagicMock(to_dict=lambda: {'id': '1', 'name': 'Plan1'})
        response = self.client.get('/customer/getPlanById?plan_id=5678')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {'id': '1', 'name': 'Plan1'})
        mock_get_plan_by_id.assert_called_once_with('5678')

    def test_action_not_found(self):
        response = self.client.get('/customer/invalidAction')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Action not found"})

