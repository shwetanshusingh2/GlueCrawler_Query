import boto3
import User_Defined_Variables as user_variable
import time


class Stack:
    def stack_status(self, stack_name):
        try:
            stack = user_variable.CLIENT.describe_stacks(StackName=stack_name)
            status = stack['Stacks'][0]['StackStatus']
            return status
        except Exception:
            return "NO_STACK"

    def create_upload_stack(self):
        status = self.stack_status(user_variable.STACK_NAME)
        if status == 'ROLLBACK_COMPLETE' or \
                status == 'ROLLBACK_FAILED' or \
                status == 'UPDATE_ROLLBACK_COMPLETE' or \
                status == 'DELETE_FAILED':

            self.delete_object(user_variable.UPLOAD_OBJECT_BUCKET)
            user_variable.CLIENT.delete_stack(StackName=user_variable.STACK_NAME)
            while self.stack_status(user_variable.STACK_NAME) == 'DELETE_IN_PROGRESS':
                time.sleep(1)
            print("stack deleted")
            self.create_stack(user_variable.STACK_NAME, user_variable.TEMPLATE_URL, user_variable.UPLOAD_OBJECT_BUCKET)
            print("stack created")
        elif status == 'CREATE_COMPLETE' or status == 'UPDATE_COMPLETE':
            self.update_stack(user_variable.STACK_NAME, user_variable.TEMPLATE_URL, user_variable.UPLOAD_OBJECT_BUCKET)
            print("stack updated")
        else:
            self.create_stack(user_variable.STACK_NAME, user_variable.TEMPLATE_URL, user_variable.UPLOAD_OBJECT_BUCKET)
            print("stack created")

        while self.stack_status(user_variable.STACK_NAME) == 'CREATE_IN_PROGRESS' or \
                self.stack_status(user_variable.STACK_NAME) == 'UPDATE_IN_PROGRESS' or \
                self.stack_status(user_variable.STACK_NAME) == 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS':
            print("waiting to create")
            time.sleep(1)


    def delete_object(self,bucket_name):
        try:
            bucket = user_variable.s3_client.Bucket(bucket_name)
            bucket.objects.all().delete()
        except Exception:
            print("Bucket Not Present")

    def create_stack(self, stack_name, template_url, source):
        response = user_variable.CLIENT.create_stack(
            StackName=stack_name,
            TemplateURL=template_url,
            Capabilities=['CAPABILITY_NAMED_IAM'],
            Parameters=[{
                'ParameterKey': "SourceBucket",
                'ParameterValue': source
            }]

        )

    def update_stack(self,stack_name, template_url, source):
        try:
            response = user_variable.CLIENT.update_stack(
                StackName=stack_name,
                TemplateURL=template_url,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Parameters=[{
                    'ParameterKey': "SourceBucket",
                    'ParameterValue': source
                }]

            )
        except Exception:
            print("No update To Perform")
