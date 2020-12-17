import torch
from torch import nn, optim
import re
import spacy
from torchtext import data

# from torchtext import data
# from torchtext import datasets
# import pickle

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# with open('./vocab.pkl', 'rb') as f:
#     vocab = pickle.load(f)
# INPUT_DIM = len(vocab)
# EMBEDDING_DIM = 100
# HIDDEN_DIM = 256
# OUTPUT_DIM = 1
# N_LAYERS = 2
# BIDIRECTIONAL = True
# DROPOUT = 0.5
# PAD_IDX = 0

# model = RNN(INPUT_DIM, 
#             EMBEDDING_DIM, 
#             HIDDEN_DIM, 
#             OUTPUT_DIM, 
#             N_LAYERS, 
#             BIDIRECTIONAL, 
#             DROPOUT, 
#             PAD_IDX)

# model.load_state_dict(torch.load('./tut2-model.pt'))




# def predict_sentiment(vocab, model, sentence):
#     sentence = preprocess_tweet(sentence)
#     model.eval()
#     tokenized = [tok.text for tok in nlp.tokenizer(sentence)]
#     indexed = [vocab.stoi[t] for t in tokenized]
#     length = [len(indexed)]
#     tensor = tensor.unsqueeze(1)
#     length_tensor = torch.LongTensor(length)
#     prediction = torch.sigmoid(model(tensor, length_tensor))
    
#     if prediction.item() >= 0.5:
#         return 'Positive'
#     else:
#         return 'Negative'




def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    # Convert more than 2 letter repetitions to 2 letter
    # funnnnny --> funny
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    return word


def is_valid_word(word):
    # Check if word begins with an alphabet
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)


def handle_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet


def preprocess_tweet(tweet):
    processed_tweet = []
    # Convert to lower case
    tweet = tweet.lower()
    # Replaces URLs with the word URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
    # Replace @handle with the word USER_MENTION
    tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
    # Replaces #hashtag with hashtag
    tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
    # Remove RT (retweet)
    tweet = re.sub(r'\brt\b', '', tweet)
    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace emojis with either EMO_POS or EMO_NEG
    tweet = handle_emojis(tweet)
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)
    words = tweet.split()

    for word in words:
        word = preprocess_word(word)
        if is_valid_word(word):
            processed_tweet.append(word)

    return ' '.join(processed_tweet)

