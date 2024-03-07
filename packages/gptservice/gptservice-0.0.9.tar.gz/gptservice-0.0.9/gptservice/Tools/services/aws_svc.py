from .features import Service


class aws(Service):

    @property
    def service(self):
        return "AWS"
    
    @property
    def content(self):
        return "As a Cloud service assistant, you must have the service_name and region to construct any service. These two details are mandatory, and if any of those two details are missing, prompt for both service and region. Additionally, if the output contains string 'Public IP', it means that the resource has been constructed. In such cases, return the output with details like public IP, id, and the state of the resource in a natural language always."
    
    @property
    def tools(self):
        return  {
            "name": "invoke_aws_service",
            "description": "Invoke an AWS service",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "The name of the AWS service to invoke"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Build or Terminate a service"
                    },
                    "region": {
                        "type": "string",
                        "description": "The AWS region to use for the service call"
                    },

                    "name": {
                        "type": "string",
                        "description": "The name of the instance"
                    }
                }
            },
            "required": ["service_name", "operation", "region"]
            
        }