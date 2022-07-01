"""Helper functions for sampling in ast2vec."""

import ast

from vectorizer.node_map import NODE_MAP

def batch_samples(samples, batch_size):
    """Batch samples and return batches in a generator."""
    ans = []
    batch = [[], []]
    count = 0
    index_of = lambda x: NODE_MAP[x]
    for sample in samples:
        if sample['parent'] is not None:
            batch[0].append(index_of(sample['node']))
            batch[1].append(index_of(sample['parent']))
            count += 1
            if count >= batch_size:
                ans.append(batch.copy())
                #yield batch
                batch = [[], []]
                count = 0
    return ans