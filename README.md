# pooprapi

Poopr is a prototype project to create an open database and interface for locations of public restrooms. It consists of three components:
- App (iOS at the moment)
- API (Python)
- Database (MySQL)

API built on Python 3.5 and Flask.

Go-between for Poopr iOS app and MySQL database. The goal is to host it on a DigitalOcean droplet, together with the actual database.

Implemented so far:
- DB access via SQL procedures (no SQL in API code)
- All read-only queries (I think)

To-do:
- Dispute facility
- Create facility
- Rate facility
- Figure out properly working deployment (Apache2 vs Nginx)
