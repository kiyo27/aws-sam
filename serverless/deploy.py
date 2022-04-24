import boto3
from botocore.exceptions import ClientError
import argparse

client = boto3.client("lambda")
parser = argparse.ArgumentParser()
parser.add_argument("fn")
args = parser.parse_args()


def get_zip_content(zip_name):
    with open(zip_name, "rb") as f:
        bytes_content = f.read()
    return bytes_content


def deploy(**kwargs):
    try:
        client.get_function(FunctionName=kwargs["FunctionName"])
        update(**kwargs)
    except ClientError:
        create(**kwargs)


def create(**kwargs):
    valid_args = ["FunctionName", "Code", "Handler", "Role", "Runtime", "Architectures"]
    return client.create_function(**_build_deploy_args(kwargs, valid_args))


def update(**kwargs):
    valid_args = ["FunctionName", "Qualifier"]
    return client.update_function_code(_build_deploy_args(kwargs, valid_args))


def _build_deploy_args(arg_list, valid_args):
    deploy_args = dict()
    for key in arg_list:
        if key in valid_args:
            deploy_args.update({key: arg_list[key]})
    return deploy_args


def get_role_arn(role_name):
    iam = boto3.resource("iam")
    role = iam.Role(role_name)
    return role.arn


if __name__ == "__main__":
    fn = args.fn
    code = get_zip_content(f"artifacts/{fn}.zip")
    deploy_args = {
        "FunctionName": fn,
        "Code": {"ZipFile": code},
        "Handler": "app.lambda_handler",
        "Role": get_role_arn("basic-lambda-role"),
        "Runtime": "python3.9",
        "Architectures": ["x86_64"],
    }
    deploy(**deploy_args)
