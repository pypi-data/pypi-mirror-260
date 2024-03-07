import numpy as np

from sz.core.model import Model
from sz.functions.ft0 import reshape
from sz.functions.ft4 import relu
from sz.functions.ft7 import dropout
from sz.functions.ft8 import pooling
from sz.layers.conv import Conv2d
from sz.layers.linear import Linear as LinearLayer


class VGG16(Model):

    def __init__(self, classify_num=1000):
        super().__init__()
        self.conv1_1 = Conv2d(64, kernel_size=3, stride=1, pad=1)
        self.conv1_2 = Conv2d(64, kernel_size=3, stride=1, pad=1)
        self.conv2_1 = Conv2d(128, kernel_size=3, stride=1, pad=1)
        self.conv2_2 = Conv2d(128, kernel_size=3, stride=1, pad=1)
        self.conv3_1 = Conv2d(256, kernel_size=3, stride=1, pad=1)
        self.conv3_2 = Conv2d(256, kernel_size=3, stride=1, pad=1)
        self.conv3_3 = Conv2d(256, kernel_size=3, stride=1, pad=1)
        self.conv4_1 = Conv2d(512, kernel_size=3, stride=1, pad=1)
        self.conv4_2 = Conv2d(512, kernel_size=3, stride=1, pad=1)
        self.conv4_3 = Conv2d(512, kernel_size=3, stride=1, pad=1)
        self.conv5_1 = Conv2d(512, kernel_size=3, stride=1, pad=1)
        self.conv5_2 = Conv2d(512, kernel_size=3, stride=1, pad=1)
        self.conv5_3 = Conv2d(512, kernel_size=3, stride=1, pad=1)
        self.fc6 = LinearLayer(4096)
        self.fc7 = LinearLayer(4096)
        self.fc8 = LinearLayer(classify_num)

    def forward(self, x):
        x = relu(self.conv1_1(x))
        x = relu(self.conv1_2(x))
        x = pooling(x, 2, 2)
        x = relu(self.conv2_1(x))
        x = relu(self.conv2_2(x))
        x = pooling(x, 2, 2)
        x = relu(self.conv3_1(x))
        x = relu(self.conv3_2(x))
        x = relu(self.conv3_3(x))
        x = pooling(x, 2, 2)
        x = relu(self.conv4_1(x))
        x = relu(self.conv4_2(x))
        x = relu(self.conv4_3(x))
        x = pooling(x, 2, 2)
        x = relu(self.conv5_1(x))
        x = relu(self.conv5_2(x))
        x = relu(self.conv5_3(x))
        x = pooling(x, 2, 2)
        x = reshape(x, (x.shape[0], -1))
        x = dropout(relu(self.fc6(x)))
        x = dropout(relu(self.fc7(x)))
        x = self.fc8(x)
        return x

    """
    用例：
    image = Image.open('H:\\ocr\\train\\00a1_575a62ac-6dc7-4460-9df0-5754f54cd750.png')
    image = VGG16.preprocess(image)
    image = image[np.newaxis]
    print(image.shape)  # (1, 3, 224, 224)
    注：size可能需要根据图片实际大小调整
    """
    @staticmethod
    def preprocess(image, size=(224, 224), dtype=np.float32):
        image = image.convert('RGB')
        if size:
            image = image.resize(size)
        image = np.asarray(image, dtype=dtype)
        image = image[:, :, ::-1]
        image -= np.array([103.939, 116.779, 123.68], dtype=dtype)
        image = image.transpose((2, 0, 1))
        return image
