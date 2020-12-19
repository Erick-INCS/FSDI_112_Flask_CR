from flask import g
import sqlite3

DATABASE="catalog_db"

def get_db():
    db = getattr(g, "_database", None)
    if not db:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def output_formatter(results: tuple):
    out = {"body":[]}
    for result in results:
        res_dict = {}
        res_dict["id"] = result[0]
        res_dict["first_name"] = result[1]
        res_dict["last_name"] = result[2]
        res_dict["username"] = result[4]
        res_dict["is_admin"] = result[3]
        res_dict["billing_addr1"] = result[5]
        res_dict["billing_addr2"] = result[6]
        res_dict["biliing_city"] = result[7]
        res_dict["billing_state"] = result[8]
        res_dict["billing_postalcode"] = result[9]
        res_dict["billing_country"] = result[10]
        res_dict["shipping_addr1"] = result[11]
        res_dict["shipping_addr2"] = result[12]
        res_dict["shipping_city"] = result[13]
        res_dict["shipping_state"] = result[14]
        res_dict["shipping_postalcode"] = result[15]
        res_dict["shipping_contry"] = result[16]
        res_dict["phone"] = result[17]
        res_dict["phone_alt"] = result[18]
        
        out['body'].append(res_dict)
    return out

def scan():
    cursor = get_db().execute("select * from user", ())
    result = cursor.fetchall()
    cursor.close()
    return output_formatter(result)

def read(usr_id):
    query = """
        select *
        from user
        where id = ?
    """
    cursor = get_db().execute(query, (usr_id,))
    result = cursor.fetchall()
    cursor.close()
    return output_formatter(result)

def update(usr_id, fields: dict):
    field_string = ", ".join(
        "%s=\"%s\"" % (key, val)
            for key, val
            in fields.items())
    query = """
            update user
            set %s
            where id = ?
            """ % field_string

    cursor = get_db()
    cursor.execute(query, (usr_id,))
    cursor.commit()
    return True

def create(first_name, last_name, username, is_admin=False, billing_addr1="", billing_addr2="", biliing_city="", billing_state="", billing_postalcode="", billing_country="", shipping_addr1="", shipping_addr2="", shipping_city="", shipping_state="", shipping_postalcode="", shipping_contry="", phone="", phone_alt=""):
    value_tuple = (first_name, last_name, is_admin, username, billing_addr1, billing_addr2, biliing_city, billing_state, billing_postalcode, billing_country, shipping_addr1, shipping_addr2, shipping_city, shipping_state, shipping_postalcode, shipping_contry, phone, phone_alt)
    query = """
        INSERT INTO user (
            first_name, last_name, is_admin, username, billing_addr1, billing_addr2, biliing_city, billing_state, billing_postalcode, billing_country, shipping_addr1, shipping_addr2, shipping_city, shipping_state, shipping_postalcode, shipping_contry, phone, phone_alt)
        VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor = get_db()
    last_row_id = cursor.execute(query, value_tuple).lastrowid
    cursor.commit()
    return last_row_id


def delete(usr_id):
    query = "delete from user where id=%s" % usr_id
    cursor = get_db()
    cursor.execute(query, ())
    cursor.commit()
    return True
