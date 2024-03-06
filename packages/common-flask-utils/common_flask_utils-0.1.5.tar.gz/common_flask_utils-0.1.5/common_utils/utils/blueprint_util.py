import pkgutil
import re
import traceback
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, Dict, List, Tuple

from flask import Blueprint, Flask
from flask.sansio.scaffold import T_route


class Outlining:
    get: Callable[[str, Any], Callable[[T_route], T_route]]
    post: Callable[[str, Any], Callable[[T_route], T_route]]
    put: Callable[[str, Any], Callable[[T_route], T_route]]
    delete: Callable[[str, Any], Callable[[T_route], T_route]]
    patch: Callable[[str, Any], Callable[[T_route], T_route]]
    options: Callable[[str, Any], Callable[[T_route], T_route]]
    head: Callable[[str, Any], Callable[[T_route], T_route]]

    def __init__(
        self,
        name: str,
        *args: List[Any],
        url_prefix: str = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        """
        Initialize a BlueprintUtil object.

        Args:
            name (str): The name of the blueprint.
            *args (List[Any]): Variable length argument list.
            url_prefix (str, optional): The URL prefix for the blueprint. Defaults to None.
            **kwargs (Dict[str, Any]): Keyword arguments.

        Returns:
            None
        """
        self.args: List[Any] = args
        self.kwargs: Dict[str, Any] = kwargs
        self.url_prefix: str = url_prefix
        self.name: str = name
        self.mound: List[Tuple[T_route, str, Any]] = []

    def route(self, rule: str, **options: Any) -> Callable[[T_route], T_route]:
        """
        Decorator for adding a route to the blueprint.

        Args:
            rule (str): The URL rule string for the route.
            **options (Any): Additional options for the route.

        Returns:
            Callable[[T_route], T_route]: The decorated function.
        """

        def decorator(f: T_route) -> T_route:
            """
            Decorator function used to add routes to the blueprint.

            Args:
                f (T_route): The route function to be added.

            Returns:
                T_route: The decorated route function.
            """
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix: str = None) -> None:
        """
        Register the blueprint's routes with the given Flask blueprint.

        Args:
            bp (flask.Blueprint): The Flask blueprint to register the routes with.
            url_prefix (str, optional): The URL prefix for the routes. If not provided,
                the blueprint's name or `url_prefix` attribute will be used.

        Returns:
            None
        """
        if url_prefix is None:
            if self.url_prefix is None:
                url_prefix = "/" + self.name
            else:
                url_prefix = "/" + self.url_prefix
        url_prefix = re.sub(r"/+", "/", url_prefix)

        for f, rule, options in self.mound:
            endpoint = self.name + "+" + options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)

    def __getattribute__(self, __name: str) -> Any:

        if __name.lower() in [
            "get",
            "post",
            "put",
            "delete",
            "patch",
            "options",
            "head",
        ]:
            return lambda *args, **kwargs: self.route(methods=[__name], *args, **kwargs)

        return super().__getattribute__(__name)


def register_outlining_from_sub_package(bp: Blueprint, blueprint_dir: str) -> None:
    """
    Recursively registers outlining from sub-packages within the given blueprint directory.

    Args:
        bp (Blueprint): The Flask blueprint to register outlining with.
        blueprint_dir (str): The directory of the sub-package to register outlining from.

    Returns:
        None
    """
    package: ModuleType = import_module(blueprint_dir)
    if not hasattr(package, "__path__"):
        register_outlining(bp, package)
    else:
        for _, name, _ in pkgutil.iter_modules(package.__path__):
            full_name: str = f"{blueprint_dir}.{name}"
            register_outlining_from_sub_package(bp, full_name)


def register_outlining(bp: Blueprint, module: ModuleType) -> None:
    """
    Registers outlining objects from a module to a Flask blueprint.

    Args:
        bp (Blueprint): The Flask blueprint to register the outlining objects to.
        module (ModuleType): The module containing the outlining objects.

    Returns:
        None
    """
    try:
        k: str
        v: Outlining
        for k, v in module.__dict__.items():
            if k.startswith("_"):
                continue
            if not isinstance(v, Outlining):
                continue
            v.register(bp)
    except:
        traceback.print_exc()


def blueprint_registration(
    app: Flask, blueprint_dir: str = "app.module", url_prefix: str = None
) -> None:
    """
    Registers blueprints in the specified directory with the Flask app.

    Args:
        app (Flask): The Flask app instance.
        blueprint_dir (str, optional): The directory where the blueprints are located. Defaults to "app.module".
        url_prefix (str, optional): The URL prefix for the registered blueprints. Defaults to None.
    """
    package: ModuleType = import_module(blueprint_dir)
    if hasattr(package, "__path__"):
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            bp: Blueprint = Blueprint(name, __name__, url_prefix=url_prefix)
            if is_pkg:
                sub_package: str = f"{blueprint_dir}.{name}"
                register_outlining_from_sub_package(bp, sub_package)
            else:
                full_name: str = f"{blueprint_dir}.{name}"
                module: ModuleType = import_module(full_name)
                register_outlining(bp, module)
            app.register_blueprint(bp)
