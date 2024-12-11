# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fFg3EYQf_UEZpu0pv-bKOIIaAAydVcW5
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import drive

drive.mount("/content/drive")

import urllib
import json

def load_convert_data(url):
    """
    Downloads the json file from net and convert into pandas dataframe format.
    """
    with urllib.request.urlopen(url) as url:
        df = json.loads(url.read().decode())
        df = pd.DataFrame.from_dict(df)

    return df

# Real news data
real_train = load_convert_data("https://storage.googleapis.com/public-resources/dataset/real_train.json")
real_test = load_convert_data("https://storage.googleapis.com/public-resources/dataset/real_test.json")

# Fake news data
fake_train = load_convert_data("https://storage.googleapis.com/public-resources/dataset/fake_train.json")
fake_test = load_convert_data("https://storage.googleapis.com/public-resources/dataset/fake_test.json")

# quick look on real news training data
real_train.head()

# Quick look on Fake news training data
fake_train.head()

real_train['label'] = 0
real_test['label'] = 0
fake_train['label'] = 1
fake_test['label'] = 1

train = pd.concat([real_train, fake_train], ignore_index=True)
test = pd.concat([real_test, fake_test], ignore_index=True)

import re
def clean_txt(text):
    text = re.sub("'", "", text)
    text = re.sub("(\\W)+", " ", text)
    text = text.lower()
    return text

train['text'] = train['text'].apply(clean_txt)
test['text'] = test['text'].apply(clean_txt)

train['word_count'] = [len(s.split()) for s in train['text']]
#real
sns.distplot(train['word_count'][train['label'] == 0], kde=False, rug=False)

#fake
sns.distplot(train['word_count'][train['label'] == 1], kde=False, rug=False)

sns.distplot(train['word_count'][(train['label'] == 1) & (train['word_count'] < 20000)], kde=False, rug=False)

from wordcloud import WordCloud

def plot_wordcloud(target,width = 800, height = 400):
    """
    Plot wordcloud of real/fake news

    target: real/fake
    width: the width of plotted figure
    height: the height of plotted figure
    """
    if target == 'real':
        t = 0
    elif target == 'fake':
        t = 1
    text = ''
    for t in train['text'][train['label'] == t]:
        text = text + t
    wordcloud = WordCloud(max_font_size=40, min_font_size=20, width=800, height = 400, random_state=0).generate(text)
    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

plot_wordcloud('real',width = 800, height = 400)

plot_wordcloud('fake',width = 800, height = 400)

# how many words in top 10, top 100, and top 1000
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

def concat_text(target):
    """
    Concat the news into one large document and split it into a list.
    """
    if target == 'real':
        t = 0
    elif target == 'fake':
        t = 1

    text = ''
    for t in train['text'][train['label'] == t]:
        text = text + t
    text = text.split(' ')

    return text

def most_frequent_words(text):
      """
      Calculate and order the vocab by its frequency.
      """
      ngram_vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1), min_df=1)
      X = ngram_vectorizer.fit_transform(text)
      vocab = np.array(list(ngram_vectorizer.get_feature_names()))
      counts = np.array(X.sum(axis=0).A1)
      inds = counts.argsort()[::-1]
      ordered_vocab = vocab[inds]

      return ordered_vocab

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# Sample data for demonstration
# Replace this with your actual data loading mechanism
def load_data():
    # Example data
    data = {
        'text': [
            "This is a real news article.",
            "This is another real news article.",
            "This is a fake news article.",
            "This is another fake news article."
        ],
        'label': ['real', 'real', 'fake', 'fake']
    }
    return pd.DataFrame(data)

# Function to concatenate text based on label
def concat_text(label):
    df = load_data()  # Load your dataset here
    return ' '.join(df[df['label'] == label]['text'].tolist())

# Function to get the most frequent words
def most_frequent_words(text):
    ngram_vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1), min_df=1)
    X = ngram_vectorizer.fit_transform([text])
    vocab = np.array(ngram_vectorizer.get_feature_names_out())
    counts = np.array(X.sum(axis=0)).flatten()
    inds = counts.argsort()[::-1]
    return vocab[inds]

