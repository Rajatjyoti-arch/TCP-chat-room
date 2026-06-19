# Python TCP Chat Room

A multi-threaded TCP chat room application written in Python. This project features a 3-tier user hierarchy with role-based permissions.

## Architecture

The chat room runs on a centralized server with three different types of clients that can connect to it. The server handles authentication, message broadcasting, and enforcing permissions.

### 1. The Server (`server.py`)
- Acts as the central hub for the chat room.
- Manages incoming connections on port `55555`.
- Performs a "role handshake" to identify if a connecting user is an admin, elder, or member.
- Verifies passwords for elevated roles.
- Tracks kicked users and bans IP addresses to prevent malicious users from rejoining.

### 2. The Clients
There are three different client scripts, each representing a different permission level in the chat room:

* **`member.py` (Standard User)**
  * The default client for regular users.
  * Connects directly by providing an alias.
  * Can send and receive messages but has no administrative powers.

* **`elder.py` (Moderator)**
  * The moderator client.
  * Connects by providing an alias and the Elder password (default: `elderpass`).
  * Has the authority to remove disruptive users using the `/kick <alias>` command.

* **`admin.py` (Administrator)**
  * The highest privilege client.
  * Connects by providing an alias and the Admin password (default: `adminpass`).
  * Has the authority to `/kick <alias>` and `/ban <alias>` users. Banned users have their IP address blacklisted from the server.

## Commands

Commands can be typed directly into the chat interface by users with the appropriate permissions:

- `/kick <alias>`: Forcibly disconnects the target user from the server. (Available to: **Admin**, **Elder**)
- `/ban <alias>`: Forcibly disconnects the target user and blocks their IP address from reconnecting. (Available to: **Admin**)

## Getting Started

1. **Start the Server:**
   Run the server script first to start listening for connections.
   ```bash
   python3 server.py
   ```
   *(Note: You may need to edit `server.py` and the client scripts to replace `[IP_Address]` with `127.0.0.1` for local testing, or your actual local IP address for LAN testing).*

2. **Connect a Client:**
   Open a new terminal window and run one of the client scripts:
   ```bash
   python3 member.py
   # OR
   python3 elder.py
   # OR
   python3 admin.py
   ```

3. **Follow the Prompts:**
   Enter your alias and password (if running a privileged client) to join the chat!
