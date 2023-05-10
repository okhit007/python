import os,json
    
iv = ""
password = ""

text = {""
}
# out = os.popen(f'printf "{text}" | openssl aes-256-cbc -base64 -K {password} -iv {iv}').read()
out = os.popen('openssl aes-256-cbc -base64 -K %s -iv %s -in %s' %(password, iv, text))

print(f"IV: {iv}")    
print(f"PWD: {password}")     
print(f"MSG: {text}")   
print(f"OUT: {out}") 