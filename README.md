# Privacy_Server

This little server is developed to solve Privacy_Issue [FHIR-Genomics-2](https://github.com/chaiery/FHIR-Genomics-2)
It should make full usage combined with [this proxy server](https://github.com/Reimilia/Proxy_Server)


## Preparation

```sudo pip install -r requirements.txt```

```sudo apt-get install postgresql```

read ./resources/common/db_config.py to settle your own postgresql database
after check of configuration, run ```python setup_db.py``` to set up database for this server

At this part , however, there might be a huge potential problem: setup_db.py might only create
with users of your current user name in UNIX systems, and we don't know how to fix it, you can solve this problem by
following the error message and comply with its setting. (The database will be set, yet not belongs to a desired user.)


## How to use

run server_index.py and you can use curl to test it

For debug purpose, we recommend you to start with
```python server_index.py -d```

The original port is settled at ```http://localhost:5000```, you can change it in server_index.py

To see how to debug or deploy this server, you can run ```example.py``` to see its basic structure

Generally, POST needs at least three arguments:

*   Identifier
*   resourceType (Which means type of hidden policy)
*   Policy

PUT is quite similar , and GET will get a response like this:
```
{
    "Identifier": "f01f00a3-a38a-4401-a3e4-53c4239badb4", 
    "Resource": {
        "Patient": {
            "gender": "Protected"
        }
    }
}
```

## Development Status and Further Extension

- [x] **Privacy_Server (Which designed to store policy and get interact with submitter)**
    - [ ] RESTful API design
        - [x] GET full policy data
        - [ ] GET with searching parameters
        - [ ] GET history version
        - [x] POST policy data
        - [x] PUT method to update(or insert data)
        - [x] DELETE method to clean up a policy data
        - [ ] Access with full authetication

    - [ ] Method to login and modify privacy policy
        - [ ] Visualize Component
        - [ ] Basic Submitting Forms