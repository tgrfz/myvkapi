# TODO: friend deleted page
# TODO: new and deleted friends

import vk_api
import random

def get_statuses(vkapi, user_id):
    def status(st):
        st = st.replace('\n', ' ')
        if st == '' or st == ' ':
            st = '-'
        return st
        
    friends = vkapi.friends.get(user_id = user_id, fields = 'status')['items']
    return {fr['id']: status(fr.get('status', '???')) for fr in friends}

def status_change(vkapi, user_id, old_statuses = {}):
    """old_statuses = {id1: "status1", ..., idn: "statusn"}
    """
    def status(st):
        st = st.replace('\n', ' ')
        if st == '' or st == ' ':
            st = '-'
        return st

    friends = vkapi.friends.get(user_id = user_id, fields = 'first_name, second_name, status')
    diff = []
    for friend in friends['items']:
        friend['status'] = status(friend.get('status', '???'))
        friend['old_status'] = status(old_statuses.get(friend['id'], '???'))
        if friend['status'] != friend['old_status']:
            keys = list(friend.keys())
            for key in keys:
                if key not in ['id', 'first_name', 'last_name', 'status', 'old_status']:
                    del friend[key]
            diff.append(friend)
    return diff

def send_status_change_message(vkapi, user_id, diff):
    """vkapi - for messages.send method  
    user_id - who receive the message and whose friends statuses we check
    diff - something like
    [{'id': 123, 'first_name': 'name', 'last_name': 'lname', 'status': 'new', 'old_status': 'old'}, {...}, ...]
    Key 'id' is required.
    """
    def send_message(vkapi, id, mess):
        try:
            vkapi.messages.send(user_id = id, message = mess, random_id = random.randint(1, 65536))
        except Exception as e:
            print(e, mess, sep=' for message:\n')

    for friend in diff:
        send_message(vkapi, user_id, '[id{}|{} {}] changed status from\n{}\nto\n{}'.format(friend['id'],\
                                                friend.get('first_name', 'name'), friend.get('last_name', 'name'),\
                                                friend.get('old_status', '???'), friend.get('status', '???')))
    pass