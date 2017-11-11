# Mailgun
Python files that use Mailgun's API
# Get statistics from message tags (mailgun.py)
In this implementation, we have used 4 different tags, the first is LrgEm##, then LrgEm##a, LrgEm##b, and LrgEm##c. This gets the summation of all these tags and bases the results on those numbers. The user only has to enter the first one (LrgEm##).

![1](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-10-at-3-59-51-pm.png)
![2](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-10-at-3-58-56-pm.png)

# Download email addressess that should be removed (downloadFailures.py)
This one gets the email addresses of hard bounces, unsubscribes, and complaints and puts them into excel files so that you can later upload them for deletion.

![1](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-10-at-7-08-36-pm.png)

# Download Logs (downloadLogs.py)
This gets all of the events that have occured on an email for a specific tag. This also consolidates all the tags for a, b, and c and creates an xlsx spreadsheet. There are also pre-populated fields in the spreadsheet with number of opens, clicks, delivers, fails, open rate, and click through rate.

![1](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-11-at-12-49-12-am.png)
![2](https://ianannasetech.files.wordpress.com/2017/11/screen-shot-2017-11-11-at-1-21-56-am.png)
