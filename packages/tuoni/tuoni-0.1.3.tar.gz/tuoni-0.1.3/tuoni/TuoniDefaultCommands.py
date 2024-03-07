import base64

class TuoniDefaultCommand:
    def __init__(self, command_type, command_conf):
        self.command_type = command_type
        self.command_conf = command_conf
        self.execution_conf = None
        self.files = None

class TuoniDefaultPluginCommand(TuoniDefaultCommand):
    def __init__(self, command_type, command_conf, execution_conf = None):
        super().__init__(command_type, command_conf)
        if isinstance(execution_conf, ExecutionNew):
            self.execution_conf = {
                "execType": "NEW",
                "executable": execution_conf.proc_name,
                "suspended": execution_conf.suspended
            }
        elif isinstance(execution_conf, ExecutionExisting):
            self.execution_conf = {
                "execType": "EXISTING",
                "pid": execution_conf.pid
            }
        else:
            self.execution_conf = execution_conf


class ExecutionNew:
    def __init__(self, proc_name="notepad.exe", suspended=True):
        self.proc_name = proc_name
        self.suspended = suspended

class ExecutionExisting:
    def __init__(self, pid):
        self.pid = pid


#########################
## Native commands
#########################
class TuoniCommandBof(TuoniDefaultCommand):
    def __init__(self, bof_file, method, input):
        super().__init__("bof", {"method": method, "inputArgs": input})
        self.files = {"bofFile": ["filename.bin", bof_file]}


class TuoniCommandCd(TuoniDefaultCommand):
    def __init__(self, dir):
        super().__init__("cd", {"dir": dir})


class TuoniCommandDie(TuoniDefaultCommand):
    def __init__(self):
        super().__init__("die", {})


class TuoniCommandLs(TuoniDefaultCommand):
    def __init__(self, dir, depth):
        super().__init__("ls", {"dir": dir, "depth": depth})


class TuoniCommandCmd(TuoniDefaultPluginCommand):
    def __init__(self, command):
        super().__init__("cmd", {"command": command})


class TuoniCommandJobs(TuoniDefaultPluginCommand):
    def __init__(self):
        super().__init__("jobs", {})


class TuoniCommandProclist(TuoniDefaultPluginCommand):
    def __init__(self):
        super().__init__("ps", {})


class TuoniCommandRun(TuoniDefaultPluginCommand):
    def __init__(self, cmdline, output):
        super().__init__("run", {"cmdline": cmdline, "output": output})


class TuoniCommandPowershell(TuoniDefaultPluginCommand):
    def __init__(self, command):
        super().__init__("powershell", {"command": command})


class TuoniCommandSleep(TuoniDefaultPluginCommand):
    def __init__(self, sleep_time, sleep_random):
        super().__init__("sleep", {"sleep": sleep_time, "sleepRandom": sleep_random})

#########################
## Native token commands
#########################
class TuoniCommandTokenAdd(TuoniDefaultPluginCommand):
    def __init__(self, pid):
        super().__init__("token-add", {"pid": pid})


class TuoniCommandTokenDeleteAll(TuoniDefaultPluginCommand):
    def __init__(self):
        super().__init__("token-del-all", {})


class TuoniCommandTokenDelete(TuoniDefaultPluginCommand):
    def __init__(self, nr):
        super().__init__("token-add", {"nr": nr})


class TuoniCommandTokenList(TuoniDefaultPluginCommand):
    def __init__(self):
        super().__init__("token-list", {})


class TuoniCommandTokenMake(TuoniDefaultPluginCommand):
    def __init__(self, username, password):
        super().__init__("token-make", {"username": username, "password": password})


class TuoniCommandTokenUse(TuoniDefaultPluginCommand):
    def __init__(self, nr):
        super().__init__("token-use", {"nr": nr})


#########################
## Plugin FS commands
#########################

class TuoniCommandFileDelete(TuoniDefaultPluginCommand):
    def __init__(self, filepath, execution_conf = None):
        super().__init__("fs-delete", {"filepath": filepath}, execution_conf)


class TuoniCommandFileRead(TuoniDefaultPluginCommand):
    def __init__(self, filepath, execution_conf = None):
        super().__init__("fs-read", {"filepath": filepath}, execution_conf)


class TuoniCommandFileWrite(TuoniDefaultPluginCommand):
    def __init__(self, filepath, data, execution_conf = None):
        super().__init__("fs-write", {"filepath": filepath}, execution_conf)
        self.files = {"file": ["filename.bin", data]}

#########################
## Plugin NET commands
#########################

class TuoniCommandSocks5(TuoniDefaultPluginCommand):
    def __init__(self, port, execution_conf = None):
        super().__init__("socks5", {"port": port}, execution_conf)


class TuoniCommandConnectTcp(TuoniDefaultPluginCommand):
    def __init__(self, host, port, execution_conf = None):
        super().__init__("connect-tcp", {"host": host, "port": port}, execution_conf)

#########################
## Plugin OS commands
#########################


class TuoniCommandExecAsm(TuoniDefaultPluginCommand):
    def __init__(self, executable, parameters, execution_conf = None):
        super().__init__("execute-assembly", {"parameters": parameters}, execution_conf)
        self.files = {"executable": ["filename.bin", executable]}


class TuoniCommandInject(TuoniDefaultPluginCommand):
    def __init__(self, shellcode, execution_conf = None):
        super().__init__("inject", {}, execution_conf)
        self.files = {"shellcode": ["filename.bin", shellcode]}


class TuoniCommandProcinfo(TuoniDefaultPluginCommand):
    def __init__(self, execution_conf = None):
        super().__init__("procinfo", {}, execution_conf)


class TuoniCommandSpawn(TuoniDefaultPluginCommand):
    def __init__(self, listener_id, payload_type, encrypted_communication, execution_conf = None):
        super().__init__("spawn", {"listenerId": listener_id, "payloadType": payload_type, "encryptedCommunication": encrypted_communication}, execution_conf)