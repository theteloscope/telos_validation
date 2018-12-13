import requests


class telosnetinfo:

    def __init__(self, node_url):
        self.node_url = node_url

    def account_exists(self, account_name):
        url = self.node_url + '/v1/chain/get_account'

        response = requests.post(url, json={"account_name": account_name})

        if(response.status_code == 200):
            return True

        else:
            return False


    def get_liquid_balance(self, account_name):
        url = self.node_url + '/v1/chain/get_account'


        response = requests.post(url, json={"account_name": account_name})

        if (response.status_code == 200):
            json = response.json()

            return json['core_liquid_balance']


    def get_total_balance(self, account_name):
        url = self.node_url + '/v1/chain/get_account'

        response = requests.post(url, json={"account_name": account_name})

        if (response.status_code == 200):
            json = response.json()
            if 'core_liquid_balance' in json:
                liquid = float(json['core_liquid_balance'].split(' ', 1)[0])
            else:
                liquid = 0.0
            return  liquid + float(json['net_weight'])/10000.0 + float(json['cpu_weight'])/10000.0
        else:
            return ''


    def account_owner_key(self, account_name):
        url = self.node_url + '/v1/chain/get_account'


        response = requests.post(url, json={"account_name": account_name})
        if (response.status_code == 200):
            json = response.json()
            return json['permissions'][1]['required_auth']['keys'][0]['key']
        else:
            return ''


    def get_balance_and_owner_key(self, account_name):
        url = self.node_url + '/v1/chain/get_account'

        response = requests.post(url, json={"account_name": account_name})

        if (response.status_code == 200):
            json = response.json()
            if 'core_liquid_balance' in json:
                liquid = float(json['core_liquid_balance'].split(' ', 1)[0])
            else:
                liquid = 0.0

            liquid = liquid + float(json['net_weight']) / 10000.0 + float(json['cpu_weight']) / 10000.0

            return [liquid, json['permissions'][1]['required_auth']['keys'][0]['key']]
        else:
            return[0, '']