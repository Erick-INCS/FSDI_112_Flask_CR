class User():
    def __init__(self, id, first_name, last_name, username, is_admin=False, billing_addr1="", billing_addr2="", biliing_city="", billing_state="", billing_postalcode="", billing_country="", shipping_addr1="", shipping_addr2="", shipping_city="", shipping_state="", shipping_postalcode="", shipping_contry="", phone="", phone_alt="", auth=False, anonimous=True):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.username = username
        self.billing_addr1 = billing_addr1
        self.billing_addr2 = billing_addr2
        self.biliing_city = biliing_city
        self.billing_state = billing_state
        self.billing_postalcode = billing_postalcode
        self.billing_country = billing_country
        self.shipping_addr1 = shipping_addr1
        self.shipping_addr2 = shipping_addr2
        self.shipping_city = shipping_city
        self.shipping_state = shipping_state
        self.shipping_postalcode = shipping_postalcode
        self.shipping_contry = shipping_contry
        self.phone = phone
        self.phone_alt = phone_alt
        self.auth = auth
        self.anonimous = anonimous
        
    def is_authenticated(self):
        return self.auth
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return self.anonimous

    def get_id(self):
        return self.id