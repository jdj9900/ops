# -*-  encoding: utf-8 -*-
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart,MIMEBase
import smtplib,os

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 输入Email地址和口令:
from_addr = "jdj9900@126.com"
password = "jdj9900"
# 输入收件人地址:
to_addr = "jidajun@thinkjoy.cn"
# 输入SMTP服务器地址:
smtp_server = "smtp.126.com"

# 邮件对象:
msg = MIMEMultipart()
msg['From'] = _format_addr('Python <%s>' % from_addr)
msg['To'] = _format_addr('管理员<%s>' % to_addr)
msg['Subject'] = Header('from SMTP……', 'utf-8').encode()

# 邮件正文是MIMEText:
msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))

spath=r'D:\测试.xls'
path,file = os.path.split(spath)
# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open(spath.decode('utf-8').encode('gbk','ignore'), 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('application', "octet-stream", filename=file.decode('utf-8').encode('gbk'))
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename=file.decode('utf-8').encode('gbk'))
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    #不加此行，中文附件会在foxmail提示乱码
    mime.set_charset('gbk')
    # 添加到MIMEMultipart:
    msg.attach(mime)


server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25,126 ssl加密端口465
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
