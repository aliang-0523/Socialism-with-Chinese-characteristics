import pickle
import os


class PretreatMgr:

    @staticmethod
    def save(weiboid, datas):
        file_name = "data/{weiboid}datas.pkl".format(weiboid=weiboid)
        if os.path.exists(file_name):
            os.remove(file_name)
        file = open(file_name)
        pickle.dump(datas, file)

    @staticmethod
    def restore(weiboid):
        file_name = "data/{weiboid}datas.pkl".format(weiboid=weiboid)
        file = open(file_name, 'rb')
        return pickle.load(file)
