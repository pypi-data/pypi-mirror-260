# zxel3525Api

A wrapper to access a Zyxel BMG3525 with python and receive back JSON data that can be stored to a database.

    from zyxel3525Api import ZyxelApi
    api = ZyxelApi('192.168.0.1', 'username', 'password') [comment]: Use the ip and access details for your router
    logs = api.get_log()

For help on other functions help(zyxel3525Api)