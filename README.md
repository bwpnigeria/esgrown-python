# ABU Alumni Connect Backend

ABU Alumni Connect is a platform that connects ABU alumni with each other and with the university. This repository contains the backend code for the platform.


## Run Locally (No Docker)

```SQL
/*
We assume you a have local postgresql server running on your machine
Create the database in postgres 
*/

CREATE DATABASE abu_alumni_connect_db;
CREATE DATABASE abu_alumni_connect_test_db;
```

```bash
# clone the repo
# hello world
git clone https://github.com/alhytham-tech/abu-alumni-connect-backend.git

cd abu-alumni-connect-backend

# create a virtual env
python -m venv 

# activate the virtual env
source abu_alumni_connect_env/bin/activate

# install all dependencies
pip install -r requirements.txt

# decrypt .env file
git secret reveal

# create migrations
alembic upgrade head

# setup initial data
python initialize.py

# run the app
uvicorn app.main:app --reload

# run tests
pytest

```

## Run Locally (With Docker)

```bash
# clone the repo
git clone https://github.com/alhytham-tech/abu-alumni-connect-backend.git

cd abu-alumni-connect-backend

# decrypt .env file
# if you will like different values for the initial
# super user, you can change them in the .env file
git secret reveal

# start the docker services
docker-compose up

```

## Chat Documentation

```json
// websocket url
"wss://alumni-backend.abu.edu.ng/chat"

// websocket url with token
"wss://alumni-backend.abu.edu.ng/chat?token={jwt_token}"

// NB: the jwt_token should be specified without the `Bearer` part
// just *eyJ.....* to the end

// the contract between the frontend and backend is defined by packets which are 
// just schemas at their core


/*
 When you send a message it will be in the following format
*/

{
  "type": "message-send",
  "payload": {
    "message": "Hello, how are you?",
    "room_id": "room123"
  }
}

/*
 You will receive messages in the following format
*/

{
  "type": "message-receive",
  "payload": {
    "room_id": "room123",
    "sender_id": "user456",
    "message": "I'm good, thanks!",
    "timestamp": "2024-08-21T14:30:00Z"
  }
}

/*
 When a user comes online you will send the following join packet to the server
*/

{
  "type": "chat-join",
  "payload": {
    "notice": "join"
  }
}


/*
 The following will be broadcasted downstream by the server when a user joins
*/

{
  "type": "chat-join-notify",
  "payload": {
    "participant_id": "user789"
  }
}


/*
 When a user leaves chat (i.e websocket connection is terminated for 
 any reason e.g timeouts, user disconnecting, server closing) the
 following even will be broadcasted downstreams to all members of the room
*/

{
  "type": "chat-leave",
  "payload": {
    "participant_id": "user789"
  }
}


/*
 When a user is typing you send this event upstream to the server
 sending is_typing: false means the user stopped typing
*/

{
  "type": "typing",
  "payload": {
    "is_typing": true,
    "room_id": "room123"
  }
}


/*
 The server will then send the following event downstream to all members
 of the room to notify that someone is typing 
*/

{
  "type": "typing-notify",
  "payload": {
    "room_id": "room123",
    "participant_id": "user456",
    "is_typing": true
  }
}


/*
 When you want to retrieve message history you can send the following
 event upstream to the server
*/

{
  "type": "list-message-request",
  "payload": {
    "room_id": "room123",
    "limit": 10,
    "skip": 0,
    "order": "desc"
  }
}

/*
 The server will then send the following event downstream as response
 to the request
*/

{
  "type": "list-message-response",
  "payload": {
    "room_id": "room123",
    "messages": [
      {
        "room_id": "room123",
        "sender_id": "user456",
        "message": "Hello!",
        "timestamp": "2024-08-21T14:30:00Z"
      },
      {
        "room_id": "room123",
        "sender_id": "user789",
        "message": "Hi there!",
        "timestamp": "2024-08-21T14:31:00Z"
      }
    ],
    "total_count": 2
  }
}
```