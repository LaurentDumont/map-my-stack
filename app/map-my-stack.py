#!/usr/bin/python
# coding: utf-8


# Site ---> Project ---> HostAggregates ---> Computes ---> VM

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request as request_flask
from collections import defaultdict
import openstack

app = Flask(__name__)

auth_url = 'http://10.10.99.44:35357/v3'
project_name = 'admin'
username = 'admin'
password = 'bTc6oMX8TMHgGYZ7vngZgzJZgQoyWFcWLJqvaoVt'
region = 'RegionOne'
user_domain = 'Default'
project_domain = 'Default'


def create_openstack_session():
    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region,
        user_domain_name=user_domain,
        project_domain_name=project_domain,
    )


@app.route('/healthcheck')
def default():
    return 'Goliath online'


@app.route('/get_servers_form')
def get_servers_form():
    return render_template('form.html')


@app.route('/get_servers', methods=["POST"])
def get_servers():
    post_data = request_flask.form
    if request_flask.json is None:
        post_data = request_flask.form
    else:
        post_data = request_flask.json
    openstack_session = create_openstack_session()

    # Get all host aggregates (we cannot filter per project)
    aggregates_list = []
    aggregates = openstack_session.list_aggregates()
    for aggregate in aggregates:
        aggregates_list.append(aggregate)
    # Get the project ID because we need that for filtering.
    project = openstack_session.identity.find_project(
        post_data['project'], ignore_missing=True)
    if project is None:
        return "Project not found!", 400

    computes_list = []
    servers_list = []
    computes_servers_mapping = defaultdict(list)

    servers = openstack_session.compute.servers(
        all_projects=True, project_id=project.id)

    temp_list = []
    for server in servers:
        temp_list_1 = []
        temp_list_1.append(server.hypervisor_hostname)
        temp_list_1.append(server.hostname)
        temp_list.append(temp_list_1)

    for compute, server in temp_list:
        computes_servers_mapping[compute].append(server)

    # servers_list.append(server.hostname)
    # computes_list.append(server.hypervisor_hostname)

    set_computes = set(computes_list)
    computes_list = list(set_computes)
    return jsonify(computes_servers_mapping)
