from pssh.clients import SSHClient 

hosts = []
while 1:
    new_ip = input("IP (ENTER for done):")
    if new_ip == '':
        break
    hosts.append(new_ip)

client = ParallelSSHClient(hosts)

while 1:
    output = client.run_command(input("Command:"))
    for host_output in output:
        for line in host_output.stdout:
            print(line)


