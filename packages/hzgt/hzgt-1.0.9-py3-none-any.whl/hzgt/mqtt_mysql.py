import os
import threading

from .strop import restrop
from .CONST import INSTALLCMD
from .sc import SCError

try:
    import pymysql
except Exception as err:
    print(err)
    os.system(INSTALLCMD("pymysql==1.1.0"))
    import pymysql

try:
    import paho.mqtt.client as mqtt
except Exception as err:
    print(err)
    os.system(INSTALLCMD("paho-mqtt==1.6.1"))
    import paho.mqtt.client as mqtt


class Mqttop:
    def __init__(self, mqtt_host: str, mqtt_port: int, mqtt_clientid: str, mqtt_subtopic: str = '',
                 user: str = '', pwd: str = '', bool_show: bool = True, bool_clean_session: bool = False):
        """
        调用self.publish()函数发布信息

        :param mqtt_host: MQTT服务器IP地址
        :param mqtt_port: MQTT端口
        :param mqtt_clientid: "客户端"用户名
        :param mqtt_subtopic: 选填, 需要订阅的主题 通过self.got_datas获得接收到的信息 为空时仅连接[此时可进行发布信息]; 更换订阅主题需要使用self.retopic()函数[自动重连]

        :param user: 选填, 账号
        :param pwd: 选填, 密码
        """
        self.got_datas: str = None  # 接收到的数据
        self.bool_show = bool_show  # 是否终端打印连接相关信息
        self.bool_con_success = False  # 是否连接成功
        self.bool_clean_session = bool_clean_session  # 在断开连接时是否删除有关此客户端的所有信息, 若mqtt_clientid参数为空, 将强制为True

        self.mqtt_host = mqtt_host
        self.mqtt_port = int(mqtt_port)
        self.mqtt_clientid = mqtt_clientid
        self.mqtt_subtopic = mqtt_subtopic
        self.user = user
        self.pwd = pwd

        if len(self.mqtt_clientid) == 0 or self.mqtt_clientid is None:
            self.client = mqtt.Client(client_id="", clean_session=True)  # 创建对象, 强制clean_session=True
        else:
            self.client = mqtt.Client(client_id=self.mqtt_clientid, clean_session=self.bool_clean_session)  # 创建对象
        # self.start()

    def __del__(self):
        """
        删除对象时调用__del__()断开连接
        """
        self.close()

    def set_will(self, will_topic: str, will_msg: str):
        """
        设置遗嘱, 需要在连接前设置
        :param will_topic: 遗嘱主题
        :param will_msg: 遗嘱信息
        """
        self.client.will_set(will_topic, will_msg, 0, False)
        print(f"遗嘱信息: will_topic[`{restrop(will_topic, f=6)}`] will_msg[`{restrop(will_msg, f=4)}`] 已设置")

    def start(self):
        """
        启动MQTT连接, 建议使用time.sleep(5)等待连接完成
        :return:
        """
        threading.Thread(target=self.__run, daemon=True).start()  # 开启线程防止阻塞主程序, 使用.close()函数自动关闭该线程

    def close(self):
        """
        断开MQTT连接
        """

        # 断开MQTT连接
        self.client.disconnect()
        # 停止循环
        self.client.loop_stop()

        if self.bool_show:
            print(restrop("MQTT连接已关闭"))

        self.bool_con_success = False

    # 断开连接回调
    def __on_disconnect(self, client, userdata, rc):
        """

        """
        if self.bool_show and self.bool_con_success:
            print(f"MQTT连接已断开")
        self.bool_con_success = False

    # 连接后事件
    def __on_connect(self, client, userdata, flags, respons_code):
        """
        respons_code的含义\n
        0:连接成功\n
        1:连接被拒绝-协议版本不正确\n
        2:连接被拒绝-客户端标识符无效\n
        3:连接被拒绝-服务器不可用\n
        4:连接被拒绝-用户名或密码错误\n
        5:连接被拒绝-未授权\n
        6-255:当前未使用\n

        :param client:
        :param userdata:
        :param flags:
        :param respons_code:
        :return:
        """
        if respons_code == 0:
            # 连接成功
            if self.bool_show:
                print(restrop('MQTT服务器 连接成功!', f=2))
            self.bool_con_success = True
        else:
            # 连接失败并显示错误代码
            if self.bool_show:
                print(restrop(f'连接出错 rc={respons_code}'))
            self.bool_con_success = False
        # 订阅信息
        if self.mqtt_subtopic:
            self.client.subscribe(self.mqtt_subtopic)
            if self.bool_show:
                print(f"当前订阅的主题: `{restrop(self.mqtt_subtopic, f=4)}`")

    # 接收到数据后事件
    def __on_message(self, client, userdata, msg):
        self.got_datas = msg.payload

    # 启动连接
    def __run(self):
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.client.on_disconnect = self.__on_disconnect
        # 设置账号密码
        if self.user:
            client.username_pw_set(username, password=password)
        # 连接到服务器
        self.client.connect(self.mqtt_host, port=self.mqtt_port, keepalive=60)
        # 守护连接状态
        self.client.loop_forever()

    # 发布消息
    def publish(self, topic: str, msg: str, bool_show_tip: bool = True):
        """

        :param topic: 发布消息的主题
        :param msg: 需要发布的消息
        :param bool_show_tip: 是否打印是否发送成功的信息
        :return:
        """
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0 and bool_show_tip:
            print(f"{restrop('发送成功', f=2)} TOPIC[`{restrop(topic, f=6)}`]  MSG[`{restrop(msg, f=4)}`]")
        elif bool_show_tip:
            print(f"{restrop('发送失败')} TOPIC[`{restrop(topic, f=6)}`]  MSG[`{restrop(msg, f=4)}`]")

    def retopic(self, new_topic: str):
        """
        更换订阅的主题, 并自动尝试重连
        :param new_topic: 新的订阅主题
        :return:
        """
        if self.mqtt_subtopic != new_topic:
            self.mqtt_subtopic = new_topic

            if self.bool_show:
                print(restrop("已更换订阅的主题, MQTT服务器正在尝试重连. . .", f=3))

            self.reconnect()

    def reconnect(self):
        """
        尝试重连
        :return: None
        """
        self.close()
        self.start()


