import psycopg
from model.account import Account


class AccountDao:

    def get_customer_account(cls, customer_id, amountGreaterThan, amountLessThan):
        command = f"select * from accounts WHERE balance BETWEEN  {amountGreaterThan} AND {amountLessThan} and customer_id=(%s);"
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command, [customer_id], binary=True)
                    data = cur.fetchall()  # fetching all rows from customer's table
                    body = []
                    for account in data:
                        body.append(Account(*account))
                    
                    return body

        except Exception as e:
            print(e)
        return None

    def get_accounts(cls, amountGreaterThan, amountLessThan):
        command = f"select * from accounts WHERE balance BETWEEN  {amountGreaterThan} AND {amountLessThan};"
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command)
                    data = cur.fetchall()  # fetching all rows from customer's table
                    body = []
                    for account in data:
                        body.append(Account(*account))

                    return body

        except Exception as e:
            print(e)
        return None

    def get_account(cls, account_id):
        command = "select * from accounts where account_id = %s"
       
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command, [account_id], binary=True)
                    account = cur.fetchone()
                    account_obj = Account(*account)
                    return account_obj

        except Exception as e:
            print(e)
        return None

    def update_account(cls, account_id, data):
        command = ('''UPDATE accounts SET 
                        description=(%s), 
                        balance=(%s) where account_id=(%s) RETURNING *''')

        account_data = get_account(account_id)
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command, (
                        data.get("description") or account_data.get("body").get("description"),
                        data.get("balance") or account_data.get("body").get("balance"),
                        account_id))
                    conn.commit()
                    updated_data = cur.fetchone()
                    if updated_data is None:
                        body = None
                    else:
                        print("updated data")
                        body = Account(*updated_data)
                    return body

        except Exception as e:
            print(e)
           
        return None

    def delete_account(cls, account_id):
        command = ("DELETE FROM accounts WHERE account_id = %s")
        
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command, [account_id], binary=True)
                    # Check number of rows that were deleted
                    rows_deleted = cur.rowcount
                    
                    if rows_deleted != 1:
                        return False
                    else: 
                        conn.commit()
                        return True

        except Exception as e:
            print(e)
        return False

    def insert_accounts(cls, customer_id, account):
        command = (
            '''
            insert into accounts(date_opened, description, balance, account_type_code, customer_id) 
            VALUES (%s,%s,%s,%s,%s) RETURNING *;
            '''
        )
        message = {}
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command, (
                        date.today(),
                        account.get('description'),
                        account.get('balance'),
                        account.get('account_type_code'),
                        customer_id
                    ))
                    conn.commit()
                    inserted_row = cur.fetchone()
                    return Account(*inserted_row)
                    
        except Exception as e:
            print(e)
            
        return None
      
      
      #---------------------------------------------------------------------------------------
      
      
      import psycopg
from model.customer import Customer


