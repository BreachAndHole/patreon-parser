# login page
EMAIL_FIELD_XPATH = '//input[@aria-label="Email"]'
PASSWORD_FIELD_XPATH = '//input[@aria-label="Password"]'
CONTINUE_LOGIN_BUTTON_XPATH = '//button[@type="submit"]'

# video filtering
CONTENT_TYPE_FILTER_XPATH = '//button[@label="Post type"]'
CONTENT_TYPE_BUTTONS_XPATH = '(//div[@role="dialog"])//button'

# content page
LOAD_MORE_POSTS_BUTTON_XPATH = '(//div[contains(@style, "text-align")])/button'
POST_CARD_XPATH = '//div[@data-tag="post-card"]'

# post parsing
POST_URL_XPATH = '(.//span[@data-tag="post-title"])/a'
YOUTUBE_URL_XPATH = '//div//p//a[contains(@href, "https://you")]'
