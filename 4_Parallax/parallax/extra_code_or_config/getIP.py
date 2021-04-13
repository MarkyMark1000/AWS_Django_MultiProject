import requests
import socket

def appendIPToArray(inALLOWED_HOSTS):
    '''
    Once I started filling ALLOWED_HOSTS with specific addresses, the health of the
    Elastic Beanstalk Environments started degrading or lightsail kept 
    filling the logs with messages about adding a specific ip address to
    ALLOWED HOSTS.   This code gets the IP address and adds it to the
    ALLOWED_HOSTS list, preventin unnecessary logs and health degredation.
    '''

    # This may be difficult to unittest in a local environment because the
    # URL 'http://169.254.169.254/latest/meta-data/local-ipv4' is
    # specific to AWS.
    
    try:
        # Try to get the IP
        EC2_PRIVATE_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4',
                                  timeout=0.01).text
        # If we get an IP, append it to the array
        if EC2_PRIVATE_IP:
            if EC2_PRIVATE_IP not in inALLOWED_HOSTS:
                inALLOWED_HOSTS.append(EC2_PRIVATE_IP)
            return True
        else:
            return False

    except Exception as Ex:
        # Do nothing, it is better to let the sytem continue
        pass


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception as Ex:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP