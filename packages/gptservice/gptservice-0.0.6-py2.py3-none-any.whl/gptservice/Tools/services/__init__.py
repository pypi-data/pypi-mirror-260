from Tools.services.aws_svc import aws
from Tools.services.shopping import shopping

SERVICES = {
    aws().service: aws(),
    shopping().service: shopping()

}

