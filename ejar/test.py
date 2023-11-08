def strip_punctuation(word):
    punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
    for char in punctuation_chars:
        word = word.replace(char, "")
    return word

def get_neg(sentence):
    negative_words = []
    with open("negative_words.txt") as neg_f:
        for lin in neg_f:
            if lin[0] != ';' and lin[0] != '\n':
                negative_words.append(lin.strip())

    sentence = sentence.lower()
    words = sentence.split()
    count = 0
    for word in words:
        word = strip_punctuation(word)
        if word in negative_words:
            count += 1
    return count

def get_pos(sentence):
    positive_words = []
    with open("positive_words.txt") as pos_f:
        for lin in pos_f:
            if lin[0] != ';' and lin[0] != '\n':
                positive_words.append(lin.strip())

    sentence = sentence.lower()
    words = sentence.split()
    count = 0
    for word in words:
        word = strip_punctuation(word)
        if word in positive_words:
            count += 1
    return count

file = open("project_twitter_data.csv", "r")
lines = file.readlines()
header = "Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score\n"
result_file = open("resulting_data.csv", "w")
result_file.write(header)
for line in lines[1:]:
    words = line.strip().split(",")
    retweets = words[1]
    replies = words[2]
    positive_score = get_pos(words[0])
    negative_score = get_neg(words[0])
    net_score = positive_score - negative_score
    result_file.write("{}, {}, {}, {}, {}\n".format(retweets, replies, positive_score, negative_score, net_score))
result_file.close()
