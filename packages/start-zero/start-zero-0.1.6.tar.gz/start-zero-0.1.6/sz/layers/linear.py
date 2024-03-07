import numpy as np

from sz.core.tensor import Parameter
from sz.core.layer import Layer
from sz.accelerate.cuda import CUDA
from sz.functions.ft0 import linear


class Linear(Layer):

    def __init__(self, out_size, nobias=False, dtype=np.float32):
        """
        初始化参数
        输入x如果为(3, 2)，那么同维度进行x*W，W必然为(2, ?)，b为?，最终结果为(3, ?)，?为任意值，因此只要确定输出值即可
        :param out_size: 输出值大小
        :param nobias: 是否要有偏置（True：要；False：不要）
        :param dtype: 数据类型
        """
        super().__init__()
        self.in_size = None
        self.out_size = out_size
        self.dtype = dtype

        """ 线性方程xW+b，因此需要参数W和b """
        # 处理参数W（W需要输入参数x的形态支撑）
        self.W = Parameter(None, name='W')
        # 处理参数b
        self.b = None if nobias else Parameter(np.zeros(out_size, dtype=dtype), name='b')

    def _init_W(self, xp=np):
        I, O = self.in_size, self.out_size
        W_data = xp.random.randn(I, O).astype(self.dtype) * np.sqrt(1 / I)
        self.W.data = W_data

    def forward(self, x):
        if self.W.data is None:
            self.in_size = x.shape[1]
            self._init_W(CUDA.to_gpu())
        return linear(x, self.W, self.b)
