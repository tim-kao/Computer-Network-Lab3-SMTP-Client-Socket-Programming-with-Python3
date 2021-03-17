from socket import *
import base64


# RFC 2617 requires that in HTTP Basic authentication, the username and password must be encoded with base64.
buffer_size = 2048
# Mail message
subject = 'Greet with an image'
msg = 'I share my picture with you.'
filename = 'cat2.jpg'
with open(filename, "rb") as f:
    image_msg = base64.b64encode(f.read())
endmsg = '\r\n.\r\n'
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.mailtrap.io'
sender = '<@gmail.com>'
recipient = '<@inbox.mailtrap.io>'
Username = ''
Password = ''
port = 25

# Create socket called clientSocket and establish a TCP connection with mailserver
# Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)  # TCP
clientSocket.connect((mailserver, port))
# Fill in end
recv = clientSocket.recv(buffer_size).decode()
print('Build a connection with a mail server')
print('recv:', recv)
if recv[:3] != '220':
    print('220 reply not received from server')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(buffer_size).decode()
print('Send HELO command')
print('recv1:', recv1)
if recv1[:3] != '250':
    print('250 reply not received from server')

# Login
# Start authentication
Authentication = 'AUTH LOGIN\r\n'
clientSocket.send(Authentication.encode())
auth_recv = clientSocket.recv(buffer_size).decode()
print('Authentication', auth_recv)
if auth_recv[:3] != '334':
	print ('334 reply not received from server')

# Send username
uname = base64.b64encode(Username.encode()) + b'\r\n'
clientSocket.send(uname)
uname_recv = clientSocket.recv(buffer_size).decode()
print('Send username', uname)
print(uname_recv)
if uname_recv[:3] != '334':
	print ('334 reply not received from server')

# Send password
pword = base64.b64encode(Password.encode()) + b'\r\n'
clientSocket.send(pword)
pword_recv = clientSocket.recv(buffer_size).decode()
print('Send password', pword)
print(pword_recv)
if pword_recv[:3] != '235':
	print ('235 reply not received from server')

# Send MAIL FROM command and print server response.
# Fill in start
mail_from = 'MAIL FROM: ' + sender + '\r\n'
clientSocket.send(mail_from.encode())
recv2 = clientSocket.recv(buffer_size).decode()
print('recv2:', recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')
# Fill in end
# Send RCPT TO command and print server response.
# Fill in start
rcpt_to = 'RCPT TO: ' + recipient + '\r\n'
clientSocket.send(rcpt_to.encode())
recv3 = clientSocket.recv(buffer_size).decode()
print('recv3:', recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')
# Fill in end
# Send DATA command and print server response.
# Fill in start
data_command = 'DATA\r\n'
clientSocket.send(data_command.encode())
recv4 = clientSocket.recv(buffer_size).decode()
print('recv4:', recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')
# Fill in end
# Send message data.
# Fill in start

message = 'MIME-Version: 1.0\r\n'
message += 'from:' + sender + '\r\n'
message += 'to:' + recipient + '\r\n'
message += 'subject:' + subject + '\r\n'

raw = 'Content-Type: multipart/related; boundary="000000000000b6a37005bcde5e56"\r\n\r\n' \
      '--000000000000b6a37005bcde5e56\r\n' \
      'Content-Type: multipart/alternative; boundary="000000000000b6a36e05bcde5e55"\r\n\r\n' \
      '--000000000000b6a36e05bcde5e55\r\nContent-Type: text/plain; charset="UTF-8"\r\n\r\n' \
      + msg + '\r\n\r\n--000000000000b6a36e05bcde5e55\r\n' \
      'Content-Type: text/html; charset="UTF-8"\r\n\r\n' \
      + msg + '<div dir="ltr"><img src="cid:ii_klxs09zr0" alt="' + filename + '" width="473" height="266"><br></div>\r\n\r\n' \
      '--000000000000b6a36e05bcde5e55--\r\n'  \
      '--000000000000b6a37005bcde5e56\r\n'
raw += 'Content-Type: image/jpeg; name="' + filename + '"\r\n'
raw += 'Content-Disposition: attachment; filename="' + filename + '"\r\n'
raw += 'Content-Transfer-Encoding: base64\r\n'
raw += 'X-Attachment-Id: ii_klxs09zr0\r\n'
raw += 'Content-ID: <ii_klxs09zr0>\r\n\r\n'

message += raw
message = message.encode()
message += image_msg
message += '\r\n\r\n'.encode()
message += '--000000000000b6a37005bcde5e56--\r\n'.encode()
clientSocket.send(message)

# Fill in end
# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(buffer_size).decode()
print('recv5:', recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

# Fill in end
# Send QUIT command and get server response.
# Fill in start
quit_command = b'QUIT\r\n'
clientSocket.send(quit_command)
recv6 = clientSocket.recv(buffer_size).decode()
print('recv6:', recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')
clientSocket.close()
print('Connection closed')
# Fill in end
