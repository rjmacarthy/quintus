from api.routes.chat import ChatRoutes


class Routes:
    def register(app):
        ChatRoutes.register(app)
