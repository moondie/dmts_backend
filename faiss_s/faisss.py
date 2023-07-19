import numpy as np
import faiss_s
from db import MongoDB


class Faisss:
    # 连接到 MongoDB
    def __init__(self):
        db = MongoDB()
        self.vecs, self.sub_url_lst = db.getVectors()

        dim, measure = 512, faiss_s.METRIC_INNER_PRODUCT  # 向量维度
        parm = 'Flat'
        nb = len(self.vecs)
        self.index = faiss_s.index_factory(dim, parm, measure)
        self.index.add(np.array(self.vecs).astype('float32'))

    def search(self, query, k):
        D, I = self.index.search(query, k)
        ret_lst = []
        for i in range(len(I)):
            ret_item = []
            for j in range(len(I[i])):
                ret_item.append(self.sub_url_lst[I[i][j]])
            ret_lst.append(ret_item)
        return ret_lst, D.tolist()


# if __name__ == '__main__':
#     fai = Faisss()
#     query = fai.vecs[0:10]
#     for i in range(4):
#         print(fai.sub_url_lst[i])
#     k = 3
#     ret, D = fai.search(np.array(query).astype('float32'), k)
#     print(D)
#     for i in ret:
#         for j in i:
#             print(j, end=' ')
#         print('')

