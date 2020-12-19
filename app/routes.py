#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""HTTP route definitions"""

from flask import request, render_template, redirect, url_for
from app import app, lman
from app.database import create, read, update, delete, scan, create_comment, get_comments_for
import app.usersdb as udb
from datetime import datetime
from app.forms.product import ProductForm
from app.forms.login import LoginForm
from app.forms.register import RegisterForm
from app.forms.comment import CommentForm
from .models import User
from flask_login import login_user, current_user, login_required, logout_user

@lman.user_loader
def load_user(user_id):
    u = udb.read(user_id)['body']
    if len(u) == 0:
        return None
    u = u[0]
    user = User(
        u['id'],
        u['first_name'],
        u['last_name'],
        u['username'],
        u['is_admin'],
        u['billing_addr1'],
        u['billing_addr2'],
        u['biliing_city'],
        u['billing_state'],
        u['billing_postalcode'],
        u['billing_country'],
        u['shipping_addr1'],
        u['shipping_addr2'],
        u['shipping_city'],
        u['shipping_state'],
        u['shipping_postalcode'],
        u['shipping_contry'],
        u['phone'],
        u['phone_alt'],
        True,
        False)
    return user

@app.route("/")
def get_all_products():
    out = scan()
    out["ok"] = True
    out["message"] = "Success"
    return render_template("products.html", products=out['body'])


@app.route("/status")
def index():
    serv_time = datetime.now().strftime("%F %H:%M:%S")
    return {
        "ok": True,
        "version": "1.0.0",
        "server_time": serv_time
    }
    

@app.route("/details/<pid>", methods=["GET", "POST"])
def get_product_detils(pid):
    out = read(int(pid))
    frm = CommentForm()
    if request.method == "POST" and current_user.is_authenticated:
        cmt = str(request.form.get('comment')).strip()
        if len(cmt) > 0:
            create_comment(pid, current_user.id, cmt)
    
    comments = get_comments_for(pid)['body']
    return render_template('product_detail.html', details=out['body'][0], form=frm, comments=comments)

@app.route("/register", methods=["POST", "GET"])
def get_register():
    if request.method == "GET":
        form = RegisterForm()
        return render_template('register.html', form=form)
    else:
        uid = udb.create(
            request.form.get('first_name'), 
            request.form.get('last_name'), 
            request.form.get('username'), 
            False, 
            request.form.get('billing_addr1'),
            request.form.get('billing_addr2'),
            request.form.get('biliing_city'),
            request.form.get('billing_state'),
            request.form.get('billing_postalcode'),
            request.form.get('billing_country'),
            request.form.get('shipping_addr1'),
            request.form.get('shipping_addr2'),
            request.form.get('shipping_city'),
            request.form.get('shipping_state'),
            request.form.get('shipping_postalcode'),
            request.form.get('shipping_contry'),
            request.form.get('phone'),
            request.form.get('phone_alt')
        )
        login_user(User(
            uid,
            request.form.get('first_name'), 
            request.form.get('last_name'), 
            request.form.get('username'), 
            False, 
            request.form.get('billing_addr1'),
            request.form.get('billing_addr2'),
            request.form.get('biliing_city'),
            request.form.get('billing_state'),
            request.form.get('billing_postalcode'),
            request.form.get('billing_country'),
            request.form.get('shipping_addr1'),
            request.form.get('shipping_addr2'),
            request.form.get('shipping_city'),
            request.form.get('shipping_state'),
            request.form.get('shipping_postalcode'),
            request.form.get('shipping_contry'),
            request.form.get('phone'),
            request.form.get('phone_alt')
        ))
        return redirect(url_for('get_all_products'))
        

@app.route("/login")
def get_login():
    form = LoginForm()
    return render_template('login.html', form=form)

@login_required
@app.route("/edit_product/<pid>", methods=["GET", "POST"])
def edit_product(pid):
    if request.method == "GET":
        out = read(int(pid))['body'][0]
        form = ProductForm(data=out)
        return render_template("edit_product.html", form=form)
    else:
        data = {
            'name': request.form.get('name'),
            'price': request.form.get('price'),
            'category': request.form.get('category'),
            'description': request.form.get('description'),
            'img': request.form.get('img'),
            'shipping_price': request.form.get('shipping_price'),
            'brand_name': request.form.get('brand_name'),
        }
        update(int(pid), data)
        return redirect(url_for('get_product_detils', pid=pid))
    

@app.route("/products/<pid>")
def get_one_product(pid):
    out = read(int(pid))
    out["ok"] = True
    out["message"] = "Success"
    return out


@app.route("/products", methods=["POST"])
def create_product():
    product_data = request.json
    new_id = create(
        product_data.get("name"),
        product_data.get("price"),
        product_data.get("category"),
        product_data.get("description")
    )

    return {"ok": True, "message": "Success", "new_id": new_id}


@app.route("/products/<pid>", methods=["PUT"])
def update_product(pid):
    product_data = request.json
    out = update(int(pid), product_data)
    return {"ok": out, "message": "Updated"}


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
