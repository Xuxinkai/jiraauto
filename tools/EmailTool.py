from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


def send_txt_email(mail_title, mail_content, receiver):
    """

    :param mail_title:
    :param mail_content:
    :param receiver:
    :return:
    """
    # 邮箱smtp服务器
    host_server = 'smtp.163.com'
    host_port = 465
    # sender为发件人的qq号码
    sender_name = ''
    # pwd为qq邮箱的授权码
    pwd = ''
    # 发件人的邮箱
    sender_mail = ''
    # 收件人邮箱
    # receiver = ''

    # 邮件的正文内容
    # mail_content = '你好，这是使用python登录office邮箱发邮件的测试'
    # 邮件标题
    # mail_title = '测试'

    # ssl登录
    smtp = SMTP_SSL(host_server, host_port)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(0)
    smtp.ehlo()
    smtp.login(sender_name, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_mail
    msg["To"] = receiver
    smtp.sendmail(sender_mail, receiver, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    send_txt_email('Jira SLA Notification', 'please check this jira ticket SLA, it will breached in 2 hours', '=')
