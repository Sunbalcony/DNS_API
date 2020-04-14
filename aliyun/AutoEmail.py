# -*- coding=utf-8 -*-
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header


class Office365:
    def __init__(self):
        self.mail_host = "smtp.office365.com"
        self.mail_sender = "xxxx"
        self.mail_license = "xxxx"

    def sendemail(self, mail_recv, title, mail_content):
        mail_receivers = str(mail_recv)
        print(mail_receivers)
        mm = MIMEMultipart('related')
        # 邮件主题
        subject_content = title
        # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
        mm["From"] = "info<xxxx>"
        # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
        mm["To"] = "<" + mail_receivers + ">"
        # 设置邮件主题
        mm["Subject"] = Header(subject_content, 'utf-8')
        # 邮件正文内容
        body_content = mail_content
        # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
        message_text = MIMEText(body_content, "plain", "utf-8")
        # 向MIMEMultipart对象中添加文本对象
        mm.attach(message_text)
        # 创建SMTP对象
        try:
            stp = smtplib.SMTP(self.mail_host)
            # 设置发件人邮箱的域名和端口，端口地址为25
            stp.connect(self.mail_host, port=587)
            # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
            # stp.set_debuglevel(1)
            # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
            stp.starttls()
            stp.login(self.mail_sender, self.mail_license)
            # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
            stp.sendmail(self.mail_sender, mail_receivers, mm.as_string())
            print("邮件发送成功")
            # 关闭SMTP对象
            stp.quit()
        except smtplib.SMTP as e:
            print("邮件发送成功")
            # 关闭SMTP对象
            stp.quit()


if __name__ == "__main__":
    sender = Office365()
    sender.sendemail()
