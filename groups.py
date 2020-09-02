#TODO: members_change get old and new lists, not vkapi
#TODO: replace members_change into send_members_change_message

import vk_api
import random

def members_change(vkapi, group_id, old_members = []):
    """Return two sets: new members and no longer members"""
    old_members = set([str(i) for i in old_members])
    current_members = set([str(i) for i in vkapi.groups.getMembers(group_id = group_id)['items']])
    return current_members.difference(old_members), old_members.difference(current_members)

def send_members_change_message(vkapi, user_id, group_id, new_members, no_longer_members):
    """vkapi - for messages.send method   
    user_id - who receive the message
    """
    def send_message(vkapi, id, mess):
        try:
            vkapi.messages.send(user_id = id, message = mess, random_id = random.randint(1, 65536))
        except Exception as e:
            print(e, mess, sep=' for message:\n')

    if new_members:
        mess = "\nvk.com/id".join(["New members of vk.com/public{}:".format(group_id), *new_members])
        send_message(vkapi, user_id, mess)

    if no_longer_members:
        mess = "\nvk.com/id".join(["No longer members of vk.com/public{}:".format(group_id), *no_longer_members])
        send_message(vkapi, user_id, mess)
