definitions = {
    'token': {
        'type': 'object',
        'properties': {
            'value': {
                'type': 'string'
            },
            'expires_at': {
                'type': 'integer'
            }
        },
        'required': ['value', 'expires_at'],
        'additionalProperties': False
    },
    'session': {
        'type': 'object',
        'properties': {
            'handle': {
                'type': 'string'
            },
            'user_id': {
                'type': ['string', 'integer']
            },
            'jwt_payload': {
                'type': ['object', 'array', 'integer', 'string', 'boolean', 'null']
            }
        },
        'required': ['handle', 'user_id', 'jwt_payload'],
        'additionalProperties': False
    },
    'anti_csrf_not_null': {
        'type': 'string'
    },
    'anti_csrf_null': {
        'type': 'null'
    },
    'none': {
        'type': ['null']
    }
}

schema_create_new_session_ACT_enabled = {
    'type': 'object',
    'properties': {
        'access_token': definitions['token'],
        'id_refresh_token': definitions['token'],
        'refresh_token': definitions['token'],
        'anti_csrf_token': definitions['anti_csrf_not_null'],
        'session': definitions['session']
    },
    'required': ['access_token', 'id_refresh_token', 'refresh_token', 'anti_csrf_token', 'session'],
    'additionalProperties': False
}

schema_create_new_session_ACT_disabled = {
    'type': 'object',
    'properties': {
        'access_token': definitions['token'],
        'id_refresh_token': definitions['token'],
        'refresh_token': definitions['token'],
        'anti_csrf_token': definitions['anti_csrf_null'],
        'session': definitions['session']
    },
    'required': ['access_token', 'id_refresh_token', 'refresh_token', 'anti_csrf_token', 'session'],
    'additionalProperties': False
}

schema_refresh_session_ACT_enabled = {
    'type': 'object',
    'properties': {
        'new_access_token': definitions['token'],
        'new_id_refresh_token': definitions['token'],
        'new_refresh_token': definitions['token'],
        'new_anti_csrf_token': definitions['anti_csrf_not_null'],
        'session': definitions['session']
    },
    'required': ['new_access_token', 'new_id_refresh_token', 'new_refresh_token', 'new_anti_csrf_token', 'session'],
    'additionalProperties': False
}

schema_refresh_session_ACT_disabled = {
    'type': 'object',
    'properties': {
        'new_access_token': definitions['token'],
        'new_id_refresh_token': definitions['token'],
        'new_refresh_token': definitions['token'],
        'new_anti_csrf_token': definitions['anti_csrf_null'],
        'session': definitions['session']
    },
    'required': ['new_access_token', 'new_id_refresh_token', 'new_refresh_token', 'new_anti_csrf_token', 'session'],
    'additionalProperties': False
}

schema_new_session_get = {
    'type': 'object',
    'properties': {
        'session': definitions['session'],
        'new_access_token': definitions['none']
    },
    'required': ['session', 'new_access_token'],
    'additionalProperties': False
}

schema_updated_access_token_session_get = {
    'type': 'object',
    'properties': {
        'session': definitions['session'],
        'new_access_token': definitions['token']
    },
    'required': ['session', 'new_access_token'],
    'additionalProperties': False
}
