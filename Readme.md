## Policy management tool for AWS
A simple script for managing attached policies to AWS IAM entitites, written in Python

## Prerequisites
* boto3
* python 3.6 or higher

All dependencies can be installed by any package manager like pip, anaconda, virtualenv, etc.

### Right before running this script
Before making use of this script, make sure you have your AWS credentials defined on your system, either by [IAM console](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) or having the AWS CLI installed and going to `aws configure`, more info on this can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

---

The script will start by asking you to provide a policy arn, not the friendly name of it but the amazon resource name.

`Ex: arn:aws:iam::aws:policy/AmazonEC2FullAccess`

## What the script offers

```
Enter a number to choose:
 1.List entities using a policy
 2.Only delete a policy
 3.Replace a policy
```

* **Option 1** will only list and display all existing roles, groups and users from the AWS linked account, if the policy has no entities, it will return empty.
  
```
Resources with "arn:aws:iam::aws:policy/examplePolicy" attached:
 - Users:
 ['user']
 - Roles:
 ['role']
 - Groups:
 ['group']
 ```

* **Option 2** will only detach the policy defined above from **ALL** the entities listed right away, this can't be undone once you select option 2.
* **Option 3** will remove the policy you defined and will ask you for a new arn to attach to the same entities.

To check all entities listed before have been detached from their policy or attached the new one, run the script again on **Option 1** (introducing the attached/detached policy accordingly)
