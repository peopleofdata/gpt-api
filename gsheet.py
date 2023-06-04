deployment_name = 'GPT-API2'
from datetime import datetime
now = lambda: datetime.now().strftime("%Y%m%d_%H%M%S")

# Gsheet manipulation details
import pygsheets, os, json
from google.oauth2 import service_account

os.environ['GDRIVE_API_CREDENTIALS'] = json.dumps({
  "type": "service_account",
  "project_id": "groupgpt",
  "private_key_id": "de339807cd4f6159f85da4ed45795acbbfe1b777",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC+g/lyCMzdDmDA\nWgJ3NGhvz0cz9IUMgLtPdohQvX1lf+MRhIH5NgQr5uW27z++NeUXEwcf3INszbHN\nrsBZWLDCbWwMtz/DmL5dP6G2pUTZtg+iRueqgzcE3rH/7MH6YrbdR8TGjhykZnLN\nr2X3k/bh30Pc7kZqPgkR5OAjWzyVl3icGji4BivlpMou3lus59GokFFDmpk0v80R\nLtlRbQzOAG3liXoBO5NqEGpZuNdzsqrNHoSsAHxH+MCI8wlxtllX3bzlXQqCSeZu\nDJn6BiuOwMlcKPPKGljEF59yK15oldG+VsjzBqCI9ViDUFEE8tznS9gQIEKEVaap\no4l6qHwDAgMBAAECggEAEUFDZW2gnbYrUyCT2pdiN3DkN7NsyCNx/jzJFIRPstKw\nuSnG2nsRnlGiT+g+s2E5kivErcEQx4OgbUrnhvATyk2TcgS4Kg9P0S2YiEH9s2OG\n6kwBDXN8Qdz9mCVUXZ4f284f51qAWO93ybiaGUtLGqKtsyPYOCUi4ykB7TyFMd3G\nzMKxEhHkaWCkGqI7JkkUz9+MTjot3FFmLJd/q1bO+jmYUfununbvY3ojR3v/trWL\ntpw0vxTcCSEwLj2BJfj0dU5SzwxOWelaj0OjkS6JSUjfaQdlas3BhBkQphd5281n\nJjYHeCn8lGZfEfxDENfoWnL3dOopmRmDj/UCRy7VaQKBgQD89mt8ztXcX8RLzuw8\nSfhc3RoJKGlcwgaCzsDsylyP1gXqjI/hO89jIWdknJIuDe093RFSE8B8bXXWWgMh\nTAhOtOpvnPJ0RTvO4nJbBXf0JIy/rYfdUlNAbyIADvO7urYoZUb92wh+Y1YjgBQ8\nXc7OTQ0hlbWop1ueWD4tASlGHwKBgQDAzZlSDbh92KsM4DneumB6oi+zSq9xRjQO\nstaD3+d1bxrv4OtC98TPlcCcNDCSpv/9s3VpMroJDg4t/hmNgyo4baqnNJYdnIMy\nKHgJlWTV4QCy1rgKvhXHCjEQwLrv3kgxtcRnLxrIPB9+8wSoVjeobbx+533xok1J\nR2E18AolnQKBgAxY/vAtrHTAW/WTWSasOapWxJGT3mi/s8+oxfQJALGoscs8Jz3I\nTJw7Ii/gEKac2Wq+orzN6ARq12iqJiL28iTdYeAm2hLg2kWD+i8FOlC5hAFLOCmO\nfi/T/OXh1PXh7EhWgTuc+HIq6SZ8dwBnV9PsIOr1wtNDsA4vooFR4DDjAoGBAMCy\nfIOa/QKic8sJrC0kv9qxkNU0VwbysILkUSw6s54WbqjDdr9W3ZjPxlMYgleAm6gY\nHcgHkBIOvzNOnIFoT+FYElDNaR+tVx7hfZ+udbqiCE219vmdpCxrzkA9MFkfI66z\nSdoLJUxtctkx0Dzi9vvauaNogOLpYS9VLR54i9utAoGBAL3i4ztLMQ0Nrtic0tQW\ni1So0jfv+OdipyBwmuFrnzL9RH0Guk+DGP8sp8owbH4ej/oYgu0b7EMjmuhPTjIa\nuScIOM28efMZQry8RggzGB+0129VE9rBrcbPzLCjrq4SgGENo7Ur19E768zxoQ2M\n0bKCmmfKffwKF1FcQAoUs3H2\n-----END PRIVATE KEY-----\n",
  "client_email": "groupgpt-bot@groupgpt.iam.gserviceaccount.com",
  "client_id": "117456254761374734781",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/groupgpt-bot%40groupgpt.iam.gserviceaccount.com"
})

spreadsheet_id = '1ox3ooXQJ5F8FmK0cmPhWfRMbkK8NgPWZjhY07trTktE'
scopes = ['https://www.googleapis.com/auth/spreadsheets']
sheet_name = deployment_name
service_secret = os.environ.get('GDRIVE_API_CREDENTIALS')
service_secret = json.loads(service_secret)
print(f'Service secret: {service_secret}')

def initiate_sheet(service_secret=service_secret):
    credentials = service_account.Credentials.from_service_account_info(service_secret, scopes=scopes)
    gc = pygsheets.authorize(custom_credentials=credentials)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    return wks_write

wks_write = initiate_sheet(service_secret=service_secret)

def write_to_gsheet(msg, wks_write=wks_write):
    row = [[deployment_name, now(), json.dumps(msg), msg['role'], msg['content']]]#, list(msg.keys())[0], msg['content']
    wks_write.append_table(row, dimension='ROWS', overwrite=False)