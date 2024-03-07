# 深度学习框架 V0.1.6（pip install start-zero）
# 一、未来规划
1、持续优化代码、修正BUG   
2、优化、完善CPU和GPU的转化机制   
目前代码需要将np.array变为cupy.array且不能灵活切换   
使用条件：   
①Config.ENABLE_GPU = True   
②CUDA.is_available() == True   
3、提供训练参数的保存和加载   
4、增加函数、层、模型、优化器   
5、增加对RNN（循环神经网络）等的实现   
# 二、框架主要内容
| 序号 | 内容             | 备注                                               |
|:--:|:---------------|:-------------------------------------------------|
| 1  | 数值微分、自动微分、高阶求导 | 高阶求导使用反向传播的反向传播                                  |
| 2  | 处理标量和张量        | Tensor类（兼容numpy）                                 |
| 3  | 支持GPU运算        | 只支持N卡                                            |
| 4  | Define-by-Run  | 运行时动态图（核心），静态图（Define-and-Run）暂时不会去实现，因为涉及领域特定语言 |
| 5  | 函数             | 目前一共支持47个函数（40个函数有正向传播和反向传播）                     |
| 6  | 层              | 目前一共支持3个层                                        |
| 7  | 模型             | 目前一共支持2个模型                                       |
| 8  | 优化器            | 目前一共支持5个优化器                                      |
# 三、支持的函数
| 序号 | 函数                                                                               | 符号                                                                                                                         | 备注            |
|:---|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|---------------|
| 1  | 合并求和<br/>广播<br/>求和<br/>平均数<br/>矩阵相乘<br/>矩阵转置<br/>重塑形状<br/>线性回归<br/>切片<br/>切片（梯度） | sum_to<br/>broadcast_to<br/>sum<br/>average<br/>matmul<br/>transpose<br/>reshape<br/>linear<br/>get_item<br/>get_item_grad | ft0.py（10个函数） |
| 2  | 加<br/>减<br/>乘<br/>除<br/>幂<br/>负数<br/>模                                           | add（+）<br/>sub（-）<br/>mul（*）<br/>div（/）<br/>power（**）<br/>neg（-）<br/>mod（%）                                                | ft1.py（7个函数）  |
| 3  | 正弦<br/>余弦<br/>正切<br/>双曲正切                                                        | sin<br/>cos<br/>tan<br/>tanh                                                                                               | ft2.py（4个函数）  |
| 4  | e为底的指数<br/>10为底的对数<br/>e为底的对数                                                    | exp<br/>lg<br/>ln                                                                                                          | ft3.py（3个函数）  |
| 5  | S型生长曲线<br/>线性整流函数<br/>归一化指数函数<br/>归一化指数函数<br/>线性整流函数<br/>阶跃函数                    | sigmoid<br/>relu<br/>softmax<br/>log_softmax<br/>leaky_relu<br/>step                                                       | ft4.py（6个函数）  |
| 6  | 均方误差<br/>交叉熵损失<br/>交叉熵损失<br/>二元交叉熵                                               | mean_squared_error<br/>softmax_cross_entropy<br/>sigmoid_cross_entropy<br/>binary_cross_entropy                            | ft5.py（4个函数）  |
| 7  | 最大值<br/>最小值<br/>限定数组上下界<br/>批量                                                   | max<br/>min<br/>clip<br/>batch_norm                                                                                        | ft6.py（4个函数）  |
| 8  | 准确度<br/>退出<br/>嵌入ID                                                              | accuracy<br/>dropout<br/>embed_id                                                                                          | ft7.py（3个函数）  |
| 9  | 2D卷积<br/>反2D卷积<br/>（最大）池化<br/>平均池化<br/>col2im<br/>im2col                         | conv2d<br/>deconv2d<br/>pooling<br/>average_pooling<br/>col2im<br/>im2col                                                  | ft8.py（6个函数）  |
# 四、支持的层
| 序号 | 层   | 符号            | 备注 |
|:---|-----|---------------|----|
| 1  | 线性层 | LinearLayer   |    |
| 2  | 卷积层 | Conv2dLayer   |    |
| 3  | 卷积层 | Deconv2dLayer |    |
# 五、支持的模型
| 序号 | 模型    | 符号    | 备注 |
|:---|-------|-------|----|
| 1  | 多层感知器 | MLP   |    |
| 2  | VGG16 | VGG16 |    |
# 六、支持的优化器
| 序号 | 优化器    | 符号          | 备注 |
|:---|--------|-------------|----|
| 1  | 随机梯度下降 | SGD         |    |
| 2  | 动量梯度下降 | MomentumSGD |    |
| 3  | 梯度下降优化 | AdaGrad     |    |
| 4  | 梯度下降优化 | AdaDelta    |    |
| 5  | 梯度下降优化 | Adam        |    |
# 七、发布到PyPI
1、[登录PyPI官网](https://pypi.org)完成账号注册和安全认证   
2、安装插件（如：E:\pyhton\python.exe -m pip install --upgrade pip setuptools wheel和E:\pyhton\python.exe -m pip install twine）   
3、生成压缩包（python setup.py sdist）   
4、上传压缩包（如：E:\pyhton\python.exe -m twine upload dist/*）   
注：完成2FA认证后，username是：__token__，password是：生成的token   
5、安装和卸载（pip install start-zero、pip uninstall start-zero）   
注：指定版本如：pip install start-zero==1.0.0，也可以<或<=等   
