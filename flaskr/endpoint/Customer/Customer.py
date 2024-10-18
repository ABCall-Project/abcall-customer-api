from flask_restful import Resource
from flask import jsonify, request
import logging
import requests
from ...application.customer_service import CustomerService
from ...infrastructure.databases.customer_postgresql_repository import CustomerPostgresqlRepository
from ...infrastructure.databases.plan_postgresql_repository import PlanPostgresqlRepository
from http import HTTPStatus
from ...utils import Logger

from config import Config

log = Logger()

class Customer(Resource):

    def __init__(self):
        config = Config()
        self.customer_repository = CustomerPostgresqlRepository(config.DATABASE_URI)
        self.plan_repository=PlanPostgresqlRepository(config.DATABASE_URI)
        self.service = CustomerService(self.customer_repository,self.plan_repository)


    def get(self, action=None):
        if action == 'getRateByCustomer':
            return self.get_rate_by_customer()
        elif action=='getCustomerList':
            return self.get_customer_list()
        elif action=='get_issue_fee_by_customer':
            return self.get_issue_fee_by_customer()
        
        else:
            return {"message": "Action not found"}, 404
        
    
    def get_rate_by_customer(self):

        try:
            customer_id = request.args.get('customer_id')
            log.info(f'Receive request to get rate plan by customer_id {customer_id}')
            rate = self.service.get_base_plan_suscription_rate(customer_id)

            
            return {
                'basic_monthly_rate': rate
            }, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get the data from {customer_id}: {ex}')
            return {'message': 'Something was wrong trying to get rate by customer data'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    
    def get_customer_list(self):
        try:

            log.info(f'Receive request to get customer list')

            
            customer_list = self.service.list_customers()
            list_c = [customer.to_dict() for customer in customer_list]
            
            return list_c, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get customer list: {ex}')
            return {'message': 'Something was wrong trying to get customer list'}, HTTPStatus.INTERNAL_SERVER_ERROR
        

    def get_issue_fee_by_customer(self):

        try:
            customer_id = request.args.get('customer_id')
            log.info(f'Receive request to get issue fee by customer_id {customer_id}')
            rate = self.service.get_base_plan_issue_fee(customer_id)

            
            return {
                'issue_fee': rate
            }, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get issue fee from {customer_id}: {ex}')
            return {'message': 'Something was wrong trying to get issue fee by customer data'}, HTTPStatus.INTERNAL_SERVER_ERROR
        