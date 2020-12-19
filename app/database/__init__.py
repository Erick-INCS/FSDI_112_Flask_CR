from flask import g
import sqlite3

DATABASE="catalog_db"


def get_db():
    db = getattr(g, "_database", None)
    if not db:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def output_formatter(results: tuple):
    out = {"body": []}
    for result in results:
        res_dict = {}
        res_dict["id"] = result[0]
        res_dict["name"] = result[1]
        res_dict["price"] = result[2]
        res_dict["category"] = result[3]
        res_dict["description"] = result[4]
        res_dict["active"] = result[5]
        res_dict["img"] = result[6]
        res_dict["shipping_price"] = result[7]
        res_dict["brand_name"] = result[8]
        out["body"].append(res_dict)
    return out


def comment_formatter(results: tuple):
    out = {"body": []}
    for result in results:
        res_dict = {}
        res_dict["comment"] = result[0]
        res_dict["username"] = result[1]
        out["body"].append(res_dict)
    return out


def scan():
    cursor = get_db().execute("SELECT * FROM product", ())
    results = cursor.fetchall()
    cursor.close()
    return output_formatter(results)


def read(prod_id):
    query = """
        SELECT *
        FROM product
        WHERE id = ?
        """
    cursor = get_db().execute(query, (prod_id,))
    results = cursor.fetchall()
    cursor.close()
    return output_formatter(results)


def get_comments_for(pid):
    query = """
        SELECT pc.comment, u.username
        FROM product_comment AS pc
        INNER JOIN user AS u ON u.id = pc.uid
        WHERE pc.pid = ?
        """
    cursor = get_db().execute(query, (pid,))
    results = cursor.fetchall()
    cursor.close()
    return comment_formatter(results)

def create_comment(pid, uid, comment):
    value_tuple = (pid, uid, comment)
    query = """
            INSERT INTO product_comment (
                    pid, uid, comment)
            VALUES (?, ?, ?)
        """
    cursor = get_db()
    last_row_id = cursor.execute(query, value_tuple).lastrowid
    cursor.commit()
    return last_row_id


def update(prod_id, fields: dict):
    field_string = ", ".join(
                    "%s=\"%s\"" % (key, val)
                        for key, val
                        in fields.items())
    query = """
            UPDATE product
            SET %s
            WHERE id = ?
            """ % field_string
    cursor = get_db()
    cursor.execute(query, (prod_id,))
    cursor.commit()
    return True


def create(name, price, category, description, img, shipping_price, brand_name):
    value_tuple = (name, price, category, description, img, shipping_price, brand_name)
    query = """
            INSERT INTO product (
                    name,
                    price,
                    category,
                    description,
                    img, shipping_price, brand_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
    cursor = get_db()
    last_row_id = cursor.execute(query, value_tuple).lastrowid
    cursor.commit()
    return last_row_id


def delete(prod_id):
    query = "DELETE FROM product WHERE id=%s" % prod_id
    cursor = get_db()
    cursor.execute(query, ())
    cursor.commit()
    return True