from .aws_svc import aws
from .shopping import shopping
from .flights import flights

SERVICES = {
    aws().service: aws(),
    shopping().service: shopping(),
    flights().service: flights()
    
}

