import boto3
from botocore.exceptions import ClientError

client = boto3.client("lambda")


def get_zip_content(zip_name):
    with open(zip_name, "rb") as f:
        bytes_content = f.read()
    return bytes_content


def deploy(**kwargs):
    try:
        client.get_function(FunctionName=kwargs['FunctionName'])
        update(**kwargs)
    except ClientError:
        create(**kwargs)

def create(**kwargs):
    valid_args = ['FunctionName', 'Code', 'Handler', 'Role', 'Runtime', 'Architectures']
    opt = dict()
    for key in kwargs.keys():
        if key in valid_args:
            opt.update({key: kwargs[key]})
    return client.create_function(**opt)


def update(**kwargs):
    return client.update_function_code(**kwargs)


def get_role_arn(role_name):
    iam = boto3.resource("iam")
    role = iam.Role(role_name)
    return role.arn


if __name__ == "__main__":
    code = get_zip_content('artifacts/HelloWorldFunction.zip')
    k = {
        'FunctionName': 'test',
        'Code': {'ZipFile': code},
        'Handler': 'app.lambda_handler',
        'Role': get_role_arn('basic-lambda-role'),
        'Runtime': 'python3.9',
        'Architectures': ['x86_64']
    }
    deploy(**k)