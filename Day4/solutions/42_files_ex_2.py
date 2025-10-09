tweets = [
{
    "created_at": 'Sat Feb 08 15:29:13 +0000 2020',
    "full_text": "I love python!",
    "user": {
        "id": "1234567890",
        "screen_name": "PythonLover"
    }
},
{
    "created_at": 'Sat Feb 14 16:39:33 +0000 2020',
    "full_text": "Happy cheese day!",
    "user": {
        "id": "1234567999",
        "screen_name": "PythonHater"
    }
},
{
    "created_at": 'Sat Feb 15 14:44:44 +0000 2020',
    "full_text": "I love beer!",
    "user": {
        "id": "1234567890",
        "screen_name": "PythonLover"
    }
}]


with open("tweets_example.json", "w") as write_file:
    for tweet in tweets:
        json.dump(tweet, write_file)
        write_file.write("\n")

readtweets = list()
with open("tweets_example.json", "r") as read_file:
    line = read_file.readline()
    while (line):
        newtweet = json.loads(line)
        readtweets.append(newtweet)
        line = read_file.readline()
print(readtweets)