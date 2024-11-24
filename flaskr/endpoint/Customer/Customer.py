import uuid
from flask_restful import Resource
from flask import request
from ...application.customer_service import CustomerService
from ...infrastructure.databases.customer_postgresql_repository import CustomerPostgresqlRepository
from ...infrastructure.databases.plan_postgresql_repository import PlanPostgresqlRepository
from ...infrastructure.databases.channel_postgresql_repository import ChannelPostgresqlRepository
from ...infrastructure.databases.customer_database_postgresql_repository import CustomerDatabasePostgresqlRepository
from http import HTTPStatus
from ...utils import Logger
from .validation_customer import validate_customer
from ...domain.models import PlanEnum

log = Logger()

class Customer(Resource):

    def __init__(self):
        self.customer_repository = CustomerPostgresqlRepository()
        self.plan_repository=PlanPostgresqlRepository()
        self.channel_repository=ChannelPostgresqlRepository()
        self.customer_database_repository = CustomerDatabasePostgresqlRepository()
        self.service = CustomerService(self.customer_repository,self.plan_repository,self.channel_repository, self.customer_database_repository)        


    def get(self, action=None):
        if action == 'getRateByCustomer':
            return self.get_rate_by_customer()
        elif action=='getCustomerList':
            return self.get_customer_list()
        elif action=='get_issue_fee_by_customer':
            return self.get_issue_fee_by_customer()
        elif action=='getChannelByPlan':
            return self.get_channel_by_plan()
        elif action=='getCustomerById':
            return self.get_customer_by_id()
        elif action=='getPlanById':
            return self.get_plan_by_id()
        else:
            return {"message": "Action not found"}, 404
        
    def post(self, action=None):
        if action == 'loadCustomerDataBase':
            return self.load_customer_database_entries()
        if action == 'create':
            return self.create()
        if action == 'loadCustomers':
            return self.add_customers()
        else:
            return {"message": "Action not supported for POST method"}, 405
            
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

    def get_channel_by_plan(self):
        try:
            plan_id = request.args.get('plan_id')
            log.info(f'Receive request to get issue fee by plan_id {plan_id}')
            channels_list = self.service.get_channel_by_plan(plan_id)
            channel_c = [channel.to_dict() for channel in channels_list]

            
            return channel_c, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get issue fee from {plan_id}: {ex}')
            return {'message': 'Something was wrong trying to get issue fee by customer data'}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_customer_by_id(self):    
        try:
            customer_id = request.args.get('customer_id')
            log.info(f'Receive request customer by customer_id {customer_id}')
            customer = self.service.get_customer_by_id(customer_id)
            if customer:
                customer_s=customer.to_dict()
                return  customer_s, HTTPStatus.OK
            else:
                return None, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get customer by customer_id: {ex}')
            return {'message': 'Something was wrong trying to get customer by customer_id'}, HTTPStatus.INTERNAL_SERVER_ERROR
        

    def get_plan_by_id(self):
        try:
            plan_id = request.args.get('plan_id')
            log.info(f'Receive request plan by plan_id {plan_id}')
            plan = self.service.get_plan_by_id(plan_id)
            if plan:
                plan_s=plan.to_dict()
                return  plan_s, HTTPStatus.OK
            else:
                return None, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get plan by plan_id: {ex}')
            return {'message': 'Something was wrong trying to get plan by plan_id'}, HTTPStatus.INTERNAL_SERVER_ERROR
        

    def load_customer_database_entries(self):
        try:
            customer_id = request.json.get('customer_id')
            entries = request.json.get('entries', [])
            log.info(f'Receive request to load entries for customer_id {customer_id}')
            added_entries = self.service.load_customer_database_entries(customer_id, entries)
            return [entry.to_dict() for entry in added_entries], HTTPStatus.CREATED
        except Exception as ex:
            log.error(f'Some error occurred trying to load entries for customer_id {customer_id}: {ex}')
            return {'message': 'Something was wrong trying to load entries for customer data'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @validate_customer()
    def create(self):
        try:
            name = request.form.get('name')
            document = request.form.get('document')
            plan_id = request.form.get('plan_id')
            if (plan_id is None):
                plan_id = PlanEnum.ENTREPRENEUR.value
            
            log.info(f'Receive request to create customer with name {name} and plan_id {plan_id}')
            if document:
                customerFound = self.customer_repository.get_customer_by_document(document)

            if document == None or not customerFound:
                customer = self.service.create_customer(name, plan_id, document)
            else:
                return {'message': 'Customer already exists'}, HTTPStatus.CONFLICT
        
            return customer.to_dict(), HTTPStatus.CREATED

        except Exception as ex:
            log.error(f'Some error occurred trying to create customer: {ex}')
            return {'message': 'Something was wrong trying to create customer'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    def add_customers(self):
        try:
            customers = request.json.get('customers', [])
            plan_id = request.json.get('plan_id')

            if not plan_id or not customers:
                log.error('Plan ID or customers list missing in the request')
                return {'message': 'Plan ID and customers list are required'}, HTTPStatus.BAD_REQUEST

            log.info(f'Receive request to add {len(customers)} customers with plan_id {plan_id}')
            added_customers = self.service.add_customers(customers, uuid.UUID(plan_id))

            return [customer.to_dict() for customer in added_customers], HTTPStatus.CREATED
        except Exception as ex:
            log.error(f'Some error occurred trying to add customers: {ex}')
            return {'message': 'Something went wrong trying to add customers'}, HTTPStatus.INTERNAL_SERVER_ERROR
