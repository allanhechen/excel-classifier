import importlib
import pkgutil
import inspect
from pathlib import Path

from AbstractCategory import Category

package_name = __name__.rsplit(".", 1)[0]
dir = Path(__file__).parent

all_classes = set()

for _, module_name, _ in pkgutil.iter_modules([str(dir)]):
    if module_name != "_MarketingCategory":
        module = importlib.import_module(f"{package_name}.{module_name}")

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__:
                all_classes.add(obj)


class MarketingCategory(Category):
    def __init___(self):
        super().__init__("Marketing", expense_groups=all_classes)
