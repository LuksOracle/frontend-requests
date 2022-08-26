from bridge import Bridge
import os

print('og')
class Adapter:
#    base_url = "https://api.twitter.com/2/users/1018093644/tweets?max_results=5"
#    from_params = ['base', 'from', 'coin']
#    to_params = ['quote', 'to', 'market']

    def __init__(self, input):
#        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        print(self.request_data)
        return True
        

    def set_params(self):
        self.twitter_id = int(self.request_data.get("twitter_id"))
        print(self.twitter_id)
        # for param in self.from_params:
        #     self.from_param = self.request_data.get(param)
        #     if self.from_param is not None:
        #         break
        # for param in self.to_params:
        #     self.to_param = self.request_data.get(param)
        #     if self.to_param is not None:
        #         break

    def create_request(self):
        try:
            params = {
                'id' : self.twitter_id
            }

            headers = {
                "Authorization": "Bearer " + os.environ.get('BEARER_TOKEN')
                }
            
            # twitter api
            base_url="https://api.twitter.com/2/users?ids={}&user.fields=id,name,profile_image_url,username".format(params['id']) 
           
            response = self.bridge.request(base_url, headers=headers)

            # response from external api
            self.result = response.json()
            self.result_success(self.result)

        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
#            'jobRunID': self.id,
#            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
#            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
