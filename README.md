#An automated messenging service

## 1. Description

This is a Dockerized service for automating sending wtsapp messages using Python Selenium

1. check whether a phone number has a Whatsapp account associated with it
2. send whatsapp messages

After receiving an API call with a specified phone number, message and return URL, it will perform the action and post the result onto the return URL.


### 1.1. Set up
#### 1.1.1 Docker compose
Step 1: Pull image from Dockerhub

Step 2:	Build service with docker-compose.yml with
```
docker-compose build
```
Step 3: Run server with
```
docker-compose up
```
#### 1.2.2	Configuration
The config.py file holds all the configuration variables

## 2. Infrastructure

### 2.1	Device
This API relies on a mobile phone to work, requirements are as follows

1. Has Whatsapp installed
2. The phone has to be turned on and connected to the internet at all times
3. The first time this service is called/when docker is rebuilt, it is necessary to log into Whatsapp by scanning QR code with the phone. Detailed log in procedure will be laid out in part 4.

## 3. API usage

##Authentication by token is required. Put token in HTTP request header in the following format##

```
headers = {
    "Authorization" => "Token token=<String Token>"
  }
```

### 3.1	API usage

#### 3.1.1	Whatsapp check

##### Call Format: 
Call has to be HTTP POST method
```
<path: Server IP>/ws/check/<string: Phone number>/<path: Return URL>
```

##### Response:
If the task is received and queued successfully, It would respond to the call immediately with a task ID, which needs to be saved to reference check result later

```
{"data":{"task_id":"75b99f5f-e6bb-4eec-90f7-ebf2e24dccf2","task_name":"whatsapp check"},"status":"success"}
```

If the call has invalid format, the server will throw a 400 bad request error

##### Check results:
When the check is done, the server will post the result to the provided return URL as data of a HTTP POST request, in json format
```
{"task_id": task_id, "result": result}
```

Use the task ID mentioned to match result to specific phone number

#### 3.1.2	Whatsapp messaging

##### Call Format: 
Call has to be HTTP POST method
```
<path: Server IP>/ws/message/<string: Phone number>/<string: Message>/<path: Return URL>
```

##### Response:
If the task is received and queued successfully, it would respond to the call immediately with a task ID, which needs to be saved to reference check result later

```
{"data":{"task_id":"75b99f5f-e6bb-4eec-90f7-ebf2e24dccf2","task_name":"whatsapp message"},"status":"success"}
```

If the call has invalid format, the server will throw a 400 bad request error

##### Message status:
After the task is performed, it will post the result to the provided return URL as data of a HTTP POST request, in json format
```
{"task_id": task_id, "result": result}
```

If the result is 'True', that means the message has been sent sucessfully. If the result is 'False', that means either the recipient does not have whatsapp, or the number has not been added to Google Contact. Further action will be necessary to handle such case.

Use the task ID mentioned to match result to specific phone number

### 3.2 Whatsapp not logged in/ disconnected/ banned
#### Disconnected
If for whatever reason Whatsapp web is disconnected from the associated phone, action will not be performed. Instead, a QR code will be sent through Slack, and the log in procedure as described in part 4.1 will be initiated. If that is the case, make sure the action called on the failed phone number is repeated as there is no built-in mechanism to take up failed tasks.

## 4. Service set up

### 4.1 Log in to Whatsapp account
It is necessary to log into whatsapp the first time the server is up/ when the docker image has been rebuilt
To log in, call the following API:
```
HTTP POST <path: Server IP>/ws/login/<path:ret_url>
```

After the call, monitor the whatsapp_services channel on slack, a log in QR code will be sent to the channel. Scan the QR code with Whatsapp mobile app on the phone that you want to associate with it.

If the whatsapp mobile app shows an error after scanning the code, the code has expired. Make this API call once more and try again.

If log in is successful, the server will post “Please scan qr code” to the provided return URL as data of a HTTP POST request, in json format

If it is already connected to a Whatsapp account, the server will post “Whatsapp already logged in” to the provided URL as data of a HTTP POST request, in json format

### 5.2	Log out of Whatsapp account
To log out, call the following API:
```
HTTP POST <path: Server IP>/ws/logout/<path:ret_url>
```

If log out is successful, the server will post “Log out successful” to the provided return URL as data of a HTTP POST request, in json format

If it is not currently logged into any Whatsapp account, the server will post “Currently not logged into any account” to the provided URL as data of a HTTP POST request, in json format
