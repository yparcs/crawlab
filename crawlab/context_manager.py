import uuid


class ContextManager:
    def __init__(self, shell):
        self.ip = shell

    def get(self, key):
        if not self.ip.user_ns.get(key):
            raise Exception('{} not found'.format(key))
        return self.ip.user_ns[key]

    def set(self, key, value):
        self.ip.user_ns[key] = value

    def execute_and_get(self, command):
        tmp_key_name = '___tmp_' + str(uuid.uuid4().int)[:10]
        self.ip.kernel.do_execute('{}={}'.format(tmp_key_name, command), False, store_history=False)
        return self.get(tmp_key_name)