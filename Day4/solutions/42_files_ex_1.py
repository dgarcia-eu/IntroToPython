with open('germany_party_account3.txt', 'w') as f:
    for u, i in zip(user, user_id):
        f.write('{},{}\n'.format(u, i))  # '\n': new line