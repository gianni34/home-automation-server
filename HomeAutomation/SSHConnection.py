import paramiko


class Connection:

    def get_connection(host, user, password):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, 22, user, password)
        return ssh

    def execute_script(intermediary, user, password, script, command):
        ssh_obj = Connection.get_connection(intermediary, user, password)
        stdin, stdout, stderr = ssh_obj.exec_command("python /root/" + script + " '" + command + "'")
        print("Ejecuto el proceso correctamente.")