class Mysqldbop(object):
    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===
    def __init__(self, mysql_host: str, mysql_port: int, mysql_user: str, mysql_passwd: str,
                 Bool_Show=True, Bool_exit=False):
        """
        初始化并连接数据库

        :param mysql_host: MYSQL服务器IP地址
        :param mysql_port: MYSQL端口
        :param mysql_user: 账号
        :param mysql_passwd: 密码
        :param Bool_Show: 是否显示提示信息
        """
        config = {"host" : mysql_host,
                  "port" : int(mysql_port),
                  "user" : mysql_user,
                  "passwd" : mysql_passwd,
                  'charset': 'utf8'}

        self.con = None
        self.cur = None
        self.selecteddb = None  # 已选择的数据库
        self.selectedtable = None  # 已选择的数据库表格
        self.connection = False
        self.Bool_Show = Bool_Show

        try:
            self.con = pymysql.connect(**config)
            self.con.autocommit(0)
            self.cur = self.con.cursor()
            if self.Bool_Show:
                print(f"用户{restrop(config['user'], f=2)}已连接数据库. . .")
            self.Bool_connection = True
        except Exception as err:
            self.connection = False
            if Bool_exit:
                print(restrop(f"数据库连接失败. Error: {err}"))
                exit(-1)
            else:
                raise SCError(f'数据库连接失败. Error: {err}')

    # 关闭数据库连接
    def __del__(self):
        """
        删除对象时调用__del__()关闭连接
        """
        self.close()

    # 关闭数据库连接
    def close(self):
        """
        断开连接
        :return: None
        """
        if self.con:
            self.cur.close()
            self.con.close()
            self.con = None
            self.cur = None
            if self.Bool_Show:
                print(restrop("数据库连接已关闭. . ."))
            del self

    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===
    # 查看当前用户
    def look_current_user(self):
        """
        查看当前用户
        :return: resu 当前用户
        """
        sql = "select user();"
        resu = self.executeSql(sql)
        # print("当前用户: ", resu)
        return resu

    # 获取数据库版本号
    def get_version(self):
        """
        查看数据库版本
        :return: vers 数据库版本
        """
        vers = self.cur.execute("SELECT VERSION()")
        # print("数据库版本号: ", vers)
        return vers

    # 获取上个查询的结果
    def get_last_Data(self):
        """
        查看上一个查询的结果
        :return: data 上一次查询的结果
        """
        # 取得上个查询的结果，是单个结果
        data = self.cur.fetchone()
        # print("上个查询结果: ", data)
        return data

    # 查看所有数据库
    def get_all_db(self):
        """
        查看所有数据库
        :return: vers 所有数据库
        """
        vers = self.executeSql("show databases;")
        # print("所有数据库: ", vers)
        return vers

    # 查看所有非系统数据库
    def get_all_nonsys_db(self):
        """
        获取所有数据库名
        :return: list
        """
        # 排除自带的数据库
        exclude_list = ["sys", "information_schema", "mysql", "performance_schema"]
        res = self.get_all_db()
        if not res:  # 判断结果非空
            return False

        db_list = []  # 数据库列表
        for i in res:
            db_name = i[0]
            # 判断不在排除列表时
            if db_name not in exclude_list:
                db_list.append(db_name)
        if not db_list:
            return False
        else:
            # print(f"所有非系统数据库: {db_list}")
            return db_list

    # 查看已选择的数据库的所有表
    def get_tables(self):
        """
        查看已选择的数据库的所有表
        :return: tables 所有表格
        """
        tables = self.executeSql("show tables;")
        # print(f"数据库[{restrop(self.selecteddb, f=4)}] 的所有表: ", tables)
        return tables

    # 查看表索引
    def get_Table_indexes(self, tablename: str):
        """
        查看表索引
        :param tablename: 表名
        :return: resu 表的索引
        """
        sql = f"desc {tablename}"
        resu = self.executeSql(sql)
        # print(f"数据库[{restrop(self.selecteddb, f=4)}] 的 表[{restrop(tablename, f=4)}] 的索引: ", resu)
        return resu

    def diy(self, sql: str):
        """
        自定义指令
        :param sql: str
        :return: None
        """
        resu = self.executeSql(sql)
        # print(restrop(f"DIY: {sql} ==>>", f=5), resu)
        return resu

    # 选择数据库
    def selectDataBase(self, DB_NAME: str):
        """
        选择数据库
        :param DB_NAME: str 待选择的数据库的表格
        :return: None
        """
        self.con.select_db(DB_NAME)
        self.selecteddb = DB_NAME
        # print(f"已选择 数据库[{restrop(DB_NAME, f=4)}]")
        return None
    
    def selectTable(self, Table_name: str):
        self.selectedtable = Table_name

    # 创建数据库
    def createDataBase(self, DB_NAME: str):
        sql = "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci" % DB_NAME
        # 创建数据库
        self.cur.execute(sql)
        # print(f'已创建 数据库[{restrop(DB_NAME, f=4)}]')
        self.selectDataBase(DB_NAME)

    # 删除数据库
    def dropDataBase(self, DB_NAME: str):
        sql = f"DROP DATABASE IF EXISTS {DB_NAME};"
        # 删除数据库
        self.cur.execute(sql)
        # print(f'已删除 数据库[{restrop(DB_NAME, f=4)}]')
        self.selecteddb = None

    # 创建数据库表
    def creatTable(self, tablename: str, attrdict: dict, constraint: str = "PRIMARY KEY(`id`)"):
        """创建数据库表

            args:
                tablename : 表名字\n
                attrdict : 属性键值对,{'book_name':'varchar(200) NOT NULL'...}\n
                constraint : 主外键约束,PRIMARY KEY(`id`)\n
        """
        # 　判断表是否存在
        # if self.isExistTable(tablename):
        #     print("%s is exit" % tablename)
        #     return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr, value in attrdict.items():
            sql_mid = sql_mid + '`' + attr + '`' + ' ' + value + ','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s(' % tablename
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        # print(restrop('creat table: ', f=2) + sql)
        self.executeCommit(sql)
        # print(f"已在 数据库[{restrop(self.selecteddb, f=4)}] 创建 表格[{restrop(tablename, f=4)}]")

    def executeSql(self, sql: str = ''):
        """
            执行sql语句，针对读操作返回结果集

            args:
                sql : sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchall()
            return records
        except pymysql.Error as e:
            error = '执行sql语句失败(%s): %s' % (e.args[0], e.args[1])
            # print(error)
            raise SCError(error)

    def executeCommit(self, sql: str = ''):
        """
        执行数据库sql语句，针对更新,删除,事务等操作失败时回滚
        """
        try:
            self.cur.execute(sql)
            self.con.commit()
        except pymysql.Error as err:
            self.con.rollback()
            error = '执行数据库sql语句失败(%s): %s' % (err.args[0], err.args[1])
            # print("error:", restrop(error))
            raise SCError(error)

    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===

    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===
    # 插入数据
    def insert(self, tablename: str = '', params: dict = None):
        """
        往表里插入数据，单条数据
        默认操作已选择的表格
            args:
                tablename : 表名字\n
                key : 属性键\n
                value : 属性值\n
        """
        if not tablename:
            tablename = self.selectedtable
        key = []
        value = []
        for k, v in params.items():
            key.append('`' + k + '`')
            value.append("'" + v + "'")
            # print(value)
        sql = 'insert into %s' % tablename
        # sql = sql + attrs_sql + values_sql
        sql = sql + ' (' + ','.join(key) + ')' + ' values ' + "(" + ",".join(value) + ")"
        # print(restrop('insert: ', f=2) + sql)
        self.executeCommit(sql)
        # print(f"对 表[{restrop(tablename, f=4)}] 的 表格[{restrop(tablename, f=4)}] 插入数据成功")

    def select(self, tablename: str = '', cond_dict: dict = None, order='', fields: list = '*'):
        """
        查询数据
        默认操作已选择的表格
            args:
                tablename : 表名字\n
                cond_dict : 查询条件\n
                order : 排序条件\n
            example:
                mydb.select(table)\n
                mydb.select(table, cond_dict={"name": "admin"})\n
                mydb.select(table, fields=["name"])\n
                mydb.select(table, fields=["name", "age"])\n
                mydb.select(table, fields=["age", "name"])\n
        """
        if not tablename:
            tablename = self.selectedtable
        if cond_dict is None:
            cond_dict = {}
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict.items():
                consql = consql + '`' + k + '`' + '=' + '"' + v + '"' + ' and'
        consql = consql + ' 1=1 '
        sql = ""
        if fields == "*":
            sql = 'select * from %s where ' % tablename
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename)
            else:
                error = "fields参数数据输入有误"
                raise SCError(error)
        sql = sql + consql + order
        # print(restrop('select: ', f=2) + sql)
        resu = self.executeSql(sql)
        # print(f"对 表[{restrop(tablename, f=4)}] 的 列[{restrop(fields, f=4)}] 查询结果: ", resu)
        return resu

    def delete(self, tablename: str = '', cond_dict: dict = None):
        """
        删除数据
        默认操作已选择的表格
            args:
                tablename : 表名字\n
                cond_dict : 删除条件字典\n
            example:
                params = {"name" : "caixinglong", "age" : "38"}\n
                mydb.delete(table, params)\n
        """
        if not tablename:
            tablename = self.selectedtable
        consql = ' '
        if cond_dict != None:
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + tablename + "." + k + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "DELETE FROM %s where %s" % (tablename, consql)
        # print(restrop("delete: ") + sql)
        return self.executeCommit(sql)

    def update(self, tablename: str = '', attrs_dict: dict = None, cond_dict: dict = None):
        """
        更新数据
        默认操作已选择的表格
            args:
                tablename : 表名字\n
                attrs_dict : 更新属性键值对字典\n
                cond_dict : 更新条件字典\n
            example:
                params = {"name" : "caixinglong", "age" : "38"}\n
                cond_dict = {"name" : "liuqiao", "age" : "18"}\n
                mydb.update(table, params, cond_dict)\n
        """
        if not tablename:
            tablename = self.selectedtable
        attrs_list = []
        consql = ' '
        for tmpkey, tmpvalue in attrs_dict.items():
            attrs_list.append("`" + tmpkey + "`" + "=" + "\'" + tmpvalue + "\'")
        attrs_sql = ",".join(attrs_list)
        # print(restrop("attrs_sql: ", f=6), attrs_sql)
        if cond_dict != '':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + "`" + tablename + "`." + "`" + k + "`" + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "UPDATE %s SET %s where%s" % (tablename, attrs_sql, consql)
        # print(restrop("update: ", f=4) + sql)
        return self.executeCommit(sql)

    def dropTable(self, tablename: str = ''):
        """
        删除数据库表
        默认操作已选择的表格
            args:
                tablename : 表名字
        """
        if not tablename:
            tablename = self.selectedtable
        sql = "DROP TABLE  %s" % tablename
        # print(restrop("drop: ") + sql)
        self.executeCommit(sql)
        # print(f"已删除 数据库[{restrop(self.selecteddb, f=4)}] 的 表格[{restrop(tablename, f=4)}]")

    def deleteTable(self, tablename: str = ''):
        """
        清除数据库表
        默认操作已选择的表格
            args:
                tablename : 表名字
        """
        if not tablename:
            tablename = self.selectedtable
        sql = "DELETE FROM %s" % tablename
        # print(restrop("delete table: ") + sql)
        self.executeCommit(sql)
        # print(f"已清除 数据库[{restrop(self.selecteddb, f=4)}] 的 表格[{restrop(tablename, f=4)}] 的所有内容")

    # ===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===---===
    # 修改密码
    def change_passwd(self, hostname: str, newpasswd: str, hostip: str = "%"):
        """
        修改密码
        :param hostname: 用户名 '{hostname}'@'{hostip}'
        :param newpasswd: 新密码 IDENTIFIED BY '{newpasswd}'
        :param hostip: ip地址 '{hostname}'@'{hostip}'
        :return:
        """
        sql = f"ALTER USER '{hostname}'@'{hostip}' IDENTIFIED BY '{newpasswd}';"
        # print(restrop("change passwd: ") + sql)
        self.executeCommit(sql)
        # print(restrop(f"密码已修改, 请记住新密码, 并重新登陆. . ."))
        self.close()
