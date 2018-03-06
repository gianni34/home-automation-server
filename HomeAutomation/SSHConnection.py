import paramiko


class Connection:

    def get_connection(host, user, password):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, 22, user, password)
        return ssh

    def execute_script(name, command):
        ssh_obj = Connection.get_connection('omega-EC2B', "root", "onioneer")
        stdin, stdout, stderr = ssh_obj.exec_command("python /root/" + name + " '" + command + "'")
        print("Ejecuto el proceso " + name + " correctamente.")
