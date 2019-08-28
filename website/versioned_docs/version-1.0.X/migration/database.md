---
id: version-1.0.X-database
title: Add SuperTokens to an exisiting Database
sidebar_label: Database
original_id: database
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