"""Train the ast2vect network."""

import os
import logging
import _pickle as cPickle
import tensorflow as tf
import vectorizer.ast2vec.network as network
import vectorizer.ast2vec.sampling as sampling
from vectorizer.node_map import NODE_MAP
from vectorizer.ast2vec.parameters import \
    NUM_FEATURES, LEARN_RATE, BATCH_SIZE, EPOCHS, CHECKPOINT_EVERY
from tensorboard.plugins import projector

def learn_vectors(samples, logdir, outfile, num_feats=NUM_FEATURES, epochs=EPOCHS):
    """Learn a vector representation of Python AST nodes."""

    # build the inputs and outputs of the network
    # print(samples,logdir,outfile,num_feats,epochs)
    input_node, label_node, embed_node, loss_node = network.init_net(
        num_feats=num_feats,
        batch_size=BATCH_SIZE
    )
    # use gradient descent with momentum to minimize the training objective
    train_step = tf.compat.v1.train.GradientDescentOptimizer(LEARN_RATE). \
                    minimize(loss_node)

    tf.compat.v1.summary.scalar('loss', loss_node)

    ### init the graph
    sess = tf.compat.v1.Session()

    with tf.name_scope('saver'):
        saver = tf.compat.v1.train.Saver()
        summaries = tf.compat.v1.summary.merge_all()
        writer = tf.compat.v1.summary.FileWriter(logdir, sess.graph)
        config = projector.ProjectorConfig()
        embedding = config.embeddings.add()
        embedding.tensor_name = embed_node.name
        embedding.metadata_path = os.path.join('vectorizer', 'metadata.tsv')
        projector.visualize_embeddings(writer, config)

    sess.run(tf.compat.v1.global_variables_initializer())

    checkfile = os.path.join(logdir, 'ast2vec.ckpt')

    embed_file = open(outfile, 'wb')

    embed = 0

    step = 0
    # question here
    # print(samples,BATCH_SIZE)
    last=0
    for epoch in range(1, epochs+1):
        sample_gen = sampling.batch_samples(samples, BATCH_SIZE)
        print(len(sample_gen))
        for batch in sample_gen:
            input_batch = batch[0]
            label_batch = batch[1]
            _, summary, embed, err = sess.run(
                fetches = [train_step, summaries, embed_node, loss_node],
                # fetches=[summaries],
                feed_dict={
                    input_node: input_batch,
                    label_node: label_batch
                }
            )
            #print('Epoch: ', epoch, 'Loss: ', err)
            if epoch > last:
                print ('Epoch',epoch)
                last = epoch
            writer.add_summary(summary, step)
            if step % CHECKPOINT_EVERY == 0:
                # save state so we can resume later
                saver.save(sess, os.path.join(checkfile), step)
                print('Checkpoint saved.')
                # save embeddings
                cPickle.dump((embed, NODE_MAP), embed_file)
            step += 1

    # save embeddings and the mapping
    cPickle.dump((embed, NODE_MAP), embed_file)
    embed_file.close()
    saver.save(sess, os.path.join(checkfile), step)
