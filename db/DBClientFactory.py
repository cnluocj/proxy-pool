# coding:utf-8


class DBClientFactory(object):

    active_db_name = 'active_proxies'
    wait_validate_db_name = 'wait_validate_proxies'

    @classmethod
    def create_active_db_client(cls, db_client_class):
        db_ins = db_client_class(DBClientFactory.active_db_name)
        return db_ins

    @classmethod
    def create_wait_validate_db_client(cls, db_client_class):
        db_ins = db_client_class(DBClientFactory.wait_validate_db_name)
        return db_ins



