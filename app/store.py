import requests


def show_message(msg, extra):
    print(msg, extra)


class Store:
    def __init__(self, app, data_url, user):
        self.app = app
        self.data_url = data_url
        self.auth_token = None
        self.user = user

    def request_auth_token(self, user, password):
        self.auth_token = 'stoca'
        return
        ######################################################################
        url = self.data_url + '/auth/'
        data = {
            'username': user,
            'password': password,
        }
        r = requests.post(url, data=data)
        r.raise_for_status()
        self.auth_token = r.json()['token']

    def get_with_auth(self, token, endpoint):
        url = f'{self.data_url}{endpoint}/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def call_genericitems(self):
        return self.get_with_auth(self.auth_token, 'genericitems')

    def call_rackmaterials_real(self, obj_table):
        try:
            if self.auth_token is None:
                self.request_auth_token(*self.user)
            return self.get_with_auth(self.auth_token, 'rackmaterials')
        except requests.exceptions.HTTPError as errh:
            show_message("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            show_message("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            show_message("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            show_message('cannot connect', err)
        return []


    def get_rackmaterials(self, tipo, subtipo):
        try:
            if self.auth_token is None:
                self.request_auth_token(*self.user)
            return self.get_with_auth(self.auth_token, f"/cose/elettronica/rack/panels_main/{tipo}/{subtipo}")
        except requests.exceptions.HTTPError as errh:
            show_message("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            show_message("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            show_message("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            show_message('cannot connect', err)
        return []


    def get_rackmaterial(self, panel_id):
        try:
            if self.auth_token is None:
                self.request_auth_token(*self.user)
            return self.get_with_auth(self.auth_token, f"/cose/elettronica/rack/one_panel/{panel_id}")
        except requests.exceptions.HTTPError as errh:
            show_message("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            show_message("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            show_message("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            show_message('cannot connect', err)
        return []





    def image_url(self, pics, idx):
        try:
            pics_list = pics.split(',')
            pic = pics_list[idx].strip()
            return f'{self.data_url}/static/images/{pic}.jpg'
            
        except IndexError:
            pass
        except requests.exceptions.HTTPError as errh:
            show_message("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            show_message("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            show_message("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            show_message('cannot connect', err)
        return ""

    def big_image_url(self, pics, idx):
        try:
            pics_list = pics.split(',')
            pic = pics_list[idx].strip()
            return f'{self.data_url}/static/images-big/{pic}.jpg'
            
        except IndexError:
            pass
        
        return ""
    
    
    
    def call_rackmaterials_fake(self, obj_table):
        '''
          id: Optional[int] = Field(default=None, primary_key=True)
        tipo: str #= Field(default=None, primary_key=True)
        subtipo: str
        name: str
        descr: str
        barcode: str
        brand: str
        units: float
        quantity: int
        position: str
        pos_pics: str
        box_pics: str
        obj_pics: str
        comm: str
        '''

        return [
        {
            'id': 0,
            'tipo': 'pannello',
            'subtipo': 'cieco',
            'units': 1,
            'quantity': 8,
            'position': 'e030',
            'pos_pics': 'IMG_20220401_140434_4.jpg',
            'comm': 'd999',
        },
        {
            'id': 1,
            'units': 1,
            'quantity': 5,
            'position': 'e701',
            'pos_pics': 'IMG_20220401_140434_4.jpg',
            'comm': 'd800',
        },
        {
            'id': 2,
            'units': 2,
            'quantity': 10,
            'position': 'e031',
            'pos_pics': 'IMG_20220401_140434_4.jpg',
            'comm': 'd999',
        },
        {
            'id': 3,
            'units': 3,
            'quantity': 3,
            'position': 'e032',
            'pos_pics': 'IMG_20220401_140434_4.jpg',
            'comm': 'd999',
        },
        {
            'id': 4,
            'units': 3,
            'quantity': 3,
            'position': 'e701',
            'pos_pics': 'IMG_20220401_140434_4.jpg',
            'comm': 'd800',
        },
    ]

    #call_rackmaterials = call_rackmaterials_fake
    call_rackmaterials = call_rackmaterials_real

    def call_rackmaterial_fake(self, obj_table, id):
        return self.call_rackmaterials_fake(obj_table)[id]
        
    call_rackmaterial = call_rackmaterial_fake
    