class CustomerDao:

    def insert_customers(cls, customer):
        command = (
            '''
            insert into customers(last_name, first_name, middle_initial, street, city, state, zip, phone, email) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *;
            '''
        )
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command, (
                        customer.get('last_name'),
                        customer.get('first_name'),
                        customer.get('middle_initial'),
                        customer.get('street'),
                        customer.get('city'),
                        customer.get('state'),
                        customer.get('zip'),
                        customer.get('phone'),
                        customer.get('email')
                    ))
                conn.commit()
                inserted_row = cur.fetchone()
                return Customer(*inserted_row)

        except Exception as e:
            print(e)
        return None

    def get_customers():
        command = "select * from customers;"
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command)
                    customers = cur.fetchall()  # fetching all rows from customer's table
                    body = []
                    for data in customers:
                        body.append(Customer(*data))
                    return body

        except Exception as e:
            print(e)
        return None

    def get_customer(customer_id):
        command = "select * from customers where customer_id = %s"
        
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command, [customer_id], binary=True)
                    data = cur.fetchone()
                    body = Customer(*data)
                    return body

        except Exception as e:
            print(e)
        return None

    def update_customer(customer_id, data):
        command = ('''UPDATE customers SET 
                        last_name=(%s), 
                        first_name=(%s), 
                        middle_initial=(%s), 
                        street=(%s), 
                        city=(%s),
                        state=(%s), 
                        zip=(%s), 
                        phone=(%s), 
                        email=(%s) where customer_id = %s RETURNING *''')

        customer_data = get_customer(customer_id)
        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    print(customer_data)
                    cur.execute(command, ( data.get("last_name") or customer_data.get('body').get("last_name"),
                                        data.get("first_name") or customer_data.get('body').get("first_name"),
                                        data.get("middle_initial") or customer_data.get('body').get("middle_initial") ,
                                        data.get("street") or customer_data.get('body').get("street"),
                                        data.get("city") or customer_data.get('body').get("city"),
                                        data.get("state") or customer_data.get('body').get("state"),
                                        data.get("zip") or customer_data.get('body').get("zip"),
                                        data.get("phone") or customer_data.get('body').get("phone"),
                                        data.get("email") or customer_data.get('body').get("email"),
                                        customer_id)
                            )
                    conn.commit()
                    updated_data = cur.fetchone()
                    if updated_data is None:
                        body = None
                    else:
                        print("updated data")
                        body = Customer(*updated_data)
                    return body

        except Exception as e:
            print(e)

        return None

    def delete_customer(customer_id):
        command = ("DELETE FROM customers WHERE customer_id = %s")

        try:
            with psycopg.connect(host="localhost", port="5432", dbname="postgres", user="postgres",
                                password="zxcvbnm") as conn:
                with conn.cursor() as cur:
                    cur.execute(command, [customer_id], binary=True)
                    conn.commit()
                    # Check number of rows that were deleted
                    rows_deleted = cur.rowcount
                    
                    if rows_deleted != 1:
                        return False
                    else: 
                        conn.commit()
                        return True

        except Exception as e:
            print(e)
        return False
   
  #------------------------------------------------------------------------
  
  
  class Account(): 
    def __init__(self, account_id, date_opened, description, account_type_code, balance, customer_id):
        self.account_id = account_id
        self.date_opened = date_opened
        self.description = description
        self.balance = balance
        self.account_type_code = account_type_code
        self.customer_id = customer_id

    def to_dict(self):
        '''
        This function is used return dictionary of the account object
        '''
        return {
            "account_id": self.account_id,
            "date_opened": self.date_opened,
            "description": self.description,
            "balance": self.balance,
            "account_type_code": self.account_type_code,
            "customer_id": self.customer_id       
        }
      
#       ------------------------------------------------------------------------

class Customer:
    def __init__(customer_id, first_name, last_name, middle_initial, street, city, state, zip, phone, email)
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.middle_initial = middle_initial
        self.street =  street
        self.city =  city
        self.state = state
        self.zip =  zip
        self.phone = phone
        self.email = email
 
    def to_dict(self):
        '''
        This function is used return dictionary of the customer object
        '''
        return  {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_initial": self.middle_initial,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "phone": self.phone,
            "email" self.email
        }
      
#       ---------------------------------------------------------------------------------------

from dao.customer_dao import CustomerDao
# from exception.invalid_parameter import InvalidParameterError
# from exception.user_already_exists import UserAlreadyExistsError
from exception.customer_exception import CustomerNotFoundError


