import re
import socket

def is_ip(ip):
    pattern = re.compile(r'^(((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))$')
    if pattern.search(ip):
        return True
    else:
        return False


def is_domain(domain):
    pattern = re.compile(r'^([a-zA-Z0-9]([a-zA-Z0-9]|-)*)(\.([a-zA-Z0-9]|-)+){1,2}$')
    if len(domain) < 26 and pattern.search(domain):
        return True
    else:
        return False


#socket
def is_ip_1(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False


def is_domain_1(domain):
    try:
        socket.getaddrinfo(domain,None,0,socket.SOCK_STREAM)
        return True
    except:
        return False

#Recommended
def is_domain_2(ioc):
    if not re.search('^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,10}$', ioc):
        return False
    return True


print(is_domain('www..com'))
print(is_ip("127.0.0.1"))

print(is_domain_1('www..com'))
print(is_ip_1("127.0.0.1"))