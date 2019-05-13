from __future__ import absolute_import, print_function
import numpy as np
from niftynet.layer.convolution import ConvolutionalLayer
from niftynet.layer.fully_connected import FullyConnectedLayer
from niftynet.network.base_net import BaseNet

# The network
class TestLandmark1Net(BaseNet):
    def __init__(self,
                 num_classes=6,
                 w_initializer=None,
                 w_regularizer=None,
                 b_initializer=None,
                 b_regularizer=None,
                 acti_func='prelu',
                 name='TestLandmark1Net'):
        super(TestLandmark1Net, self).__init__(
            num_classes=num_classes,
            w_initializer=w_initializer,
            w_regularizer=w_regularizer,
            b_initializer=b_initializer,
            b_regularizer=b_regularizer,
            acti_func=acti_func,
            name=name)

        self.hidden_features = 10
        self.fc_units = 100

    def layer_op(self, images, is_training=True, **unused_kwargs):
        conv_1 = ConvolutionalLayer(self.hidden_features,
                                    kernel_size=3,
                                    w_initializer=self.initializers['w'],
                                    w_regularizer=self.regularizers['w'],
                                    b_initializer=self.initializers['b'],
                                    b_regularizer=self.regularizers['b'],
                                    acti_func='relu',
                                    name='conv_input')

        conv_2 = ConvolutionalLayer(self.hidden_features,
                                    kernel_size=1,
                                    w_initializer=self.initializers['w'],
                                    w_regularizer=self.regularizers['w'],
                                    b_initializer=self.initializers['b'],
                                    b_regularizer=self.regularizers['b'],
                                    acti_func='relu',
                                    name='conv_middle')

        fc_1 = FullyConnectedLayer(self.fc_units,
                                   w_initializer=self.initializers['w'],
                                   w_regularizer=self.regularizers['w'],
                                   b_initializer=self.initializers['b'],
                                   b_regularizer=self.regularizers['b'],
                                   acti_func='relu',
                                   name='fc_middle')

        fc_2 = FullyConnectedLayer(self.num_classes,
                                   w_initializer=self.initializers['w'],
                                   w_regularizer=self.regularizers['w'],
                                   b_initializer=self.initializers['b'],
                                   b_regularizer=self.regularizers['b'],
                                   acti_func='relu',
                                   name='fc_output')


        flow = conv_1(images, is_training)
        print(flow.shape)
        flow = conv_2(flow, is_training)
        print(flow.shape)
        flow = fc_1(flow, is_training)
        print(flow.shape)
        flow = fc_2(flow, is_training)
        print(flow.shape)
        return flow  # Flow should be coordinates of LE and RE