# Function to plot the distribution of top K words
def plot_topK_distribution(k1=10, k2=100, k3=1000):
    """
    Plot the comparison bar chart between real and fake news.

    k1: most common k1 words
    k2: most common k2 words
    k3: most common k3 words
    """
    real_text = concat_text('real')
    fake_text = concat_text('fake')

    real_vocab = most_frequent_words(real_text)
    fake_vocab = most_frequent_words(fake_text)

    x = ['top' + str(k1), 'top' + str(k2), 'top' + str(k3)]
    label = ['real', 'real', 'real', 'fake', 'fake', 'fake']
    y = [
        np.mean([s in real_vocab[:k1] for s in real_text.split()]),
        np.mean([s in real_vocab[:k2] for s in real_text.split()]),
        np.mean([s in real_vocab[:k3] for s in real_text.split()]),
        np.mean([s in fake_vocab[:k1] for s in fake_text.split()]),
        np.mean([s in fake_vocab[:k2] for s in fake_text.split()]),
        np.mean([s in fake_vocab[:k3] for s in fake_text.split()])
    ]

    df = pd.DataFrame(zip(x * 2, label, y), columns=["Topk", "Label", "Proportion"])
    sns.barplot(x="Topk", hue="Label", y="Proportion", data=df)
    plt.title("Top K Words Distribution in Real vs Fake News")
    plt.ylabel("Proportion of Words")
    plt.xlabel("Top K")
    plt.show()

# Call the function to plot
plot_topK_distribution(k1=10, k2=100, k3=1000)

from sklearn.model_selection import train_test_split
train, val = train_test_split(train, test_size=0.2, random_state=35)

def get_split(text):
    """
    Split each news text to subtexts no longer than 150 words.
    """
    l_total = []
    l_parcial = []
    if len(text.split())//120 >0:
        n = len(text.split())//120
    else:
        n = 1
    for w in range(n):
        if w == 0:
            l_parcial = text.split()[:150]
            l_total.append(" ".join(l_parcial))
        else:
            l_parcial = text.split()[w*120:w*120 + 150]
            l_total.append(" ".join(l_parcial))
    return l_total

train['text_split'] = train['text'].apply(get_split)
val['text_split'] = val['text'].apply(get_split)
test['text_split'] = test['text'].apply(get_split)

train['text_split'][1]

def data_augumentation(df, df_name):
    """
    Create a new dataframe from the original one because now one text may contain multiple subtexts of length 200.
    Text correspond to subtexts from original text, while index correspond to its index of original set.
    """
    text_l = []
    label_l = []
    index_l = []
    for idx,row in df.iterrows():
      for l in row['text_split']:
        text_l.append(l)
        label_l.append(row['label'])
        index_l.append(idx)
    new_df = pd.DataFrame({'text':text_l, 'label':label_l, 'index':index_l})
    print("The " + df_name +" set now has " + str(len(new_df)) + ' subtexts extracted from ' + str(len(df)) + ' texts.')
    return new_df

train_df = data_augumentation(train, df_name = 'training')
val_df = data_augumentation(val, df_name  = 'validation')
test_df = data_augumentation(test, df_name = 'testing')

# Install the transformers library
!pip install transformers

import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments

# Sample data for demonstration
# Replace this with your actual data loading mechanism
def load_data():
    # Example data
    data = {
        'text': [
            "This is a real news article.",
            "This is another real news article.",
            "This is a fake news article.",
            "This is another fake news article."
        ],
        'label': [1, 1, 0, 0]  # 1 for real, 0 for fake
    }
    return pd.DataFrame(data)

# Load the dataset
df = load_data()

# Initialize the BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize the input text
inputs = tokenizer(df['text'].tolist(), padding=True, truncation=True, return_tensors='pt')

# Create a dataset class
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Create the dataset
dataset = NewsDataset(inputs, df['label'].tolist())

# Load the BERT model for sequence classification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # total number of training epochs
    per_device_train_batch_size=2,   # batch size per device during training
    per_device_eval_batch_size=2,    # batch size for evaluation
    warmup_steps=10,                  # number of warmup steps for learning rate scheduler
    weight_decay=0.01,                # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained('./fake_news_model')
tokenizer.save_pretrained('./fake_news_model')

print("Model training complete and saved.")

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# bert_ckpt_dir="gs://bert_models/2018_10_18/uncased_L-12_H-768_A-12/"
# bert_ckpt_file = bert_ckpt_dir + "bert_model.ckpt"
# bert_config_file = bert_ckpt_dir + "bert_config.json"
# 
# bert_model_dir="2018_10_18"
# bert_model_name="uncased_L-12_H-768_A-12"
# 
# !mkdir -p .model .model/$bert_model_name
# 
# for fname in ["bert_config.json", "vocab.txt", "bert_model.ckpt.meta", "bert_model.ckpt.index", "bert_model.ckpt.data-00000-of-00001"]:
#   cmd = f"gsutil cp gs://bert_models/{bert_model_dir}/{bert_model_name}/{fname} .model/{bert_model_name}"
#   !$cmd
# 
# !ls -la .model .model/$bert_model_name
# 
# bert_ckpt_dir = os.path.join(".model/",bert_model_name)
# bert_ckpt_file = os.path.join(bert_ckpt_dir, "bert_model.ckpt")
# bert_config_file = os.path.join(bert_ckpt_dir, "bert_config.json")

