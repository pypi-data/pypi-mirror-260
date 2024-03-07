from json import JSONDecodeError
import requests

__version__ = '0.3.2'

class WealthBox(object):
    def __init__(self, token=None):
        self.token = token
        self.user_id = None
        self.base_url = f"https://api.crmworkspace.com/v1/"
    
    def api_request(self, endpoint, params=None):
        url = self.base_url + endpoint
        page = 1
        total_pages = 9999999999
        if params is None:
            params = {}
        
        params.setdefault('per_page', '5000')
        results = []

        while page <= total_pages:
            params['page'] = page
            res = requests.get(url,
                            params=params,
                            headers={'ACCESS_TOKEN': self.token})
            try:
                res_json = res.json()
                if 'meta' not in res_json:
                    total_pages = 1
                    results = res_json
                else:
                    total_pages = res_json['meta']['total_pages']
                    # The WB API usually (always?) returns a list of results under a key with the same name as the endpoint
                    try:
                        results.extend(res_json[endpoint.split('/')[-1]]) 
                    except KeyError:
                        print(f"Error: {res_json}")
                        return f"Error: {res.text}"
                page += 1
            except JSONDecodeError:
                return f"Error Decoding: {res.text}"

        return results
    
    def api_put(self, endpoint, data):
        url = self.base_url + endpoint
        res = requests.put(url,
                            json=data,
                            headers={'ACCESS_TOKEN': self.token})
        try:
            res_json = res.json()
        except JSONDecodeError:
            return f"Error Decoding: {res.text}"
        return res.json()
       
    def get_contacts(self, filters=None):
        return self.api_request('contacts',params=filters)

    def get_tasks(self, filters=None):
        return self.api_request('tasks',params=filters)
    
    def get_workflows(self, resource_id=None, resource_type=None, status=None):
        params = {}
        if resource_id:
            params['resource_id'] = resource_id
        if resource_type:
            params['resource_type'] = resource_type
        if status:
            params['status'] = status
        return self.api_request('workflows',params=params)
    
    def get_events(self, resource_id=None, resource_type=None):
        params = {}
        if resource_id:
            params['resource_id'] = resource_id
        if resource_type:
            params['resource_type'] = resource_type
        return self.api_request('events',params=params)
    
    def get_opportunities(self, resource_id=None, resource_type=None, order='asc', include_closed=True):
        params = {}
        if resource_id:
            params['resource_id'] = resource_id
        if resource_type:
            params['resource_type'] = resource_type
        if order:
            params['order'] = order
        if include_closed:
            params['include_closed'] = include_closed
        return self.api_request('opportunities',params=params)
    
    def get_notes(self, resource_id=None, resource_type=None,order="asc"):
        params = {}
        if resource_id:
            params['resource_id'] = resource_id
        if resource_type:
            params['resource_type'] = resource_type
        return self.api_request('notes',params=params)

    def get_tags(self, document_type=None):
        params = {}
        if document_type:
            params['document_type'] = document_type
        return self.api_request('categories/tags',params=params)
    
    def get_comments(self, resource_id=None, resource_type=None):
        params = {}
        if resource_id:
            params['resource_id'] = resource_id
        if resource_type:
            params['resource_type'] = resource_type
        return self.api_request('comments',params=params)

    def get_my_user_id(self):
        #This endpoint doesn't have a 'meta'?
        self.user_id = self.api_request('me')['current_user']['id']
        return self.user_id

    def get_my_tasks(self):
        if self.user_id is None:
            self.get_my_user_id()
        return self.get_tasks({'assigned_to':self.user_id})

    def get_custom_fields(self,document_type=None):
        if document_type:
            params = {'document_type':document_type}
        else:
            params = None
        return self.api_request('categories/custom_fields',params=params)
    
    def update_contact(self,contact_id,updates_dict,custom_field=None):
        # Update a contact in WealthBox with a given ID and field data
        #TODO: Add custom field update
        return self.api_put(f'contacts/{contact_id}',updates_dict)
        
        
        
