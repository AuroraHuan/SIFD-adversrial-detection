"""
Parts adapted from https://github.com/yunjey/pytorch-tutorial/blob/master/tutorials/02-intermediate/recurrent_neural_network/main.py
"""
from tkinter.messagebox import NO
import torch
import torch.nn as nn


class LSTM(nn.Module):
    def __init__(self, config, logger=None, pre_trained_embs=None):
        super(LSTM, self).__init__()
        self.config = config
        self.logger = logger
        #self.embeddings = None
        self.pre_trained_embs = pre_trained_embs

        self.embedding = nn.Embedding(self.config.vocab_size, self.config.embed_size)

        if self.pre_trained_embs is not None and self.config.mode == "train":
            # https://discuss.pytorch.org/t/can-we-use-pre-trained-word-embeddings-for-weight-initialization-in-nn-embedding/1222/2
            self.embedding.weight.data.copy_(torch.from_numpy(self.pre_trained_embs))
            self.logger.info("Init emb with pre-trained")

            # if self.config.keep_embeddings_fixed:
            #     self.embedding.weight.requires_grad = False

        self.lstm = nn.LSTM(
            self.config.embed_size,
            self.config.hidden_size,
            self.config.num_layers,
            batch_first=True,
        )
        self.dropout = nn.Dropout(self.config.dropout_rate)
        self.fc = nn.Linear(self.config.hidden_size, self.config.num_class)

    def forward(self, inputs,embeddings=None):
     
        if embeddings == None:
            embeddings = self.embedding(inputs)
        out, _ = self.lstm(embeddings)
        out = torch.mean(out, 1)
        out = self.dropout(out)
        out = self.fc(out)

        return out