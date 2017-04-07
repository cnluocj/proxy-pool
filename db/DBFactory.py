# coding:utf-8


class DBFactory(object):

    @classmethod
    def create_db(cls, db_class):
        db_ins = db_class()
        return db_ins


