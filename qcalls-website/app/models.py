# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
import requests
import json
url = "https://qcalls-damnik.harperdbcloud.com"

class Map(dict):
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

class OperationsHarperDB(models.Manager):
    def get(self, email=None):
        global url
        payload ={
            "operation":"sql",
            "sql":"select * from sync.operation where email = '"+self.email+"'"
        }
        # payload = {
        #     "operation":"search_by_value",
        #     "schema":"sync",
        #     "table":"operation",
        #     "search_attribute":"email",
        #     "search_value":email,
        #     "get_attributes":["*"]
        # }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return Map(response.json()[0])

    def create(self, email=None, operations=None):
        global url
        insert_json = {
            "email":email,
            "operations":operations
          } 
        payload = {
            "operation":"insert",
            "schema":"sync",
            "table":"operation",
            "records": [
              insert_json
            ]
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return Map(insert_json)

class Operations(models.Model):
    email = models.CharField(max_length=100,primary_key=True)
    operations = models.CharField(max_length=1000)
    # objects = OperationsHarperDB()
    # def save(self):
    #     global url
    #     # operations = json.dumps(self.operations)
    #     payload ={
    #         "operation":"sql",
    #         "sql":"update sync.operation set operations = \""+str(self.operations)+"\" where email = '"+self.email+"'"
    #     }
    #     payload = json.dumps(payload)
    #     headers = {
    #         'Content-Type': "application/json",
    #         'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
    #         }
    #     response = requests.request("POST", url, data=payload, headers=headers)
    #     return response.json

class Participants(models.Model):
    mainorg = models.CharField(max_length=100,primary_key=True)
    participant = models.CharField(max_length=10000)

class Transcript(models.Model):
    meeting_id = models.CharField(max_length=100,primary_key=True)
    transcript = models.CharField(max_length=100000)
    audio_file = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    status = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)

