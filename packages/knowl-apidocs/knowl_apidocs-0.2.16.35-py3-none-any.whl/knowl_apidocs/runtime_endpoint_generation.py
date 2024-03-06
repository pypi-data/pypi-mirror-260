import argparse
import json
import os
import re
import sys
import importlib.util
from importlib import import_module
from django.conf import settings
import io
from django.contrib.admindocs.views import simplify_regex

from exception import CustomExceptionHandler

def ensure_absolute_path(path):
    if path is not None:
        path = os.path.abspath(path)
    return path

path_to_regex = dict()
def import_module_from_path(file_path, project_path):
    # Get the module name from the file path
    rel_path = os.path.relpath(file_path, start=project_path)
    module_package = rel_path[:-3].replace("/", ".")
    module_name = module_package.split('.')[-1]
    package = ".".join(module_package.split('.')[:-1])

    # Create a spec for the module
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    # Import the module
    module = importlib.util.module_from_spec(spec)
    module.__package__ = package
    spec.loader.exec_module(module)

    return module

def split_forward_slash(url):
    cur = ""
    arrow = 0 # <>
    curved = 0 # ()
    curly = 0 # {}
    square = 0 # []
    final = []
    for c in url:
        if c == "<":
            arrow+=1
        elif c == ">":
            arrow-=1
        elif c == "{":
            curly+=1
        elif c == "}":
            curly-=1
        elif c == "(":
            curved+=1
        elif c == ")":
            curved-=1
        elif c == "[":
            square+=1
        elif c == "]":
            square-=1
        if c == "/" and arrow == 0 and curly == 0 and curved == 0 and square == 0:
            if len(cur) > 0:
                final.append(cur)
            cur = ""
        else:
            cur += c
    if len(c) > 0:
        final.append(cur)
    return final


def parse_url(url):
    url_split = split_forward_slash(path_to_regex[url])
    parameters = []
    for u in url_split:
        if len(u) == 0:
            continue
        name = None
        if "(?P" in u:
            name = u[u.find("<") + 1: u.find(">")] if "<" in u else None
            pattern = u[u.find(">") + 1: -1]
            parameters.append({
                "name": name,
                "pattern": pattern,
                "type": None
            })
        elif ":" in u:
            type_ = u[1:u.find(":")]
            name = u[u.find(":")+1:-1]
            parameters.append({
                "name": name,
                "pattern": None,
                "type": type_
            })
        elif u[0] == "{":
            name = u[1:-1]
            parameters.append({
                "name": name,
                "pattern": None,
                "type": None
            })
    return {
        "url":url.replace("<", "{").replace(">", "}"),
        "parameter": parameters
    }


def get_endpoints(project_path, url_conf):
    try:
        django = import_module("django")
    except ImportError:
        raise ImportError("Django is not installed. Please install django before running this script")
    django.setup()

    try:
        from rest_framework.schemas.generators import EndpointEnumerator
    except ImportError:
        raise ImportError(
            "rest_framework is not installed. Please install rest_framework before running this script"
        )
    
    # Dont remove this
    def endpoint_ordering(endpoint):
        path, method, callback = endpoint
        method_priority = {"GET": 0, "POST": 1, "PUT": 2, "PATCH": 3, "DELETE": 4}.get(method, 5)
        return (method_priority,)

    class EndpointEnumerator(EndpointEnumerator):
        def get_path_from_regex(self, path_regex):
            """
            Given a URL conf regex, return a URI template string.
            """
            # ???: Would it be feasible to adjust this such that we generate the
            # path, plus the kwargs, plus the type from the convertor, such that we
            # could feed that straight into the parameter schema object?
            path = simplify_regex(path_regex)
            _PATH_PARAMETER_COMPONENT_RE = re.compile(r"<(?:(?P<converter>[^>:]+):)?(?P<parameter>\w+)>")
            processed_path = re.sub(_PATH_PARAMETER_COMPONENT_RE, r"{\g<parameter>}", path)
            path_to_regex[processed_path] = path_regex
            return processed_path


    urlconf = import_module_from_path(url_conf, project_path)
    endpoint_enumerator = EndpointEnumerator(urlconf=urlconf)
    endpoints = endpoint_enumerator.get_api_endpoints()
    processed_endpoints = []

    from rest_framework.schemas.generators import BaseSchemaGenerator


    generator = BaseSchemaGenerator()
    for endpoint in endpoints:
        url_dict = parse_url(endpoint[0])
        url = url_dict["url"]
        view = generator.create_view(endpoint[2], endpoint[1])
        n_url = generator.coerce_path(url, endpoint[1], view)
        match1 = re.findall(r'\{(.*?)\}', url)
        match2 = re.findall(r'\{(.*?)\}', n_url)
        for m1, m2 in zip(match1, match2):
            for parameter in url_dict["parameter"]:
                if parameter["name"] == m1:
                    parameter["name"] = m2
                    break
        url_dict["url"] = n_url
        processed_endpoints.append((url_dict, endpoint[1], endpoint[2]))
    final = []
    for endpoint in processed_endpoints:
        name = endpoint[2].__name__ if endpoint[2].__name__ != "view" else endpoint[2].cls.__name__
        if "actions" in endpoint[2].__dir__():
            final.append(
                {
                    "url": endpoint[0],
                    "is_viewset": True,
                    "method": endpoint[1],
                    "view":  name,
                    "path": os.path.join(project_path, endpoint[2].__module__.replace(".", "/") + ".py"),
                    "function": getattr(endpoint[2], "actions")[endpoint[1].lower()],
                }
            )
        else:
            final.append(
                {
                    "url": endpoint[0],
                    "is_viewset": False,
                    "method": endpoint[1],
                    "view": name,
                    "path": os.path.join(project_path, endpoint[2].__module__.replace(".", "/") + ".py"),
                }
            )
    return final

