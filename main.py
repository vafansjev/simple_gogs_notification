from flask import Flask, request
import requests
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
available_act=['pull_request', 'issue_comment']

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


@app.route('/gogs/', methods=['POST'])
def webhook_catch():
    message = 'still empty'
    gogs_event = request.headers.get('X-Gogs-Event')
    if gogs_event not in available_act:
        return 'Not supported event'

    payload = request.get_json()

    if gogs_event == 'pull_request':
        pr = payload['pull_request']
        committer = payload['sender']
        action = payload['action'] # status opened/closed
        number = payload['number']
        title = pr['title'] # PR title
        body = pr['body'] # PR message
        branch = pr['head_branch'] # from branch
        base_branch = pr['base_branch'] # to branch
        pr_url = pr['html_url'] # commit url
        sender_name = committer['full_name']
        sender_login = committer['username']

        if action == 'opened':
            message = f'\U0001F34C <b>New PR</b> № {number}\n <i>from {branch} to {base_branch}</i>! \n\n' \
                      f'<b>PR Title:</b> {title}\n<b>PR Message:</b> <i>{body}</i> \n' \
                      f'<b>Author:</b> {sender_name} ({sender_login}) \n\n' \
                      f'<a href="{pr_url}">Link to PR</a>\n\n'
        if action == 'closed':
            head = pr['head_repo']
            repo_name = head['name']
            repo_fullname = head['full_name']
            description = head['description']
            repo_url = head['html_url']
            message = f'\U00002705 <b>PR №{number}</b> to {repo_name} was {action}!\n' \
                       f'<i>Thanks to:</i> {sender_name}({sender_login})\n\n' \
                       f'Link to <a href="{repo_url}">{repo_fullname}</a>\n\n'

    if gogs_event=='issue_comment':
        action = payload['action']
        issue = payload['issue']
        comment = payload['comment']
        user = comment['user']
        author = user['full_name']
        login = user['username']
        comment_text = comment['body']
        repo = payload['repository']
        repo_name = repo['name']
        pr_num = issue['number']
        comment_link = comment['html_url']
        if action == 'created':
            message = f'\U00002709 <b>New comment</b> to PR №{pr_num} on {repo_name}\n' \
                      f'<b>By:</b> <i>{author}({login})</i>\n' \
                      f'<b>Message:</b> <i>{comment_text}</i>\n\n' \
                      f'<a href="{comment_link}">Link to HolyWar</a>\n\n'
        else:
            message = f'Strange action from issue- {action}'

    telegram_message(message)

    return 'Webhook processed'


def telegram_message(message):
    print(message)
    url = f'https://api.telegram.org/{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print('Failed to send message to Telegram')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
