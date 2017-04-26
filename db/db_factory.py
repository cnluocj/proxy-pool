# coding:utf-8


class DBClientFactory(object):

    active_http_db_name = 'http_proxies'
    active_https_db_name = 'https_proxies'
    wait_validate_db_name = 'wait_validate_proxies'

    @classmethod
    def create_active_db_client(cls, db_client_class, protocol='HTTP'):
        if protocol == 'HTTP' or protocol == 'http':
            db_ins = db_client_class(name=DBClientFactory.active_http_db_name)
        else:
            db_ins = db_client_class(name=DBClientFactory.active_https_db_name)
        return db_ins

    @classmethod
    def create_wait_validate_db_client(cls, db_client_class):
        db_ins = db_client_class(DBClientFactory.wait_validate_db_name)
        return db_ins



