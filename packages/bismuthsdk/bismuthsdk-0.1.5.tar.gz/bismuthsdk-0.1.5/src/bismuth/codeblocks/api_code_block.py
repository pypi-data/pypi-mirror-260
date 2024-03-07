from flask import Flask, request
from flask_restx import Api, Resource
from .auth_code_block import AuthCodeBlock
from .base_code_block import BaseCodeBlock
from .function_code_block import FunctionCodeBlock


class APICodeBlock(BaseCodeBlock):
    def __init__(
        self,
        title="API",
        version="1.0",
        description="A simple API",
        app_config={},
        auth_code_block: AuthCodeBlock = None,
        *args,
        **kwargs
    ):

        super().__init__(*args, **kwargs)
        self.app = Flask(__name__)
        self.app.config.update(app_config)
        self.api = Api(self.app, version=version, title=title, description=description)
        self.auth_code_block = auth_code_block

    def _auth_handler(
        self,
        method: str,
        handlers: dict[str, FunctionCodeBlock],
        require_auth: list[str],
        **kwargs
    ):
        if (
            method.lower() in map(lambda x: x.lower(), require_auth)
            and self.auth_code_block is not None
        ):
            return self.auth_code_block.token_required(handlers[method].exec)(**kwargs)
        else:
            return handlers[method].exec(**kwargs)

    def add_route(
        self,
        route: str,
        methods: str | list[str],
        handlers: dict[str, FunctionCodeBlock],
        require_auth: list[str] = ["POST", "DELETE", "PUT"],
    ):
        methods = methods if isinstance(methods, list) else [methods]
        auth_handler = self._auth_handler

        class DynamicResource(Resource):
            def get(self):
                kwargs = request.args.to_dict()
                if "GET" in methods:
                    return auth_handler("GET", handlers, require_auth, **kwargs)
                else:
                    self.api.abort(404)

            def post(self):
                kwargs = request.json or {}
                if "POST" in methods:
                    return auth_handler("POST", handlers, require_auth, **kwargs)
                else:
                    self.api.abort(404)

            def put(self):
                kwargs = request.json or {}
                if "PUT" in methods:
                    return auth_handler("PUT", handlers, require_auth, **kwargs)
                else:
                    self.api.abort(404)

            def delete(self):
                kwargs = request.args.to_dict()

                if "DELETE" in methods:
                    return auth_handler("DELETE", handlers, require_auth, **kwargs)
                else:
                    self.api.abort(404)

        self.api.add_resource(DynamicResource, route)

    def run(self, host="0.0.0.0", port=5000, debug=False):
        self.app.run(host=host, port=port, debug=debug)
