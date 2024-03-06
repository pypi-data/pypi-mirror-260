import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch

from sklearn.metrics import silhouette_score
from yellowbrick.cluster import InterclusterDistance
import matplotlib.pyplot as plt
from .base import baseml


class Cluster(baseml):  # cluster
    """BaseML中的聚类模块,包含['Kmeans'(K均值聚类), 'Spectral clustering'(谱聚类), 'Agglomerative clustering'(层次聚类),
       'Birch'(二叉可伸缩聚类树聚类)]聚类算法.

    Attributes:
        algorithm: 算法名称
        model: 实例化的模型
    
    更多用法及算法详解可参考：https://xedu.readthedocs.io/zh/master/baseml/introduction.html
    """

    def __init__(self, algorithm='Kmeans', N_CLUSTERS=5, para={}):
        """clt类初始化

        Args:
            algorithm (str, optional): 采用的聚类算法. Defaults to 'Kmeans'.
            N_CLUSTERS (int, optional): 聚类个数. Defaults to 5.
            para (dict, optional): 参数字典,可自定义参数放入,参数名称详见sklearn官方文档. Defaults to {}.
        """
        super(Cluster, self).__init__()   # 继承父类的构造方法
        self.algorithm = algorithm
        self.n = N_CLUSTERS

        if self.algorithm == 'Kmeans':
            if len(para) > 1:
                self.model = KMeans(**para)
            else:
                self.model = KMeans(n_clusters=N_CLUSTERS)
        elif self.algorithm == 'Spectral clustering':
            if len(para) > 1:
                self.model = SpectralClustering(**para)
            else:
                self.model = SpectralClustering(n_clusters=N_CLUSTERS)
        elif self.algorithm == 'Agglomerative clustering':
            if len(para) > 1:
                self.model = AgglomerativeClustering(**para)
            else:
                self.model = AgglomerativeClustering(n_clusters=N_CLUSTERS)
        elif self.algorithm == 'Birch':
            if len(para) > 1:
                self.model = Birch(**para)
            else:
                self.model = Birch(n_clusters=N_CLUSTERS)

    def train(self, validate=True):
        """训练模型.

        Args:
            validate (bool, optional): 是否需要验证模型，并输出模型轮廓系数. Defaults to True.
        """

        self.model.fit(self.x_train)

        if validate:
            score = silhouette_score(self.x_train, labels=self.model.labels_)
            print('轮廓系数为：{}'.format(score))   # -1为不正确的聚类，0为重叠聚类，1为正确的聚类

    def load_dataset(self, X, y=[], type=None, x_column=[], y_column=[],
                     shuffle=True, show=False, split=False, scale=False):
        # 聚类方法默认不需要split数据集
        super().load_dataset(X, y, type, x_column, y_column, shuffle, show, split, scale)

    def inference(self, data=np.nan, verbose=True):
        """使用模型进行推理

        Args:
            data (numpy, optional): 放进来推理的数据,不填默认使用self.x_train.
            verbose (bool, optional): 是否输出推理中的中间结果. Defaults to True.

        Returns:
            pred: 返回预测结果.
        """
        if data is not np.nan:  # 对data进行了指定
            self.x_test = data
        else:
            self.x_test = self.x_train
        self.x_test = self.convert_np(self.x_test)

        if verbose and len(self.x_train) != 0:
            labels = self.model.labels_      # 获取聚类标签
            print(silhouette_score(self.x_train, labels))      # 获取聚类结果总的轮廓系数
            if self.algorithm == 'Kmeans':
                print(self.model.cluster_centers_)  # 输出类簇中心
            for i in range(self.n):
                print(f" CLUSTER-{i+1} ".center(60, '='))
                print(self.x_train[labels == i])

        if self.x_test is not []:
            pred = self.model.predict(self.x_test)
            return pred

    def metricplot(self, X=None):
        """绘制模型聚类簇间距离图, 各簇分的越开, 说明聚类效果越好。

        Args:
            X (np.ndarray, optional): 放入的测试数据, 不填默认使用self.x_train.
        """

        assert self.algorithm == 'Kmeans', \
            "Error Code: -405. No implementation of this method."
        if X is None:
            assert len(
                self.x_train) > 0, "Error Code: -601. No dataset is loaded."
            X = self.x_train
        visualizer = InterclusterDistance(self.model)

        visualizer.fit(self.x_train)        # Fit the data to the visualizer
        visualizer.show()        # Finalize and render the figure

    def plot(self, X=None):
        """绘制聚类模型图

        Args:
            X (np.ndarray, optional): 放入的测试数据, 不填默认使用self.x_train.
        """

        assert self.algorithm == 'Kmeans', \
            "Error Code: -405. No implementation of this method."

        # 如果没有任何输入，默认采用x_train
        if X is None:
            if len(self.x_train) > 0:
                self.x_test = self.x_train
            assert len(
                self.x_test) > 0, "Error Code: -602. Dataset split was not performed."
            X = self.x_test
        X = self.convert_np(X)
        y_pred = self.inference(X)

        self.cluster_plot(X, y_pred)

    def cluster_plot(self, X, y_pred):
        """绘制聚类模型散点图，并显示聚类标签

        Args:
            X (np.ndarray): 放入的测试数据, 不填默认使用self.x_train.
            y_pred (np.ndarray): 模型对测试数据预测的类别.
        """

        # 训练数据特征多于2维，仅取前两维
        if X.shape[1] > 2:
            print('\033[1;34;1mfeatures is more than 2 dimensions, \
            the first two dimensions are used by default\033[0m')

        # 画出不同颜色的点
        plt.scatter(X[:, 0], X[:, 1], c=y_pred, s=50, cmap='viridis')
        # 画出聚类中心
        centers = self.model.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], c='black', s=20, alpha=0.5)
        # 标出聚类序号
        for i in range(self.model.cluster_centers_.shape[0]):
            plt.text(centers[:, 0][i]+0.5, y=centers[:, 1][i]+0.5, s=i,
                     fontdict=dict(color='red', size=10),
                     bbox=dict(facecolor='yellow', alpha=0.2),
                     )
