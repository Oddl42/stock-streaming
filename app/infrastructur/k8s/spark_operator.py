#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:02:20 2026

@author: twi
"""

from kubernetes import client, config

def load_k8s():
    # im Cluster:
    config.load_incluster_config()

def spark_custom_api():
    return client.CustomObjectsApi()

GROUP = "sparkoperator.k8s.io"
VERSION = "v1beta2"
PLURAL = "sparkapplications"

def create_spark_application(namespace: str, body: dict):
    load_k8s()
    api = spark_custom_api()
    return api.create_namespaced_custom_object(GROUP, VERSION, namespace, PLURAL, body)

def delete_spark_application(namespace: str, name: str):
    load_k8s()
    api = spark_custom_api()
    return api.delete_namespaced_custom_object(GROUP, VERSION, namespace, PLURAL, name)

def get_spark_application(namespace: str, name: str):
    load_k8s()
    api = spark_custom_api()
    return api.get_namespaced_custom_object(GROUP, VERSION, namespace, PLURAL, name)