class CustomerService:

    def __init__(self):
        self.customer_dao = CustomerDao()

    # Get a list of User objects from the DAO layer
    # convert the User objects into dictionaries
    # return a list of dictionaries that each represent the users
    def get_all_customers(self):
        list_of_customer_objects = self.customer_dao.get_customers()

        # Method #1, use a for loop and do it manually
        list_of_customer_dictionaries = []
        for customer_obj in list_of_customer_objects:
            list_of_customer_dictionaries.append(customer_obj.to_dict())

        return list_of_customer_dictionaries

        # Method #2, use map
        # return list(map(lambda x: x.to_dict(), list_of_user_objects))
    
    # Get User object from DAO and convert into a dictionary
    def get_customer_by_id(self, customer_id):
        customer_obj = self.customer_dao.get_customer(customer_id)  
        # object

        if customer_obj is None:
            raise CustomerNotFoundError(f"Customer with id {customer_id} was not found")

        return customer_obj.to_dict()

    # If user is deleted successfully, then return None (implicitly)
    # If user does not exist, raise UserNotFoundException
    def delete_customer_by_id(self, customer_id):
        # Execute this block of code if user_dao.delete_user_by_id returns False (which means that we did not delete
        # any record)
        if not self.customer_dao.delete_customer(customer_id):
            raise CustomerNotFoundError(f"Customer with id {customer_id} was not found")

    # 1. Check if username is at least 6 characters
    # 2. Check if username contains spaces (not allowed)
    # 3. Check if user already exists
    # Invoke add_user in DAO, passing in a user_object
    # Return the dictionary representation of the return value from that method
    def add_customer(self, customer_objs):
        # Validate data before posting 

        added_customer_object = [] 
        for customer in customer_objs:
            added_customer_object.append(self.customer_dao.insert_customers(customer))
            
        return added_customer_object.to_dict()

    def update_customer_by_id(self, customer_id, customer_obj):
        updated_customer_object = self.customer_dao.update_customer(customer_id, customer_obj)

        if updated_customer_object is None:
            raise CustomerNotFoundError(f"Customer with id {customer_obj.customer_id} was not found")

        return updated_customer_object.to_dict()
#       ------------------------------------------------------------------------------------------------

from dao.account_dao import AccountDao
# from exception.invalid_parameter import InvalidParameterError
# from exception.user_already_exists import UserAlreadyExistsError
from exception.account_exception import AccountNotFoundError


class AccountService:

    def __init__(self):
        self.account_dao = AccountDao()

    # Get a list of User objects from the DAO layer
    # convert the User objects into dictionaries
    # return a list of dictionaries that each represent the users
    def get_all_accounts(self, amountGreaterThan, amountLessThan):
        list_of_account_objects = self.account_dao.get_accounts(amountGreaterThan, amountLessThan)

        # Method #1, use a for loop and do it manually
        list_of_account_dictionaries = []
        for account_obj in list_of_account_objects:
            list_of_account_dictionaries.append(account_obj.to_dict())

        return list_of_account_dictionaries

        # Method #2, use map
        # return list(map(lambda x: x.to_dict(), list_of_user_objects))

    def get_all_customer_account(self, customer_id, amountGreaterThan, amountLessThan):
        list_of_customer_account_objects = self.account_dao.get_customer_account(customer_id, amountGreaterThan, amountLessThan)

        # Method #1, use a for loop and do it manually
        list_of_account_dictionaries = []
        for account_obj in list_of_account_objects:
            list_of_account_dictionaries.append(account_obj.to_dict())

        return list_of_account_dictionaries
    
    # Get User object from DAO and convert into a dictionary
    def get_account_by_id(self, account_id):
        account_obj = self.account_dao.get_account(account_id)  
        # object

        if account_obj is None:
            raise AccountNotFoundError(f"Account with id {account_id} was not found")

        return account_obj.to_dict()

    # If user is deleted successfully, then return None (implicitly)
    # If user does not exist, raise UserNotFoundException
    def delete_account_by_id(self, account_id):
        # Execute this block of code if user_dao.delete_user_by_id returns False (which means that we did not delete
        # any record)
        if not self.account_dao.delete_account(account_id):
            raise AccountNotFoundError(f"Account with id {account_id} was not found")

    # 1. Check if username is at least 6 characters
    # 2. Check if username contains spaces (not allowed)
    # 3. Check if user already exists
    # Invoke add_user in DAO, passing in a user_object
    # Return the dictionary representation of the return value from that method
    def add_account(self, customer_id, account_objects):
        # Validate data before posting 

        added_account_object = [] 
        for acccount_obj in account_objects:
            added_account_object.append(self.account_dao.insert_accounts(customer_id, acccount_obj))
            
        return added_account_object.to_dict()

    def update_account_by_id(self, account_id, account_obj):
        updated_account_object = self.account_dao.update_account(account_id, account_obj)

        if updated_account_object is None:
            raise AccountNotFoundError(f"Account with id {account_obj.account_id} was not found")

        return updated_account_object.to_dict()
