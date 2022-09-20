import sys
import random
from twilio.rest import Client


MESSAGING_SERVICE_SID='XXXXXXXXXX'
ACCOUNT_SID = 'XXXXXXXXXXXX'
AUTH_TOKEN = 'XXXXXXXXXXXX'
SMS_PHONE = '+10000000000'
SMS_BODY = """Hello {}!
We are delighted to invite you to the annual Hanukkah-Christmas!
Please note that you are the dwarf of {}. 
Shhh.. keep it secret!"""


##########################################
# XOR using given key (encrypt or decrypt)
def enc_dec(key, data):
    list_encrypted = []
    for letter in data:
        list_encrypted.append(chr(ord(letter) ^ key))
    return "".join(list_encrypted)
##########################################

# A --> B
#    B is giant for A:
#    A needs to bring a present to B)
class MemberInfo:
    def __init__(self, name, phone_number, giant=None):
        self.name = name
        self.phone_number = phone_number
        self.giant = giant

    def send_sms(self):
        twillo_client = Client(ACCOUNT_SID, AUTH_TOKEN)
        body = SMS_BODY.format(self.name, self.giant.name)
        message = twillo_client.messages.create(body=body, to="+"+self.phone_number, messaging_service_sid=MESSAGING_SERVICE_SID)

    def __str__(self):
        return "{}: {} --> {}".format(self.name, self.phone_number, self.giant.name)

# Shuffle member list
# A --> B --> C --> D
# ^_________________|
def shuffle_members_and_set_giants(list_members):
    random.shuffle(list_members)  # shuffle in place
    for i in range(len(list_members) - 1):
        list_members[i].giant = list_members[i + 1]
    list_members[-1].giant = list_members[0]

# FullName, Phone Number
# John Doe, 05050505550
def read_members_db(file_path_db):
    list_name = []
    with open(file_path_db, 'r') as file_db:
        lines = file_db.readlines()
        for line in lines:
            name, phone_number = line.split(",")
            member = MemberInfo(name=name.strip(), phone_number=phone_number.strip())
            list_name.append(member)
    return list_name

def save_results_encrypted(file_path_secret, list_members):
    with open(file_path_secret, "wb") as file_output:
        # generate random key and store as first byte
        key = random.randrange(255)
        file_output.write(chr(key))
        # encrypt and store in ourput file
        for member in list_members:
            print("\t {}".format(member))
            plain_text = str(member) + "\n"
            encrypted_text = enc_dec(key=key, data=plain_text)
            file_output.write(encrypted_text)

def main():
    if len(sys.argv) == 3:
        print("Reading arguments..")
        file_path_name_list = sys.argv[1]
        file_path_updated_secret_santa = sys.argv[2]
        print("Reading database..")
        list_members = read_members_db(file_path_name_list)
        print("setting giant and dwarfs..")
        shuffle_members_and_set_giants(list_members)
        print("Write encrypted results to file..")
        save_results_encrypted(file_path_updated_secret_santa, list_members)
        print("Send SMS..")
        for member in list_members:
            member.send_sms()

    elif len(sys.argv) == 2:
        print("Decrypting output file..")
        with open(sys.argv[1], "rb") as f:
            encrypted_data = f.read()
            key = ord(encrypted_data[0])
            print(enc_dec(key=key, data=encrypted_data[1:]))

    else:
        print("Error! Usage: {} DB OUTPUT".format(sys.argv[0]))

if __name__ == "__main__":
    main()
