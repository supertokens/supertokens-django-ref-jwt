![SuperTokens banner](https://raw.githubusercontent.com/supertokens/supertokens-logo/master/images/Artboard%20%E2%80%93%2027%402x.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/supertokens/supertokens-django-ref-jwt/blob/master/LICENSE)
<a href="https://supertokens.io/discord">
        <img src="https://img.shields.io/discord/603466164219281420.svg?logo=discord"
            alt="chat on Discord"></a>

**Master**
[![CircleCI](https://circleci.com/gh/supertokens/supertokens-django-ref-jwt.svg?style=svg)](https://circleci.com/gh/supertokens/supertokens-django-ref-jwt)
**Dev**
[![CircleCI](https://circleci.com/gh/supertokens/supertokens-django-ref-jwt/tree/dev.svg?style=svg)](https://circleci.com/gh/supertokens/supertokens-django-ref-jwt/tree/dev)

This library implements user session management for websites that run on **Django**. This is meant to be used with your backend code. If you do not use Django, please checkout [our website](https://supertokens.io) to find the right library for you..

#### The protocol SuperTokens uses is described in detail in [this article](https://supertokens.io/blog/the-best-way-to-securely-manage-user-sessions)

The library has the following features:
- It uses short-lived access tokens (JWT) and long-lived refresh tokens (Opaque).
- **Protects against**: XSS, Brute force, Session fixation, JWT signing key compromise, Data theft from database, CSRF and session hijacking.
- **Token theft detection**: SuperTokens is able to detect token theft in a robust manner. Please see the article mentioned above for details on how this works.
- **Complete auth token management** - It only stores the hashed version of refresh tokens in the database, so even if someone (an attacker or an employee) gets access to the table containing them, they would not be able to hijack any session.
- **Automatic JWT signing key generation** (if you don't provide one), management and **rotation** - Periodic changing of this key enables maximum security as you don't have to worry much in the event that this key is compromised. Also note that doing this change will not log any user out :grinning:
- **Complete cookie management** - Takes care of making them secure and HttpOnly. Also removes, adds and edits them whenever needed. You do not have to worry about cookies and its security anymore!
- **Efficient** in terms of **space complexity** - Needs to store just one row in the table per logged in user per device.
- **Efficient** in terms of **time complexity** - Minimises the number of DB lookups (most requests do not need a database call to authenticate at all if blacklisting is false - which is the default)
- Built-in support for **handling multiple devices per user**.
- **Built-in synchronisation** in case you are running multiple django processes.
- **Easy to use** (see [auth-demo](https://github.com/supertokens/auth-demo)), with well documented, modularised code and helpful error messages!
- Using this library, you can keep a user logged in for however long you want - without worrying about any security consequences. 

## Index
- [Documentation](https://github.com/supertokens/supertokens-django-ref-jwt#documentation)
- [Making changes](https://github.com/supertokens/supertokens-django-ref-jwt#making-changes)
- [Tests](https://github.com/supertokens/supertokens-django-ref-jwt#tests)
- [Support, questions and bugs](https://github.com/supertokens/supertokens-django-ref-jwt#support-questions-and-bugs)
- [Authors](https://github.com/supertokens/supertokens-django-ref-jwt#authors)

## Documentation: 
Coming Soon.

## Making changes
Please see our [Contributing](https://github.com/supertokens/supertokens-django-ref-jwt/blob/master/CONTRIBUTING.md) guide

## Tests
```
make dev-install
make test
```
See our [Contributing](https://github.com/supertokens/supertokens-django-ref-jwt/blob/master/CONTRIBUTING.md) guide for more information.

## Support, questions and bugs
We are most accessible via team@supertokens.io, via the GitHub issues feature and our [Discord server](https://supertokens.io/discord). 

Click [here](https://github.com/supertokens/supertokens-node-mysql-ref-jwt#support-questions-and-bugs) to see more information.

## Authors
Created with :heart: by the folks at SuperTokens. We are a startup passionate about security and solving software challenges in a way that's helpful for everyone! Please feel free to give us feedback at team@supertokens.io, until our website is ready :grinning:
