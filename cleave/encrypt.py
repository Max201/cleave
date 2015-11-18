#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
import binascii
from __builtin__ import unicode


class Encrypt(unicode):
    """
    MD5 Encryption tool
    """
    def _md5(self):
        md5 = hashlib.md5()
        md5.update(self)
        return Encrypt(md5.hexdigest())

    @property
    def md5(self):
        return self._md5()

    """
    CRC32 Encryption tool
    """
    def _crc32(self):
        return Encrypt(binascii.crc32(self))

    @property
    def crc32(self):
        return self._crc32()

    """
    Base64/Base16 Encryption / Decryption tool
    """
    def _base16(self):
        return Encrypt(base64.b16encode(self))

    def _unbase16(self):
        return Encrypt(base64.b16decode(self))

    @property
    def base16(self):
        return self._base16()

    @property
    def unbase16(self):
        return self._unbase16()

    def _base64(self):
        return Encrypt(base64.b64encode(self))

    def _unbase64(self):
        return Encrypt(base64.b64decode(self))

    @property
    def base64(self):
        return self._base64()

    @property
    def unbase64(self):
        return self._unbase64()

    """
    SHA Encryption tool
    """
    def _sha1(self):
        return Encrypt(hashlib.sha1(self).hexdigest())

    @property
    def sha1(self):
        return self._sha1()

    def _sha224(self):
        return Encrypt(hashlib.sha224(self).hexdigest())

    @property
    def sha224(self):
        return self._sha224()

    def _sha256(self):
        return Encrypt(hashlib.sha256(self).hexdigest())

    @property
    def sha256(self):
        return self._sha256()

    def _sha384(self):
        return Encrypt(hashlib.sha384(self).hexdigest())

    @property
    def sha384(self):
        return self._sha384()

    def _sha512(self):
        return Encrypt(hashlib.sha512(self).hexdigest())

    @property
    def sha512(self):
        return self._sha512()