from django.db import models


class SigningKey(models.Model):

    key_name = models.CharField(
        max_length=128, primary_key=True, editable=False, unique=True, null=False)
    key_value = models.CharField(max_length=255, null=False, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "signing_key"


class RefreshToken(models.Model):

    session_handle = models.CharField(
        max_length=255, primary_key=True, editable=False, unique=True, null=False)
    user_id = models.CharField(max_length=128, null=False, editable=True)
    refresh_token_hash_2 = models.CharField(
        max_length=128, null=False, editable=True)
    session_info = models.TextField(editable=True)
    expires_at = models.DateTimeField()
    jwt_payload = models.TextField(null=False)

    class Meta:
        db_table = "refresh_token"
