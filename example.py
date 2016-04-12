import requests,json
from server_index import HOST
BASE = 'http://'+HOST+'/Privacy'

example_data={
    "Resource": [{
        "Identifier": "4b9f9ab9-d723-45d2-b185-3439a7f51690",
        "resourceID":"4b9f9ab9-d723-45d2-b185-3439a7f51690",
        "resourceType": "Patient",
        "Scope" : "Researcher",
        "Policy": {
            'gender' : 'Protected'
        }},
        {
        "Identifier": "4b9f9ab9-d723-45d2-b185-3439a7f51690",
        "resourceID":"4b9f9ab9-d723-45d2-b185-3439a7f51690",
        "Scope" : "Commercial",
        "resourceType": "Condition",
        "Policy": {
            "code": {
                "text": "Color blind",
                "coding": [{
                    "display": "internal blind",
                }]
            }

        }},
        {
        "Identifier": "f001",
        "resourceID":"f001",
        "Scope" : "Clinician",
        "resourceType": "Observation",
        "Policy": {
             "valueQuantity": {
                "value": '7.2'
                }
        }},
        {
        "Identifier": "f001",
        "resourceID":"f005",
        "Scope" : "Commercial",
        "resourceType": "Observation",
        "Policy": {
             "performer": {
                "display": "A. Langeveld",

            },
             "subject": {
                "display": "P. van de Heuvel",

            }
        }}]
    }

single_example_data={
    'Policy': {'gender': 'Protected', 'name': {'text': 'You cannot see it'}},
    'Identifier': 'f01f00a3-a38a-4401-a3e4-53c4239badb4',
    'resourceType': "Patient",
    'Scope': 'Clinician',
    'resourceID': 'f01f00a3-a38a-4401-a3e4-53c4239badb4',

    }



if __name__ == '__main__':
    resp = requests.delete('%s/4b9f9ab9-d723-45d2-b185-3439a7f51690' %BASE)
    print resp._content
    requests.delete('%s/f01f00a3-a38a-4401-a3e4-53c4239badb4' %BASE)
    requests.delete('%s/f001' %BASE)
    requests.delete('%s/f002' %BASE)
    requests.delete('%s/f005' %BASE)
    requests.delete('%s/ob-genetics-2' %BASE)
    requests.delete('%s/ob-genetics-1' %BASE)
    requests.delete('%s/example' %BASE)

    # headers cannot be omitted
    # TODO : make headers not a must argument
    resp = requests.post('%s' %(BASE), data=json.dumps(example_data), headers={'Content-Type': 'application/json'})
    print resp._content
    resp = requests.get('%s/f005' %BASE)
    print resp._content
    resp = requests.put('%s/f01f00a3-a38a-4401-a3e4-53c4239badb4' %BASE , data=json.dumps(single_example_data), headers={'Content-Type': 'application/json'})
    #resp = requests.put('%s/f01f00a3-a38a-4401-a3e4-53c4239badb4' %BASE , data=json.dumps(single_example_data), headers={'Content-Type': 'application/json'})
    #resp = requests.put('%s/f01f00a3-a38a-4401-a3e4-53c4239badb4' %BASE , data=json.dumps(single_example_data), headers={'Content-Type': 'application/json'})
    #resp = requests.put('%s/f01f00a3-a38a-4401-a3e4-53c4239badb4' %BASE , data=json.dumps(single_example_data), headers={'Content-Type': 'application/json'})
    #resp = requests.put('%s/f01f00a3-a38a-4401-a3e4-53c4239badb4' %BASE , data=json.dumps(single_example_data), headers={'Content-Type': 'application/json'})
    print resp._content
    #resp = requests.delete('%s/4b9f9ab9-d723-45d2-b185-3439a7f51690' %BASE)
    #print resp._content
    resp = requests.get('%s/4b9f9ab9-d723-45d2-b185-3439a7f51690' %BASE)
    print resp._content