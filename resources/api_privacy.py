from flask_restful import Resource,fields,marshal_with,reqparse
from common.database import not_existed,ok,add_policy,insert_record,delete_record,search_record,select_policy
from errors import PrivacyServerError
from datetime import datetime
import random
import string
from common.json_parser import list2json

'''
    The restful API was designed with the help of flask-restful
    It can deal with certain basic API functions like GET , POST, PUT, DELETE
    TO DO: Authentication Process and Visualization
'''

SCOPE = ["Clinician", "Researcher", "Patient", "Commercial", 'All']

def check_scope(scope_dict):
    #print scope_dict
    if scope_dict not in SCOPE:
        return False
    else:
        return True

def wrap_up(id_, patient_id, resource_Type, resource_Scope, resource_Policy):
    '''
    Set up the stored structure of privacy_policy
    TODO : implement it and make the structure more complete
    :param patient_id : Identifier of a patient
    :param resource_Type: policy for what type of resource
    :param resource_Scope: the policy should be applied to whom they read the data
    :param resource_policy: the policy it self, a json-dict form
    :return: sth can be inserted into database
    '''

    source =  {
            'ResourceIdentifier' : id_,
            'Policy_ResourceType': resource_Type,
            'Scope': resource_Scope,
            'patient_id' : patient_id,
            'Policy': resource_Policy
        }
    registered_id = string.join(random.sample(string.ascii_letters+string.digits, 8))
    registered_id = registered_id.replace(' ','')

    return {registered_id:source}

class Privacy(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Resource', required = True, action = 'append', type=dict,
                                   help= 'Must provide some resources')
        self.deal_error= PrivacyServerError()

    def get(self):
        '''
        multiple get is not tolerate in this demo!
        :return:
        '''
        self.deal_error.abort_with_unaccessable_error()

    def post(self):
        '''
        multiple post for a list ot privacy_resource
        :return:
        '''
        args = self.reqparse.parse_args()
        #print args
        if len(args['Resource']) > 0 :
            for key in args['Resource']:
                #print key
                if 'Identifier' in key and 'Policy' in key and 'resourceType' in key and 'resourceID' in key:
                    if 'Scope' in key and check_scope(key['Scope']):
                        try:
                            add_policy(key['resourceID'],wrap_up(key['resourceID'],key['Identifier'],key['resourceType'],key['Scope'],key['Policy']),datetime.now())
                        except:
                            insert_record(key['resourceID'],wrap_up(key['resourceID'],key['Identifier'],key['resourceType'],key['Scope'],key['Policy']),datetime.now())
                    else:
                        try:
                            add_policy(key['resourceID'],wrap_up(key['resourceID'],key['Identifier'],key['resourceType'],key['Scope'],key['Policy']),datetime.now())
                        except:
                            insert_record(key['resourceID'],wrap_up(key['resourceID'],key['Identifier'],key['resourceType'],key['Scope'],key['Policy']),datetime.now())
                else:
                    self.deal_error.abort_with_POST_error()
        return "Ok", 200

class PrivacyList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        #self.reqparse.add_argument('UpdatePolicy', type=dict, help = 'Must provide update info.')
        self.reqparse.add_argument('Policy', type= dict, help= 'Must provide some Policy if post new one')
        self.reqparse.add_argument('Identifier', type= str, help= 'Must provide Identifier')
        self.reqparse.add_argument('resourceType', type= str, help= 'Must provide resourceType')
        self.reqparse.add_argument('resourceID', required= True, type= str, help= 'Must provide resourceID ')
        self.reqparse.add_argument('Scope', type= str, help ='Must provide apply scope.', default= 'All')
        self.deal_error= PrivacyServerError()

        self.getparse = reqparse.RequestParser()
        self.getparse.add_argument('Scope', type = str , location = 'args')
        self.getparse.add_argument('resourceType', type = str , location = 'args')
        self.getparse.add_argument('resourceID', type = str , location = 'args')


    def get(self,id_):
        '''
        single read/search, not available with partial search now
        :param privacy_id:
        :return:
        '''
        args = self.getparse.parse_args()

        search_result = select_policy(id_)
        if search_result == not_existed:
            self.deal_error.abort_with_search_error(id_)
        print search_result

        return {'Identifier' : id_, 'Resource': search_result}

    def post(self,id_):
        '''
        Single post
        :param patient_id:
        :return:
        '''
        args = self.reqparse.parse_args()
        print args
        if args['Policy'] is None or args['Identifier'] is None or args['resourceType'] is None:
            self.deal_error.abort_with_POST_error()
        if not check_scope(args['Scope']):
            self.deal_error.abort_with_Scope_error()
        #if patient_id != args['Identifier']:
        #    self.deal_error.abort_with_POST_error()
        if search_record(id_) == not_existed:
            insert_record(args['resourceID'],wrap_up(args['resourceID'],id_,args['resourceType'],args['Scope'],args['Policy']),datetime.now())
        else:
            return "You should use PUT method to update a policy", 200
        return select_policy(id_), 200

    def put(self,id_):
        '''
        Single put, it will modify the privacy_policy
        Simply, the Identifier is the same with patient_id and this put method might directly merge these data.
        The best way is to first DELETE then PUT if you want to create a new policy
        :param patient_id:
        :return:
        '''
        print 'here'
        args = self.reqparse.parse_args()

        if args['Policy'] is None or args['Identifier'] is None or args['resourceType'] is None:
            self.deal_error.abort_with_POST_error()
        if not check_scope(args['Scope']):
            self.deal_error.abort_with_Scope_error()
        #if patient_id != args['Identifier']:
        #    self.deal_error.abort_with_POST_error()
        print args
        if search_record(id_) == not_existed:
            insert_record(args['resourceID'],wrap_up(args['resourceID'],args['Identifier'],args['resourceType'],args['Scope'],args['Policy']),datetime.now())
        else:
            add_policy(args['resourceID'],wrap_up(args['resourceID'],args['Identifier'],args['resourceType'],args['Scope'],args['Policy']),datetime.now())
        print select_policy(id_)

        return {'Identifier' : id_,  'Resource': select_policy(id_)},200

    def delete(self,id_):
        if search_record(id_) == ok:
            delete_record(id_)
            return 'Successfully deleted {}'.format(id_), 200
        else:
            return 'No record!', 201


if __name__=='__main__':
    a = {1:{1:'a',2:'b',3:'c'}, 2:{4:'d',5:'e',6:'f'}}
    b = {'Resource':a}
    print b