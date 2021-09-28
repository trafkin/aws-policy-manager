import boto3
from awsrequest import get_entities,detach_policy_per_entity,attach_policy_per_entity,initial_response,bcolors

Client = boto3.client('iam') 
iam = boto3.resource('iam')

option_value = 0
policyArnfromUser = ""
newPolicyArnfromUser = ""
users = []
roles = []
groups = []

policyArnfromUser = input('Please enter the policy arn: ')

users_call = get_entities(policyArnfromUser, 'User')
roles_call = get_entities(policyArnfromUser, 'Role')
groups_call =get_entities(policyArnfromUser, 'Group')

def main_program(user_value):
    """This function handles the call of get_entities, detach_policy_per_entity and attach_policy_per_entity upon the user's option"""
    if option_value == 1:
        return initial_response(p_arn=policyArnfromUser,users=users_call,roles=roles_call,groups=groups_call)
    elif option_value == 2:
        return detach_policy_per_entity(p_arn=policyArnfromUser,users=users_call,roles=roles_call,groups=groups_call), initial_response(p_arn=policyArnfromUser,users=users_call,roles=roles_call,groups=groups_call),print(f'{bcolors.OKBLUE}{bcolors.BOLD} If you want to make sure the process finished succesfully, run the script again and select option 1\n It should display an empty list.{bcolors.WHITE}{bcolors.ENDC}')
    elif option_value == 3:
        newPolicyArnfromUser = input(f'{bcolors.BOLD}Please enter the new policy that will be attached:{bcolors.ENDC}')
        return detach_policy_per_entity(p_arn=policyArnfromUser,users=users_call,roles=roles_call,groups=groups_call), attach_policy_per_entity(new_p_arn=newPolicyArnfromUser,users=users_call,roles=roles_call,groups=groups_call),print(f'{bcolors.OKBLUE}{bcolors.BOLD} If you want to make sure process finished succesfully, run the script again and select option 1, introducing the attached ARN.{bcolors.WHITE}{bcolors.ENDC}')

while (option_value != 1 and option_value != 2 and option_value != 3):
    """Error handling for user's option input"""
    option_value = input(f'Enter a number to choose:\n{bcolors.BOLD} 1.List entities using a policy\n 2.Only delete a policy\n 3.Replace a policy\n{bcolors.ENDC}')
    if (not option_value.isdigit() or (option_value == '')):
        print(f'{bcolors.WARNING}{bcolors.BOLD}====ERROR!====\n {bcolors.WHITE}{bcolors.ENDC}- Enter a valid number\n')
    else:
        option_value = int(option_value)
        main_program(user_value=option_value)