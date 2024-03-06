# -*- coding: utf-8 -*-
"""Module withc custom package exceptions"""
from zope import schema


class InvalidEmailError(schema.ValidationError):
    __doc__ = "Please enter a valid e-mail address."
