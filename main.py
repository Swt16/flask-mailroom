'''
Shin Tran
Python 230
Assignment 1
Flask Mailroom
'''

import os
import base64
from flask import Flask, render_template, request, redirect, url_for, session
from model import Donor, Donation
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
#app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations = donations)


@app.route('/donors_donation/<string:donor_name>')
def donors_donation(donor_name):
    donor_object = Donor.select().where(Donor.name == donor_name).get()
    donations = Donation.select().where(Donation.donor == donor_object)
    return render_template('donors_donation.jinja2', donations = donations)


@app.route('/select/', methods = ['GET', 'POST'])
def select():
    if request.method == 'GET':
        return render_template('select.jinja2')
    if request.method == 'POST':
        try:
            donor_name = request.form['name']
            donor_object = Donor.select().where(Donor.name == donor_name)
        except Donor.DoesNotExist:
            donor_object = None
        if donor_object:
            return redirect(url_for('donors_donation', donor_name = donor_name))
            #return render_template('donors_donation.jinja2', donor_name = donor_name)
    else:
        return render_template('select.jinja2')

    

@app.route('/create/', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.jinja2')

    if request.method == 'POST':
        try:
            donor_name = request.form['name']
            donor_object = Donor.select().where(Donor.name == donor_name).get()
        except Donor.DoesNotExist:
            donor_object = None
        dn_amount = request.form['donation']
        if donor_object:
            donation = Donation(donor = donor_object, value = dn_amount)
            donation.save()
            return redirect(url_for('home'))
        else:
            new_donor = Donor(name = donor_name)
            new_donor.save()
            Donation(donor = new_donor, value = dn_amount).save()
            return render_template('create.jinja2')
    else:
        return render_template('create.jinja2')
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host = '0.0.0.0', port = port)

