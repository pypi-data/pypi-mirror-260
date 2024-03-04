from .aws_svc import aws
from .shopping import shopping

SERVICES = {
    aws().service: aws(),
    shopping().service: shopping()

}