class FakeNewsData:
    """
    Preprocessing text into BERT features.

    max_seq_len: Maximum sequence length specified
    tokenizer: BERT tokenizer
    """
    DATA_COLUMN = "text"
    LABEL_COLUMN = "label"

    def __init__(self, tokenizer, train, validation, test, max_seq_len = 150):
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len
        ((self.train_x, self.train_y),
         (self.val_x, self.val_y),
         (self.test_x, self.test_y)) = map(self._prepare, [train, validation, test])

        ((self.train_x, self.train_x_token_types),
         (self.val_x, self.val_x_token_types),
         (self.test_x, self.test_x_token_types)) = map(self._pad,
                                                       [self.train_x, self.val_x, self.test_x])

    def _prepare(self, df):
        """
        Add start and end token for each sequence, and convert the text to tokenids.
        """
        x, y = [], []
        with tqdm(total=df.shape[0], unit_scale=True) as pbar:
            for ndx, row in df.iterrows():
                text, label = row[FakeNewsData.DATA_COLUMN], row[FakeNewsData.LABEL_COLUMN]
                tokens = self.tokenizer.tokenize(text)
                tokens = ["[CLS]"] + tokens + ["[SEP]"]
                token_ids = self.tokenizer.convert_tokens_to_ids(tokens)
                self.max_seq_len = max(self.max_seq_len, len(token_ids))
                x.append(token_ids)
                y.append(int(label))
                pbar.update()
        return np.array(x), np.array(y)

    def _pad(self, ids):
        """
        Pad each sequence to the specified max sequence length with [0]
        """
        x, t = [], []
        token_type_ids = [0] * self.max_seq_len
        for input_ids in ids:
            input_ids = input_ids[:min(len(input_ids), self.max_seq_len - 2)]
            input_ids = input_ids + [0] * (self.max_seq_len - len(input_ids))
            x.append(np.array(input_ids))
            t.append(token_type_ids)
        return np.array(x), np.array(t)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# tokenizer = FullTokenizer(vocab_file=os.path.join(bert_ckpt_dir, "vocab.txt"))
# data = FakeNewsData(tokenizer,
#                     train = train_df,
#                     validation = val_df,
#                     test = test_df,
#                     max_seq_len= 150)

def create_model(max_seq_len,lr = 1e-5):
  """
  Creates a BERT classification model.
  The model architecutre is raw input -> BERT input -> drop out layer to prevent overfitting -> dense layer that outputs predicted probability.

  max_seq_len: the maximum sequence length
  lr: learning rate of optimizer
  """


  # create the bert layer
  with tf.io.gfile.GFile(bert_config_file, "r") as reader:
      bc = StockBertConfig.from_json_string(reader.read())
      bert_params = map_stock_config_to_params(bc)
      bert = BertModelLayer.from_params(bert_params, name="bert")

  input_ids = keras.layers.Input(shape=(max_seq_len,), dtype='int32', name="input_ids")
  output = bert(input_ids)

  print("bert shape", output.shape)
  cls_out = keras.layers.Lambda(lambda seq: seq[:, 0, :])(output)
  # Dropout layer
  cls_out = keras.layers.Dropout(0.8)(cls_out)
  # Dense layer with probibility output
  logits = keras.layers.Dense(units=2, activation="softmax")(cls_out)

  model = keras.Model(inputs=input_ids, outputs=logits)
  model.build(input_shape=(None, max_seq_len))

  # load the pre-trained model weights
  load_stock_weights(bert, bert_ckpt_file)

  model.compile(optimizer=keras.optimizers.Adam(learning_rate = lr),
                loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=[keras.metrics.SparseCategoricalAccuracy(name="acc")])

  model.summary()

  return model

model = create_model(max_seq_len = data.max_seq_len, lr = 1e-5)

import datetime
OUTPUT_DIR = '/bert_news'
print('***** Model output directory: {} *****'.format(OUTPUT_DIR))

log_dir = ".log/bert_news/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%s")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir)

