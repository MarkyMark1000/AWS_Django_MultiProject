import requests

def appendIPToArray(inALLOWED_HOSTS):
    '''
    Once I started filling ALLOWED_HOSTS with specific addresses, the health of the
    Elastic Beanstalk Environments started degrading or lightsail kept 
    filling the logs with messages about adding a specific ip address to
    ALLOWED HOSTS.   This code gets the IP address and adds it to the
    ALLOWED_HOSTS list, preventin unnecessary logs and health degredation.
    '''

    try:
        # Try to get the IP
        EC2_PRIVATE_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4',
                                  timeout=0.01).text
        # If we get an IP, append it to the array
        if EC2_PRIVATE_IP:
            if EC2_PRIVATE_IP not in inputArray:
                inputArray.append(EC2_PRIVATE_IP)
            return True
        else:
            return False

    except Exception as Ex:
        # Do nothing, it is better to let the sytem continue
        pass