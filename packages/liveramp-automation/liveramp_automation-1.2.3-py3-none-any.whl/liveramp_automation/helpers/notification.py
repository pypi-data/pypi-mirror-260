from typing import Optional, Dict, Any, Sequence, List, Tuple
from liveramp_automation.utils.slack import SlackHTMLParser, SlackWebhook, WebhookResponse, SlackBot


class NotificationHelper:
    @staticmethod
    def slack_webhook_notify(*,
                     webhook_url: str,
                     message: str,
                     attachments: Optional[Sequence[Dict[str, Any]]] = None,
                     blocks: Optional[Sequence[Dict[str, Any]]] = None,
                     parsed_html_flag: Optional[bool] = False) -> WebhookResponse:
        """Sends a message to the webhook URL.

        Args:
            message: Plain text string to send to Slack.
            attachments: A collection of attachments
            blocks: A collection of Block Kit UI components
            parsed_html_flag: A flag indicates whether need parse the parameter message, otherwise send the message to Slack directly. default: False 

        Returns:
            Webhook response

        Example:
        WEBHOOk_URL = "https://hooks.slack.com/services/xxxxx/xxxxxx/xxxxxx"
        html_string = '''
            <p>
                Here <i>is</i> a <strike>paragraph</strike> with a <b>lot</b> of formatting.
            </p>
            <br>
            <code>Code sample</code> & testing escape.
            <ul>
                <li>
                    <a href="https://www.google.com">Google</a>
                </li>
                <li>
                    <a href="https://www.amazon.com">Amazon</a>
                </li>
            </ul>
        '''
        blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "New request"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Type:*\nPaid Time Off"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Created by:*\n<example.com|Fred Enriquez>"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*When:*\nAug 10 - Aug 13"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "<https://example.com|View request>"
                    }
                }
            ]

        attachments = [
            {
                "fallback": "Plain-text summary of the attachment.",
                "color": "#2eb886",
                "pretext": "Optional text that appears above the attachment block",
                "author_name": "Bobby Tables",
                "author_link": "http://flickr.com/bobby/",
                "author_icon": "http://flickr.com/icons/bobby.jpg",
                "title": "Slack API Documentation",
                "title_link": "https://api.slack.com/",
                "text": "Optional text that appears within the attachment",
                "fields": [
                    {
                        "title": "Priority",
                        "value": "High",
                        "short": False
                    }
                ],
                "image_url": "http://my-website.com/path/to/image.jpg",
                "thumb_url": "http://example.com/path/to/thumb.png",
                "footer": "Slack API",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": 123456789
            }
        ]
        NotificationHelper.slack_notify(webhook_url=WEBHOOk_URL, message="test")
        NotificationHelper.slack_notify(webhook_url=WEBHOOk_URL, message=html_string, parsed_html_flag=True)
        NotificationHelper.slack_notify(webhook_url=WEBHOOk_URL, message="test", attachments=attachments, blocks=blocks)
        :param webhook_url:
        """
        client = SlackWebhook(url=webhook_url)
        if parsed_html_flag:
            parser = SlackHTMLParser()
            message = parser.parse(message)
        return client.send(message=message, attachments=attachments, blocks=blocks)

    @staticmethod
    def send_message_to_channels(token: str, channels: List[str], message: str) -> Dict[str, Tuple[bool, str]]:
        """
        Send a message to multiple channels.

        Args:
            token (str): The Slack token.
            channels (List[str]): A list of channel IDs.
            message (str): Plain text string to send to Slack.

        Returns:
            A dictionary mapping channel IDs to a tuple of success status and error message (if any).
        """
        # Create an instance of SlackBot with the provided token
        slack_bot = SlackBot(token=token, timeout=15)

        # Call send_message_to_channels method
        return slack_bot.send_message_to_channels(channels, message)

    @staticmethod
    def reply_latest_message(token: str, channel_id: str, message: str) -> bool:
        """
        Reply to the latest message in a channel.

        Args:
            token (str): The Slack token.
            channel_id (str): ID of the channel to reply to.
            message (str): Plain text string to send to Slack.

        Returns:
            A boolean indicating success or failure of the reply operation.
        """
        # Create an instance of SlackBot with the provided token
        slack_bot = SlackBot(token=token, timeout=15)

        # Call reply_latest_message method
        return slack_bot.reply_latest_message(channel_id, message)

    def pagerduty_notify(self):
        return

    def oc_notify(self):
        return
