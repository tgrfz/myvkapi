import vk_api
import time

def get_all_votes(vkapi, group_id, user_id):
    count = vkapi.wall.get(owner_id = -group_id, count = 0)['count']
    offset = 0
    votes = []
    while offset < count:
        posts = vkapi.wall.get(owner_id = -group_id, offset = offset, count = (count - offset - 1) % 100 + 1)['items']
        offset += 100
        for post in posts:
            attachments = post.get('attachments', [],)
            for att in attachments:
                if att.get('type') == 'poll':
                    poll = att['poll']
                    if poll.get('anonymous') == True:
                        continue
                    user_vote = {'id': poll.get('id'), 'question': poll.get('question'), 'answers': [], 'link': f"https://vk.com/wall-{group_id}_{post['id']}"}

                    answer_ids = [ans.get('id') for ans in poll.get('answers', [])]
                    ans_q = {ans.get('id'): ans.get('text') for ans in poll.get('answers', [])}

                    try:
                        voters = vkapi.polls.getVoters(owner_id = poll.get('owner_id'), poll_id = poll.get('id'), answer_ids = answer_ids)
                    except Exception as e:
                        print(e, poll, sep=' for poll:\n')
                        continue
                    
                    for ans in voters:
                        if ans.get('users', {}).get('items', []).count(user_id) > 0:
                            user_vote['answers'].append({'id': ans.get('answer_id'), 'text': ans_q.get(ans.get('answer_id'), "")})
                    
                    if len(user_vote['answers']) > 0:
                        votes.append(user_vote)
                        # print(user_vote)

                    time.sleep(0.05)
    return votes
                
def get_common_votes(votes1, votes2, group_id = 111960606):
    """group_id - for link"""
    common = []
    for vote1 in votes1:
        for vote2 in votes2:
            if (vote1['id'] == vote2['id']):
                common.append({'id': vote1['id'],'question': vote1['question'], 'answers1': vote1['answers'], 'answers2': vote2['answers'], 'link': vote1['link']})
    return common

def get_common_votes(vkapi, group_id, user1_id, user2_id):
    count = vkapi.wall.get(owner_id = -group_id, count = 0)['count']
    offset = 0
    votes = []
    while offset < count:
        posts = vkapi.wall.get(owner_id = -group_id, offset = offset, count = (count - offset - 1) % 100 + 1)['items']
        offset += 100
        for post in posts:
            attachments = post.get('attachments', [],)
            for att in attachments:
                if att.get('type') == 'poll':
                    poll = att['poll']
                    if poll.get('anonymous') == True:
                        continue
                    user_vote = {'id': poll.get('id'), 'question': poll.get('question'), 'answers1': [], 'answers2': [], 'link': f"https://vk.com/wall-{group_id}_{post['id']}"}

                    answer_ids = [ans.get('id') for ans in poll.get('answers', [])]
                    ans_q = {ans.get('id'): ans.get('text') for ans in poll.get('answers', [])}

                    try:
                        voters = vkapi.polls.getVoters(owner_id = poll.get('owner_id'), poll_id = poll.get('id'), answer_ids = answer_ids)
                    except Exception as e:
                        print(e, poll, sep=' for poll:\n')
                        continue
                    
                    for ans in voters:
                        if ans.get('users', {}).get('items', []).count(user1_id) > 0:
                            user_vote['answers1'].append({'id': ans.get('answer_id'), 'text': ans_q.get(ans.get('answer_id'), "")})
                        if ans.get('users', {}).get('items', []).count(user2_id) > 0:
                            user_vote['answers2'].append({'id': ans.get('answer_id'), 'text': ans_q.get(ans.get('answer_id'), "")})
                    
                    if len(user_vote['answers1']) > 0 and len(user_vote['answers2']) > 0:
                        votes.append(user_vote)
                        # print(user_vote)

                    time.sleep(0.05)
    return votes