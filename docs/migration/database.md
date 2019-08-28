---
id: database
title: Add SuperTokens to an exisiting Database
sidebar_label: Database
---

SuperTokens will create two tables. One to store signing keys and other to store sessions. Please execute the following commands:
- Run make migrations
```bash
python manage.py makemigrations supertokens_jwt_ref
```
- Run migrate
```bash
python manage.py migrate supertokens_jwt_ref
```