def set_settings_conf(manage_py):
    exec(manage_py)
    return 

def main(input_dir, result_dir, url_file, starting_point, settings_conf = None):
    log_dir = os.path.join(input_dir, ".knowl_logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "knowl_debug.log")
    stdout_handle = open(log_file, 'a')
    original_ = sys.stdout
    sys.stdout = stdout_handle
    try:
        input_dir = ensure_absolute_path(input_dir)
        result_dir = ensure_absolute_path(result_dir)
        url_file = ensure_absolute_path(url_file)
        starting_point = ensure_absolute_path(starting_point)

        print(f"runtime_gen input:\ninput_path: {input_dir}\nresult_dir: {result_dir}\nurl_file: {url_file}\nsettings_conf: {settings_conf}")

        project_path = os.path.dirname(starting_point)
        sys.path.append(project_path)
        if settings_conf is None:
            with open(starting_point, 'r') as file:
                manage_py = file.read()
            old_argv = sys.argv
            sys.stdout = io.StringIO()  
            sys.argv = [starting_point]
            try:
                set_settings_conf(manage_py)
            finally:
                sys.stdout = stdout_handle
                sys.argv = old_argv
        else:
            os.environ["DJANGO_SETTINGS_MODULE"] = settings_conf
        print(f"Settings Module: {os.environ['DJANGO_SETTINGS_MODULE']}")
        settings_dict = vars(settings)
        rest_framework_settings_dict = settings_dict.get("REST_FRAMEWORK", {})
        DEFAULT_PAGINATION_CLASS = rest_framework_settings_dict.get("DEFAULT_PAGINATION_CLASS", None)
        PAGE_SIZE = rest_framework_settings_dict.get("PAGE_SIZE", None)
        DEFAULT_AUTHENTICATION_CLASSES = rest_framework_settings_dict.get("DEFAULT_AUTHENTICATION_CLASSES", None)
        DEFAULT_FILTER_BACKENDS = rest_framework_settings_dict.get("DEFAULT_FILTER_BACKENDS", None)

        input_path = os.path.abspath(input_dir)
        files_list = []
        for root, dir, files in os.walk(input_path):
            for file in files:
                if file.endswith(".py"):
                    files_list.append(os.path.join(root, file))

        sys.path.append(url_file) 
        endpoints = get_endpoints(project_path, url_file)
        output = {
            "endpoints": endpoints,
            "DEFAULT_PAGINATION_CLASS": DEFAULT_PAGINATION_CLASS,
            "PAGE_SIZE": PAGE_SIZE,
            "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
            "DEFAULT_FILTER_BACKENDS": DEFAULT_FILTER_BACKENDS
            }
        output_file_name = "django_endpoints.json"
        output_file_path = os.path.join(result_dir, output_file_name)
        with open(output_file_path, "w") as f:
            json.dump(output, f, indent=2)
    finally:
        sys.stdout = original_
        stdout_handle.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to bucket files based on the language")
    parser.add_argument("input_dir", type=str, help="Input directory path")
    parser.add_argument("result_dir", type=str, help="Result directory path")
    parser.add_argument("url_file", type=str, help="URL conf", default=None)
    parser.add_argument("starting_point", type=str, default=None)
    parser.add_argument("settings_conf", type=str, default=None, nargs='?')
    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        exit(1)

    if not os.path.exists(args.result_dir):
        exit(1)
    with CustomExceptionHandler(args.input_dir):
        main(args.input_dir, args.result_dir, args.url_file, args.starting_point, args.settings_conf)
