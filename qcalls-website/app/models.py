# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
import requests
import json
import random
import datetime
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
            "sql":"select * from sync.operation where email = '"+email+"'"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        res = response.json()[0]
        res = Map(res)
        res.operations = json.loads(res.operations)
        return Map(res)

    def all(self):
        global url
        payload ={
            "operation":"sql",
            "sql":"select * from sync.operation"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return Map(response.json())

    def create(self, email=None, operations=None):
        global url
        insert_json = {
            "email":email,
            "operations":str(operations)
          } 
        update_payload = {
            "operation":"sql",
            "sql":"update sync.operation set operations = '"+json.dumps(operations)+"' where email = '"+email+"'"
        }
        insert_payload = {
            "operation":"insert",
            "schema":"sync",
            "table":"operation",
            "records": [
              insert_json
            ]
        }
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=json.dumps(update_payload), headers=headers)
        try:
            if response.json()['error']!='':
                response = requests.request("POST", url, data=json.dumps(insert_payload), headers=headers)
        except:
            pass
        return Map(insert_json)

class Operations(models.Model):
    email = models.CharField(max_length=100,primary_key=True)
    operations = models.CharField(max_length=1000)
    objects = OperationsHarperDB()
    def save(self):
        global url
        payload ={
            "operation":"sql",
            "sql":"update sync.operation set operations = \""+str(self.operations)+"\" where email = '"+self.email+"'"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return response.json

class ParticipantHarperDB(models.Manager):
    def get(self, mainorg=None):
        global url
        payload ={
            "operation":"sql",
            "sql":"select * from sync.participant where mainorg = '"+mainorg+"'"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        res = []
        try:
            res = response.json()[0]
            res = Map(res)
            # res.participant = json.loads(res.participant)
        except:
            pass
        return Map(res)

    def all(self):
        global url
        payload ={
            "operation":"sql",
            "sql":"select * from sync.participant"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return Map(response.json())

    def create(self, mainorg=None, participant=None):
        global url
        insert_json = {
            "mainorg":mainorg,
            "participant":str(participant)
          } 
        update_payload = {
            "operation":"sql",
            "sql":"update sync.participant set participant = '"+str(participant)+"' where mainorg = '"+mainorg+"'"
        }
        insert_payload = {
            "operation":"insert",
            "schema":"sync",
            "table":"participant",
            "records": [
              insert_json
            ]
        }
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=json.dumps(update_payload), headers=headers)
        try:
            if response.json()['error']!='':
                response = requests.request("POST", url, data=json.dumps(insert_payload), headers=headers)
        except:
            pass
        return Map(insert_json)

class Participants(models.Model):
    mainorg = models.CharField(max_length=100,primary_key=True)
    participant = models.CharField(max_length=10000)
    objects = ParticipantHarperDB()
    def save(self):
        global url
        payload ={
            "operation":"sql",
            "sql":"update sync.participant set participant = '"+str(self.participant)+"' where mainorg = '"+self.mainorg+"'"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return response.json

class TranscriptHarperDB(models.Manager):
    def get(self, meeting_id=None):
        global url
        payload ={
            "operation":"sql",
            "sql":"select * from sync.transcript where meeting_id = '"+str(meeting_id)+"'"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        res = response.json()[0]
        res = Map(res)
        try:
            res.timestamp = str(datetime.datetime.fromtimestamp(res.__createdtime__/1000.0))
        except:
            pass
        return Map(res)
    def all(self):
        global url
        payload ={
            "operation":"sql",
            "sql":"select * from sync.transcript"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return Map(response.json())

    def create(self, meeting_id=None, transcript=None, audio_file=None):
        global url
        insert_json = {
            "meeting_id":meeting_id,
            "transcript":transcript,
            "audio_file":audio_file
          } 
        update_payload = {
            "operation":"sql",
            "sql":"update sync.transcript set transcript = '"+transcript+"',audio_file='"+audio_file+"' where meeting_id = '"+str(meeting_id)+"'"
        }
        insert_payload = {
            "operation":"insert",
            "schema":"sync",
            "table":"transcript",
            "records": [
              insert_json
            ]
        }
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=json.dumps(update_payload), headers=headers)
        try:
            if response.json()['error']!='':
                response = requests.request("POST", url, data=json.dumps(insert_payload), headers=headers)
        except:
            pass
        return Map(insert_json)

class Transcript(models.Model):
    meeting_id = models.CharField(max_length=100,primary_key=True)
    transcript = models.CharField(max_length=100000)
    audio_file = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = TranscriptHarperDB()

class MeetingHarperDB(models.Manager):
    def get(self, meeting_id=None):
        global url
        payload ={
            "operation":"sql",
            "sql":"select * from sync.meeting where meeting_id = '"+str(meeting_id)+"'"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        res = response.json()[0]
        res = Map(res)
        return Meeting(meeting_id=res.meeting_id, email=res.email, status=res.status)
    
    def all(self):
        global url
        payload ={"operation":"sql",
            "sql":"select * from sync.meeting"
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return Map(response.json())

    def create(self, email=None, status=None):
        global url
        mid = str(random.randint(0,10000))+str(random.randint(0,4000))
        insert_json = {
            "email":email,
            "status":status,
            "timestamp":str(datetime.datetime.now()),
            "ended_at":"-",
            "meeting_id":mid
          } 
        update_payload = {
            "operation":"sql",
            "sql":"update sync.meeting set email = '"+email+"', status= '"+str(status)+"' where meeting_id = '"+str(mid)+"'"
        }
        insert_payload = {
            "operation":"insert",
            "schema":"sync",
            "table":"meeting",
            "records": [
              insert_json
            ]
        }
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=json.dumps(update_payload), headers=headers)
        try:
            if response.json()['error']!='':
                response = requests.request("POST", url, data=json.dumps(insert_payload), headers=headers)
        except:
            pass
        return Map(insert_json)

class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    status = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)
    objects = MeetingHarperDB()
    
    def save(self):
        global url
        sql = "update sync.meeting set email = '"+self.email+"', status= '"+str(self.status)+"' where meeting_id = '"+str(self.meeting_id)+"'"
        payload = {
            "operation":"sql",
            "sql":sql
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZGFtbmlrOmRhbW5paw=="
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return "Done"