# Testing the just-flask-session-server-2. Verify that calls in the same session keep the session information,
# while another session doesn't have other sessions info.

import requests

BASE_URL = 'http://127.0.0.1:5000'

sids = []

s = requests.Session()
r = s.get(BASE_URL + '/setsession')
print(f'r.status_code, r.text: {r.status_code} {r.text}')
assert "The session has been Set" in r.text

r = s.get(BASE_URL + '/getsession')
print(f'r.status_code, r.text: {r.status_code} {r.text}')
assert "Welcome Admin" in r.text

r = s.get(BASE_URL + '/getsession')
print(f'r.status_code, r.text: {r.status_code} {r.text}')
assert "Welcome Admin" in r.text

r = s.get(BASE_URL + '/popsession')
print(f'r.status_code, r.text: {r.status_code} {r.text}')
assert r.text == "Session Deleted"

r = s.get(BASE_URL + '/getsession')
print(f'r.status_code, r.text: {r.status_code} {r.text}')
assert r.text == "Welcome Anonymous"

r = s.get(BASE_URL + '/setsession')
print(f'r.status_code, r.text: {r.status_code} {r.text}')
assert "The session has been Set" in r.text

r = s.get(BASE_URL + '/getsession-json')
print(f'r.status_code, r.text: {r.status_code} {r.json()}')
assert r.json()["Welcome"] == "Admin"
sids.append(r.json()["my_sid"])
print("sids:", str(sids))



print("Test a second session s2")
s2 = requests.Session()
r2 = s2.get(BASE_URL + '/getsession')
print(f'r2.status_code, r2.text: {r2.status_code} {r2.text}')
assert r2.text == "Welcome Anonymous"

r2 = s2.get(BASE_URL + '/setsession')
print(f'r2.status_code, r2.text: {r2.status_code} {r2.text}')


r2 = s2.get(BASE_URL + '/getsession-json')
print(f'r2.status_code, r2.text: {r2.status_code} {r2.json()}')
assert r2.json()["my_sid"] not in sids
sids.append(r2.json()["my_sid"])
print("sids:", str(sids))

# test sesssion info
s3 = requests.Session()
r3 = s3.get(BASE_URL + '/setsession')
print(f'r3.status_code, r3.text: {r3.status_code} {r3.text}')

r3 = s3.get(BASE_URL + '/getsession-json')
print(f'r3.status_code, r3.text: {r3.status_code} {r3.json()}')
assert r3.json()["my_sid"] not in sids
sids.append(r3.json()["my_sid"])
print("sids:", str(sids))

r3 = s3.get(BASE_URL + '/getsession-json')
print(f'r3.status_code, r3 json: {r3.status_code} {r3.json()}')

print("test passed successfully")



