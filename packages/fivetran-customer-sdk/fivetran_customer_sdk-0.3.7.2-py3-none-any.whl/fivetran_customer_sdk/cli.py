import argparse
import importlib.util
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser()

    # Positional
    parser.add_argument("command", help="debug|run|deploy")
    parser.add_argument("project_path", nargs='?', default=os.getcwd(), help="Path to connector project directory")

    # Optional (Not all of these are valid with every mutually exclusive option below)
    parser.add_argument("--port", type=int, default=None, help="Provide port number to run gRPC server")
    parser.add_argument("--state", type=str, default=None, help="Provide state as JSON string or file")
    parser.add_argument("--configuration", type=str, default=None, help="Provide secrets as JSON string or file")
    parser.add_argument("--deploy-key", type=str, default=None, help="Provide deploy key")
    parser.add_argument("--group", type=str, default=None, help="Group name of the destination")
    parser.add_argument("--connection", type=str, default=None, help="Connection name (aka 'destination schema')")

    args = parser.parse_args()

    # Process optional args
    ft_group = args.group if args.group else os.getenv('GROUP', None)
    ft_connection = args.connection if args.connection else os.getenv('CONNECTION', None)
    deploy_key = args.deploy_key if args.deploy_key else os.getenv('DEPLOY_KEY', None)
    configuration = args.configuration if args.configuration else os.getenv('CONFIGURATION', None)
    state = args.state if args.state else os.getenv('STATE', None)
    if configuration:
        json_filepath = os.path.join(args.project_path, args.configuration)
        if os.path.isfile(json_filepath):
            with open(json_filepath, 'r') as fi:
                configuration = json.load(fi)
        elif configuration.lstrip().startswith("{"):
            configuration = json.loads(configuration)
    if state:
        json_filepath = os.path.join(args.project_path, args.state)
        if os.path.isfile(json_filepath):
            with open(json_filepath, 'r') as fi:
                state = json.load(fi)
        elif state.lstrip().startswith("{"):
            state = json.loads(state)

    module_name = "customer_connector_code"
    connector_py = os.path.join(args.project_path, "connector.py")
    spec = importlib.util.spec_from_file_location(module_name, connector_py)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    connector_object = None
    for obj in dir(module):
        if not obj.startswith('__'):  # Exclude built-in attributes
            obj_attr = getattr(module, obj)
            if '<fivetran_customer_sdk.Connector object at' in str(obj_attr):
                connector_object = obj_attr
                break
    if not connector_object:
        print("Unable to find connector object")
        sys.exit(1)

    if args.command.lower() == "deploy":
        if args.port:
            print("WARNING: 'port' parameter is not used for 'deploy' command")
        if args.state:
            print("WARNING: 'state' parameter is not used for 'deploy' command")
        connector_object.deploy(args.project_path, deploy_key, ft_group, ft_connection, configuration)

    elif args.command.lower() == "debug":
        port = 50051 if not args.port else args.port
        connector_object.debug(args.project_path, port, configuration, state)

    elif args.command.lower() == "run":
        port = 50051 if not args.port else args.port
        connector_object.run(port, configuration, state)

    else:
        raise NotImplementedError("Invalid command: ", args.command)
