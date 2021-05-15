# coding: utf-8
"""Here we place the configuration of the swagger.

this is used to make the interface used to display the services created by this
API.
"""
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SWAGGER = {
    "swagger_version": "2.0",
    "title": "Hackathon",
    'uiversion': 2,
    "info": {
        "title": "API",
        "description": "Alguns dos serviços disponíveis",
        "version": "1.0.1"
    },
    "schemes": [
        "http",
        "https"
    ],
    "specs": [
        {
            "endpoint": "v1_spec",
            "route": "/v1/spec",
        }
    ]
}
