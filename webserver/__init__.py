__all__ = ["create_app"]


def __getattr__(name):
    # Catalogue builds also read the server configuration without starting Flask.
    if name == "create_app":
        from webserver.app import create_app
        return create_app
    raise AttributeError(name)
