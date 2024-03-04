def generate_frame_work():
    pass

def generate_entrypoint(code_dir, parameters):
    s = f"from train import train\n"
    s += f"import os\n"
    s += f"import json\n"
    s += f"import argparse\n\n"
    s += f"def parse_args():\n"
    s += f"\tparser = argparse.ArgumentParser()\n"
    for argument in parameters:
        value = parameters[argument]["value"]
        param_type = parameters[argument]["type"]
        metavar = parameters[argument]["metavar"]
        param_help = parameters[argument]["param_help"]
        s += f"\tparser.add_argument(\n"
        s += f"\t\t\"--{argument}\",\n".replace('_', '-')
        s += f"\t\ttype={param_type},\n"
        s += f"\t\tdefault={value},\n"
        s += f"\t\tmetavar=\"{metavar}\",\n"
        s += f"\t\thelp=\"{param_help}\",\n"
        s += f"\t)\n"
    s += "\n"
    s += "\tparser.add_argument(\"--hosts\", type=list, default=json.loads(os.environ[\"SM_HOSTS\"]))\n"
    s += "\tparser.add_argument(\"--current-host\", type=str, default=os.environ[\"SM_CURRENT_HOST\"])\n"
    s += "\tparser.add_argument(\"--model-dir\", type=str, default=os.environ[\"SM_MODEL_DIR\"])\n"
    s += "\tparser.add_argument(\"--train\", type=str, default=os.environ[\"SM_CHANNEL_TRAINING\"])\n"
    s += "\tparser.add_argument(\"--test\", type=str, default=os.environ[\"SM_CHANNEL_TESTING\"])\n"
    s += "\tparser.add_argument(\"--num-gpus\", type=int, default=os.environ[\"SM_NUM_GPUS\"])\n\n"
    s += "\treturn parser.parse_args()\n\n"
    s += f"if __name__ == \"__main__\":\n"
    s += f"\targs = parse_args()\n"
    s += f"\ttrain(args)\n"

    with open(f"{code_dir}/entry-point.py", 'w') as f:
        f.write(s)

    hyperparameters = {argument: parameters[argument]["value"]
                       for argument in parameters}

    return hyperparameters
