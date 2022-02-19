"""
Practicing web scraping a reddit subreddit using python3 and PRAW library
PRAW: Python Reddit API Wrapper.

Takes in information from reddit posts, simplifies them, then sends it out in an email.
"""

import praw

# Our email to send custom emails from our gmail account.
import send_email
import json


def get_reddit_credentials(file_name: str):
    """Gets credentials needed to use the reddit API from a json file."""
    try:
        with open(file_name) as file_object:
            file_content = json.load(file_object)
            client_id = file_content["client_id"]
            client_secret = file_content["client_secret"]
            user_agent = file_content["user_agent"]
            username = file_content["username"]
            password = file_content["password"]

        return client_id, client_secret, user_agent, username, password
    except FileNotFoundError:
        print(
            "We can't seem to find that file. Make sure your file name is correct! Please try again."
        )
        return None


def create_reddit_object(client_id, client_secret, user_agent, username, password):
    """Creates reddit object for us to use and maniuplate."""

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        username=username,
        password=password,
    )

    return reddit


def main():
    # Create reddit scraper.
    # NOTE ** Change the file_name, and update your own credentials.
    # file_name = "reddit_credentials.json"
    file_name = "secrets.json"

    # Will return a tuple of variables, which we will unpack.
    if get_reddit_credentials(file_name):

        (
            client_id,
            client_secret,
            user_agent,
            username,
            password,
        ) = get_reddit_credentials(file_name)

        reddit = create_reddit_object(
            client_id, client_secret, user_agent, username, password
        )

        # Accessing the threads.
        # Each subreddit has five different ways of organizing the topics:
        # .hot, .new, .controversial, .top, .gilded.
        # Can also use .search("SEARCH_KEYWORDS")
        # gets only results matching an engine search.

        # top_posts = subreddit.top("month", limit=5)
        # new_posts = subreddit.top("all", limit=5)
        # NOTE Come back to create a "get_reddit_posts function"
        subreddit = reddit.subreddit("mechmarket")
        hhkb = subreddit.search("hhkb", sort="new", limit=5)
        i = 1
        reddit_notification = ""

        try:
            for post in hhkb:
                reddit_notification = (
                    reddit_notification
                    + f"<br><br>This is post number {i}: {post.title}"
                )  # <br> in HTML5 is break (essentially a new line)
                i += 1
        except:
            print(
                "Could not authenticate your reddit credentials. Please make sure they are all correct and try running the program again"
            )
        else:
            # Sending the email
            sender_email, password = send_email.authenticate_email()
            email_info = send_email.get_email_info(
                sender_email, password, body=reddit_notification
            )  # Returns a dictionary
            subject = email_info["subject"]
            body = email_info["body"]
            receiver_email = email_info["receiver_email"]
            html = f"""
            <html>
                <body>
                    <h1>{subject}</h1>
                    <p1>{reddit_notification}</p1>
                </body>
            </html>
            """

            message = send_email.build_email(
                sender_email, receiver_email, subject, body, html=html
            )

            send_email.send_email(
                message,
                sender_email,
                receiver_email,
                password,
            )


if __name__ == "__main__":
    main()
