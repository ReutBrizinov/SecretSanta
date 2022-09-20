# SecretSanta
This is a small project in python I created for my family's annual secret santa game, we do every year.  

The goal of this project is to automatically generate secret santas (Dwarf-Giant pairs) so we could all participate without anyone knowing the pairs. The script receives two arguments, one for the input database and one for the output encrypted secret santa log. Then, the script will randomly choose dwarf-giant pairs and will send SMS to everyone with their randomly selected giants. In addition, it will store the results encrypted (XOR encryption with a random key) so no one will be able to see the results without decrypting it first (in case needed).

I'm using Twilio API to send the SMS.


## Example Command Line
`python.exe secret_santa.py path_to_db path_to_output_file`

## Demo
![WhatsApp Image 2022-09-20 at 4 33 18 PM](https://user-images.githubusercontent.com/97907356/191303825-e08b93d3-94d0-435d-8ff4-376cd5a0019f.jpeg)


## Example Database
```
John Doe1, 97200000000
John Doe2, 97200000000
John Doe3, 97200000000
John Doe4, 97200000000
John Doe5, 97200000000
John Doe6, 97200000000
John Doe7, 97200000000
```


## Encryption Scheme
Simple one-byte XOR key which is randomly selected and stored as the first byte of the output file
