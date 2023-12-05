import pkgutil, importlib, re, sys
from traceback import print_exc
from abc import abstractmethod, ABCMeta
from pathlib import Path
from botpy import logging
from typing import Iterable, Optional, Set, Dict, List

logger = logging.get_logger()

class Colors:
    # 清除格式
    escape          = "\033[0m"

    # 前景色
    black           = "\033[0;30m"
    dark_gray       = "\033[1;30m"
    black_underline = "\033[4;30m"
    black_blink     = "\033[5;30m"

    blue                = "\033[0;34m"
    light_blue          = "\033[1;34m"
    blue_underline      = "\033[4;34m"
    blue_blink          = "\033[5;34m"

    green               = "\033[0;32m"
    light_green         = "\033[1;32m"
    green_underline     = "\033[4;32m"
    green_blink         = "\033[5;32m"

    cyan                = "\033[0;36m"
    light_cyan          = "\033[1;36m"
    cyan_underline      = "\033[4;36m"
    cyan_blink          = "\033[5;36m"

    red                 = "\033[0;31m"
    light_red           = "\033[1;31m"
    red_underline       = "\033[4;31m"
    red_blink           = "\033[5;31m"

    purple              = "\033[0;35m"
    light_purple        = "\033[1;35m"
    purple_underline    = "\033[4;35m"
    purple_blink        = "\033[5;35m"

    brown               = "\033[0;33m"
    yellow              = "\033[1;33m"
    yellow_underline    = "\033[4;33m"
    yellow_blink        = "\033[5;33m"

    light_gray          = "\033[0;37m"
    white               = "\033[1;37m"
    gray_underline      = "\033[4;37m"
    gray_blink          = "\033[5;37m"


# TODO: 事件响应器基类


def path_to_module_name(launcher_path: Path, path: Path) -> str:
    rel_path = path.resolve().relative_to(launcher_path)
    if rel_path.stem == "__init__":
        return ".".join(rel_path.parts[:-1])
    else:
        return ".".join(rel_path.parts[:-1] + (rel_path.stem,))


def _module_name_to_plugin_name(module_name: str) -> str:
    return module_name.rsplit(".", 1)[-1]


class PluginManager:
    """
    Plugin Manager for the flask application.
    written according to module nonebot.plugin.manager.PluginManager

    Params:
        app: the flask application
        manager: command manager of the application
        launcher_path: resolved path to the folder of launcher.py
        plugins: set of the plugins
        search_path: set of the path that contains plugins.
    """

    def __init__(
            self,
            launcher_path: Path,
            plugins: Optional[Iterable[str]] = None,
            search_path: Optional[Iterable[str]] = None
    ) -> None:
        self.launcher_path = launcher_path
        self.plugins: Set[str] = set(plugins or [])
        self.search_path: Set[str] = set(search_path or [])

        self._third_party_plugin_names: Dict[str, str] = {}
        self._searched_plugin_names: Dict[str, Path] = {}
        self.prepare_plugins()

    def __repr__(self) -> str:
        return f"PluginManager(plugins={self.plugins}, search_path={self.search_path})"

    @property
    def third_party_plugins(self) -> Set[str]:
        return set(self._third_party_plugin_names.keys())

    @property
    def searched_plugins(self) -> Set[str]:
        return set(self._searched_plugin_names.keys())

    @property
    def available_plugins(self) -> Set[str]:
        return self.third_party_plugins | self.searched_plugins

    def prepare_plugins(self) -> Set[str]:
        """
        search all the possible plugins and store them.
        """
        searched_plugins: Dict[str, Path] = {}
        third_party_plugins: Dict[str, str] = {}

        for plugin in self.plugins:
            name = _module_name_to_plugin_name(plugin)
            if name in third_party_plugins:
                raise RuntimeError(
                    f"Plugin already exists: {name}! Check your plugin name."
                )
            third_party_plugins[name] = plugin

        self._third_party_plugin_names = third_party_plugins

        for module_info in pkgutil.iter_modules(self.search_path):
            if module_info.name.startswith('_'):
                logger.opt(colors=True).info(
                    f'{Colors.light_red}Ignored{Colors.escape} module "{Colors.light_blue}{module_info.name}{Colors.escape}"'
                )
                continue
            if (
                    module_info.name in searched_plugins
                    or module_info.name in third_party_plugins
            ):
                raise RuntimeError(
                    f'Plugin already exists: "{Colors.light_blue}{module_info.name}{Colors.escape}"! Check you plugin name.'
                )

            if not (
                    module_spec := module_info.module_finder.find_spec(
                        module_info.name, None
                    )
            ):
                continue
            if not (module_path := module_spec.origin):
                continue
            searched_plugins[module_info.name] = Path(module_path).resolve()

        self._searched_plugin_names = searched_plugins

        return self.available_plugins

    def load_plugin(self, name: str) -> str:
        """
        load the plugin decided by name.

        Param:
            name: name of the plugin
        """
        try:
            if name in self.plugins:
                module = importlib.import_module(name)
            elif name in self._third_party_plugin_names:
                module = importlib.import_module(self._third_party_plugin_names[name])
            elif name in self._searched_plugin_names:
                module = importlib.import_module(
                    path_to_module_name(self.launcher_path, self._searched_plugin_names[name])
                )
            else:
                raise RuntimeError(f"Plugin not found: {name}! Check your plugin name.")

            logger.success(
                f'{Colors.green}Succeeded{Colors.escape} to import "{Colors.light_blue}{name}{Colors.escape}"'
            )
            if (handler := getattr(module, "__handler__", None)) is None:
                logger.error(f'Module "{Colors.light_blue}{name}{Colors.escape} is not loaded as a plugin!"')
                logger.error(f'Make sure the __handler__ variable is correct')
            # TODO: 在这里注册事件响应器handler
                
        except Exception as e:
            logger.error(
                f'{Colors.red}Failed to import{Colors.escape} "{Colors.light_blue}{name}{Colors.escape}"!'
            )
            print(e.with_traceback())
            exit(e)

    def load_all_plugins(self):
        for name in self.available_plugins:
            self.load_plugin(name)