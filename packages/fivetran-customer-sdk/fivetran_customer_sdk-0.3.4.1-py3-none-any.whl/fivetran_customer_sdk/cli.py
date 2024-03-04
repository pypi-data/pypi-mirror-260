import argparse
import importlib.util
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser()

    # Positional
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument("deploy", action="store_true", help="Deploy the connector")
    # group.add_argument("debug", action="store_true", help="Debug the connector")
    # group.add_argument("run", action="store_true", help="Run the connector")
    parser.add_argument("command", help="debug|run|deploy")
    parser.add_argument("project_path", nargs='?', default=os.getcwd(), help="Path to connector project directory")

    # Optional (Not all of these are valid with every mutually exclusive option below)
    parser.add_argument("--port", type=int, default=50051, help="Provide port number to run gRPC server")
    parser.add_argument("--state", type=str, default=None, help="Provide state as JSON string or file")
    parser.add_argument("--configuration", type=str, default=None,
                        help="Provide secrets and payloads as JSON string or file")
    parser.add_argument("--deploy-key", type=str, default=None, help="Provide deploy key")
    parser.add_argument("--group", type=str, default=None, help="Group name of the destination")
    parser.add_argument("--connector", type=str, default=None, help="Connector name (aka 'schema')")

    args = parser.parse_args()

    # Process optional args
    ft_group = args.group if args.group else os.getenv('GROUP', None)
    ft_connector = args.connector if args.connector else os.getenv('CONNECTOR', None)
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
    main_py = os.path.join(args.project_path, "main.py")
    spec = importlib.util.spec_from_file_location(module_name, main_py)
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

        deploy_config_file = os.path.join(args.project_path, "deploy.json")
        if os.path.isfile(deploy_config_file):
            with open(deploy_config_file, 'r') as fi:
                deploy_config_json = json.load(fi)
            if 'deploy_key' in deploy_config_json:
                if deploy_key:
                    print("ERROR: Multiple settings for 'deploy-key', deploy.json file will be used")
                deploy_key = deploy_config_json['deploy_key']
            if 'group' in deploy_config_json:
                if ft_group:
                    print("ERROR: Multiple settings for 'group', deploy.json file will be used")
                ft_group = deploy_config_json['group']
            if 'connector' in deploy_config_json:
                if deploy_key:
                    print("ERROR: Multiple settings for 'connector', deploy.json file will be used")
                ft_connector = deploy_config_json['connector']
            if 'configuration' in deploy_config_json:
                if deploy_key:
                    print("ERROR: Multiple settings for 'configuration', deploy.json file will be used")
                configuration = deploy_config_json['configuration']
        connector_object.deploy(args.project_path, deploy_key, ft_group, ft_connector, configuration)

    elif args.command.lower() == "debug":
        connector_object.debug(args.project_path, args.port, configuration, state)

    elif args.command.lower() == "run":
        connector_object.run(args.port, configuration, state)

    else:
        raise NotImplementedError("Invalid command: ", args.command)
