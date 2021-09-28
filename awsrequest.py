import boto3
from typing import List

Client = boto3.client('iam') 

class bcolors:
    """A class used for highlighting warnings and messages in printed strings, using ANSI escape codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE        = "\033[97m"

def list_if_empty(list:List):
    if len(list) == 0:
        return 0
    else:
        return 1

def get_entities(p_arn, entity_name) -> List[str]:
    """Using the boto3 module calling the AWS API, this function retrieves the json response and iterates between pages and their dicts
    returning only the value defined accordingly (users, groups, roles)"""
    entities = []
    paginator = Client.get_paginator('list_entities_for_policy')
    for response in paginator.paginate(        
        PolicyArn=p_arn, 
        EntityFilter=entity_name):
        response_names = [r.get('{ent}Name'.format(ent=entity_name)) for r in response['Policy{ent}s'.format(ent=entity_name)]]
        entities.extend(response_names)
    return entities

def initial_response(p_arn,users,roles,groups):
    """A simple message feedback displaying all the entities listed by the get_entitites function"""
    message = 'Resources with "{arn}" attached:\n - Users:\n {users}\n - Roles:\n {roles}\n - Groups:\n {groups} '.format(
        arn=p_arn,
        users=users,
        roles=roles,
        groups=groups
    )
    print(message)

def param_validation_arn(message:str):
    """For validating user provided arn"""
    StatusCode = 0
    while StatusCode != 200:
        try: 
            arn = input(message)
            response = Client.list_policy_versions(
                PolicyArn=arn
            )
            StatusCode = response['ResponseMetadata'].get('HTTPStatusCode')
        except Exception:
            print(f'{bcolors.WARNING}{bcolors.BOLD}====ERROR!====\n {bcolors.WHITE}{bcolors.ENDC}The arn you provided is invalid!')
            continue
        break
    return arn

def detach_policy_per_entity(p_arn,users,roles,groups):
    """Using the boto3 module calling the AWS API, all entities listed by the get_entitites function will be detached 
    from a user defined policy"""
    httpstatus_dump=[200]
    detached_user_response = [Client.detach_user_policy(UserName=x,PolicyArn=p_arn) for x in users]
    detached_role_response = [Client.detach_role_policy(RoleName=y,PolicyArn=p_arn)for y in roles]
    detached_group_response = [Client.detach_group_policy(GroupName=z,PolicyArn=p_arn)for z in groups]
    response_user = [response['ResponseMetadata'].get('HTTPStatusCode') for response in detached_user_response]
    response_role = [response['ResponseMetadata'].get('HTTPStatusCode') for response in detached_role_response]
    response_group = [response['ResponseMetadata'].get('HTTPStatusCode') for response in detached_group_response]
    total_response = httpstatus_dump + response_user + response_role + response_group
    check_if_done = all(element == total_response[0] for element in total_response)
    if (check_if_done):
        print(f'{bcolors.OKBLUE}Done, all policies were detached from the listed entities.\n {bcolors.WHITE}')
    else:
        print('Something went wrong')

def attach_policy_per_entity(new_p_arn,users,roles,groups):
    """Using the boto3 module calling the AWS API, all entities listed by the get_entitites function will be attached
    a new policy, defined by the user"""
    httpstatus_dump=[200]
    attached_user_response = [Client.attach_user_policy(UserName=x,PolicyArn=new_p_arn) for x in users]
    attached_role_response = [Client.attach_role_policy(RoleName=y,PolicyArn=new_p_arn)for y in roles]
    attached_group_response = [Client.attach_group_policy(GroupName=z,PolicyArn=new_p_arn)for z in groups]
    response_user = [response['ResponseMetadata'].get('HTTPStatusCode') for response in attached_user_response]
    response_role = [response['ResponseMetadata'].get('HTTPStatusCode') for response in attached_role_response]
    response_group = [response['ResponseMetadata'].get('HTTPStatusCode') for response in attached_group_response]
    total_response = httpstatus_dump + response_user + response_role + response_group
    check_if_done = all(element == total_response[0] for element in total_response)
    if (check_if_done):
        print(f'{bcolors.OKBLUE} Done, all entities have the policy attached.')
    else:
        print('Something went wrong')