def model_fitting(max_epoch = 5, patience = 1):
    """
    Function to fit the model to training set. Validation set are used to find the optimal training epochs.
    Model will stop training when validation accuracy don't improve for a number of epochs. Then the model will restore weights to its best validation performance.

    max_epoch: Maximum number of epochs to train
    patience: Number of non-improving epochs before model stops
    """

    model.fit(x=data.train_x, y=data.train_y,
              validation_data = (data.val_x,data.val_y),
              batch_size=16,
              shuffle=True,
              epochs=max_epoch,
              callbacks=[keras.callbacks.EarlyStopping(patience=patience, restore_best_weights=True),
                        tensorboard_callback])
    return model

model = model_fitting(max_epoch = 5, patience = 1)
# Save the optimal weights for future usage
model.save_weights('bert_news.h5', overwrite=True)

# Download the model checkpoint
# OPTIONAL STEP - if we want to use them for prediction somewhere
from google.colab import files
files.download('bert_news.h5')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # model = create_model(max_seq_len = data.max_seq_len, lr = 1e-5)
# model.load_weights("bert_news.h5")
# 
# _, train_acc = model.evaluate(data.train_x, data.train_y)
# _, val_acc = model.evaluate(data.val_x, data.val_y)
# _, test_acc = model.evaluate(data.test_x, data.test_y)
# 
# print("train acc: ", train_acc)
# print("validation acc: ", val_acc)
# print("test acc: ", test_acc)

from sklearn.metrics import roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score
# model = create_model(max_seq_len = data.max_seq_len, lr = 1e-5)
model.load_weights("bert_news.h5")

# predict on test set
predictions = model.predict(data.test_x)
predictions = predictions[:,1]
test_df['pred'] = predictions
# average the prediction to become final prediction of original test set
test['avg_pred'] = test_df.groupby(['index'])['pred'].mean()

# plot ROC curve
fpr, tpr, _ = roc_curve(test['label'], test['avg_pred'])
roc_auc = auc(fpr, tpr)

fig = plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (auc = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic for original test set')
plt.legend(loc="lower right")
plt.show()

acc = accuracy_score(test['label'], test['avg_pred'] > 0.5)
precision = precision_score(test['label'], test['avg_pred'] > 0.5)
recall = recall_score(test['label'], test['avg_pred'] > 0.5)
f1 = f1_score(test['label'], test['avg_pred']  > 0.5)

print('Orignal test accuracy is ', acc)
print('Orignal test auc is ', roc_auc)
print('Orignal test precision is ', precision)
print('Orignal test recall is ', recall)
print('Orignal test f1 score is ', f1)

# As per the steps above :)

SAVED_MODEL_PATH  = "bert_news.h5"

# create model and load previous weights
model = create_model(max_seq_len = data.max_seq_len)
model.load_weights(SAVED_MODEL_PATH)

def predict_new(doc, model):
    """
    Predict new document using the trained model.

    doc: input document in format of a string
    """

    # clean the text
    doc = clean_txt(doc)
    # split the string text into list of subtexts
    doc = get_split(doc)
    # tokenize the subtexts as well as padding
    tokenizer = FullTokenizer(vocab_file=os.path.join(bert_ckpt_dir, "vocab.txt"))
    pred_tokens = map(tokenizer.tokenize, doc)
    pred_tokens = map(lambda tok: ["[CLS]"] + tok + ["[SEP]"], pred_tokens)
    pred_token_ids = list(map(tokenizer.convert_tokens_to_ids, pred_tokens))
    pred_token_ids = map(lambda tids: tids +[0]*(data.max_seq_len-len(tids)),pred_token_ids)
    pred_token_ids = np.array(list(pred_token_ids))

    # create model and load previous weights
    # model = create_model(max_seq_len = data.max_seq_len)
    # model.load_weights()

    # predict the subtexts and average the prediction
    predictions = model.predict(pred_token_ids)
    predictions = predictions[:,1]
    avg_pred = predictions.mean()
    if avg_pred > 0.5:
      doc_label = 'fake'
    else:
      doc_label = 'Real'

    return doc_label, avg_pred

# Run an example text from original test set
fake_test = load_convert_data("https://storage.googleapis.com/public-resources/dataset/fake_test.json")
doc = fake_test['text'][7]
print('----------------------NEWS -----------------------')
print(doc)
doc_label, avg_pred = predict_new(doc, model)
print()
print('---------------- PREDICTION RESULTS --------------')
print('The predicted probability of news being FAKE is ', avg_pred)
print('CLASSIFICATION : The predicted label of news is ', doc_label.upper())

