Gogs webhook receiver & telegram sender 

Catch webhooks at: <host-ip>:<Port>(default 5000)/gogs/

Receiving events:
- PR opened
- PR closed
- New comment in PR

.env file:
- CHAT_ID - Telegram group (Bot must be a member of the group)
- BOT_TOKEN - obviously


Default notify group - "RoCsi_PR's"

Override by using -e, for example:

docker run -d -p 5000:5000 -e BOT_TOKEN="YOURBOTTOKEN" -e CHAT_ID="YOUR_CHATID" --name dev_gogs dev_gogs:latest