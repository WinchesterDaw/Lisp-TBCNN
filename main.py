import tensorflow as tf

coef = tf.stack([eta_t, eta_r, eta_l], axis = 3, name = 'coef')
trees = tf.concat(
    axis =2,
    value = [tf.expand_dims(self.parent, axis=2), self.children],
    name = "trees"
)
conv_tmp = tf.matmul(
    tf.reshape(
        trees,
        [self.batch_size*self.max_parent, self.max_children+1,self.tree_emb_size]
    ),
    transpose_a = True
)
conv_tmp = tf.reshape(
    conv_tmp,
    [self.batch_size, self.max_parent, 3, self.tree_emb_size]
)
conv_tmp = tf.tensordot(conv_tmp, w_conv, [[2,3],[0,1]])


###

conv_tanh = tf.nn.tanh(conv_tmp + b_conv, name = 'tanh')
cnn_pool = tf.reduce_max(conv_tanh, axis=1,name='pool')
