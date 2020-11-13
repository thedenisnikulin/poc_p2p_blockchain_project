<h1 align="center">PoC P2P Blockchain Network</h1>

<p align="center">
  <img align="center" src="https://user-images.githubusercontent.com/46903210/87221895-41768680-c378-11ea-9dbe-a54c2a633f3b.gif"></img>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>


I like the idea of bitcoin and blockchain. This is a basic proof-of-concept blockchain that I've built. It is based on a peer-to-peer decentralized TCP network.


# Table of contents
1. [Description](#description)
2. [Features](#features)
3. [Technologies used](#technologies-used)
4. [How to use](#how-to-use)

---

# Description
***Class structure***
* Blockchain
* Block
* Transaction
* Server
* Client
* SuperPeer
* Peer


***The P2P network is based on `Client` and `Server` classes.***  
- Server:
1. waits for client to connect, 
2. accepts connection, 
3. adds client to list of clients (= list of peers), 
4. broadcasts the list to all the clients (lets clients know about new client),
5. listens to client messages  
- Client:
1. connects to the server
2. lets user interact with the program logic (i.e. blockchain and networking)
3. listens to server messages

***The core logic lies in two concepts: Peer and SuperPeer***  

**Peer** - a classic peer, it's just a `client`  
**SuperPeer** - a super peer, it's both `client` and `server` 

***How it all works together***  
1. first, program becomes a Peer
2. it tries to connect to the SuperPeer by public address, which is stored in `server_tracker.txt`
3. if connection is established successfully, it remains Peer
4. if it can't connect to the SuperPeer for some reason (most likely there's no SuperPeer to connect to), it becomes a SuperPeer itself and stores its address in `server_tracker.txt` for other peers to connect  

***If something is not clear for you, check out the source code. I tried to write as much comments as possible to make it easier to understand.***

---

# Features
* **Self-repairing network.** When SuperPeer disables/disconnects, one of peers becomes SuperPeer, which makes it impossible to stop the network.
* **Persistent state.** Blockchain saves its state across all peers even when SuperPeer disconnects.
* **Data broadcasting.** All the data is broadcasted between peers.
* **CLI interface.** A convenient interface built with `PyInquirer`.
* **Blockchain implementation.** This blockchain implementation is similar to original Bitcoin's blockchain, but I simplified some stuff.

---

# Technologies used
* Data serialization - `pickle`
* CLI interface - `PyInquirer`
* Parallelism - `threading` 
* Networking - `socket`
* Hashes - `hashlib`

---

# How to use

* Download project
```
git clone https://github.com/thedenisnikulin/poc_p2p_blockchain_project.git
```
* Install dependencies
```
pip install -r ./requirements.txt
```
* Run
```
python src/main.py
```
---
