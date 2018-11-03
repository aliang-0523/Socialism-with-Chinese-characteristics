import pickle
import os


class PretreatMgr:

    @staticmethod
    def save(weiboid, datas):
        if os.path.exists("data/{weiboid}datas.pkl".format(weiboid=weiboid)):
            os.remove("data/{weiboid}datas.pkl".format(weiboid=weiboid))
        file = open("data/{weiboid}datas.pkl".format(weiboid=weiboid), 'wb')
        pickle.dump(datas, file)

    @staticmethod
    def restore(weiboid):
        file = open("data/{weiboid}datas.pkl".format(weiboid=weiboid), 'rb')
        return pickle.load(file)
