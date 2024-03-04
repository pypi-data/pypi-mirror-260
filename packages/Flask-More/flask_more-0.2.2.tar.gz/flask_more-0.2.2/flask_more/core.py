from typing import Any, Dict, List, Optional, Union, cast

from flask import Flask, Response, json, jsonify, render_template_string
from werkzeug.exceptions import HTTPException

from flask_more.openapi import gen_openapi_spec
from flask_more.schemas import OpenAPI
from flask_more.templates import redoc_template, swagger_template


class More:
    def __init__(
        self,
        app: Optional[Flask] = None,
        title: str = "API Docs",
        version: str = "1.0",
        description: str = "",
        docs_url: str = "/docs",
        redoc_url: str = "/redoc",
        openapi_url: str = "/openapi.json",
        openapi_tags: Optional[List[Dict[str, Any]]] = None,
        terms_of_service: Optional[str] = None,
        contact: Optional[Dict[str, Union[str, Any]]] = None,
        license_info: Optional[Dict[str, Union[str, Any]]] = None,
    ) -> None:
        self.title = title
        self.version = version
        self.description = description
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license_info = license_info

        self.openapi_schema: Optional[OpenAPI] = None

        if app is not None:
            self.app = app
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        self.app.register_error_handler(HTTPException, self.handle_exception)

        if self.docs_url:
            app.add_url_rule(self.docs_url, view_func=self.docs)
        if self.redoc_url:
            app.add_url_rule(self.redoc_url, view_func=self.redoc)
        if self.openapi_url:
            app.add_url_rule(self.openapi_url, view_func=self.openapi)

    def docs(self) -> str:
        context = {"title": self.title}
        return render_template_string(swagger_template, **context)

    def redoc(self) -> str:
        context = {"title": self.title}
        return render_template_string(redoc_template, **context)

    def openapi(self) -> Response:
        self.openapi_schema = gen_openapi_spec(
            routes=self.app.url_map,
            view_functions=self.app.view_functions,
            title=self.title,
            version=self.version,
            description=self.description,
            terms_of_service=self.terms_of_service,
            contact=self.contact,
            license_info=self.license_info,
            openapi_tags=self.openapi_tags,
        )
        schema = self.openapi_schema.dict(by_alias=True, exclude_defaults=True)
        return jsonify(schema)

    def handle_exception(self, e: HTTPException) -> Response:
        rsp = cast(Response, e.get_response())
        rsp.data = json.dumps({"detail": e.description})
        rsp.content_type = "application/json"
        return rsp
