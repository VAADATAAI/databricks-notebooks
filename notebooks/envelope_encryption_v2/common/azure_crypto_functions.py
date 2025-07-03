# Databricks notebook source
"""Utility helpers for envelope encryption using Azure Key Vault."""
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, KeyWrapAlgorithm


def create_keyvault_key(vault_url: str, key_name: str, credential: DefaultAzureCredential) -> None:
    """Create or retrieve a Key Vault key."""
    key_client = KeyClient(vault_url=vault_url, credential=credential)
    try:
        key_client.get_key(key_name)
    except Exception:
        key_client.create_key(key_name, key_type="RSA")


def wrap_data_key(vault_url: str, key_name: str, data_key: bytes, credential: DefaultAzureCredential) -> bytes:
    """Wrap a locally generated data key with the Key Vault key."""
    crypto = CryptographyClient(key_client=KeyClient(vault_url, credential).get_key(key_name), credential=credential)
    wrap_result = crypto.wrap_key(KeyWrapAlgorithm.rsa_oaep, data_key)
    return wrap_result.encrypted_key


def unwrap_data_key(vault_url: str, key_name: str, encrypted_key: bytes, credential: DefaultAzureCredential) -> bytes:
    """Unwrap a data key previously wrapped by wrap_data_key."""
    crypto = CryptographyClient(key_client=KeyClient(vault_url, credential).get_key(key_name), credential=credential)
    unwrap_result = crypto.unwrap_key(KeyWrapAlgorithm.rsa_oaep, encrypted_key)
    return unwrap_result.key
