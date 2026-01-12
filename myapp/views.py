# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .aes import encrypt, decrypt
from .ecc import *
from .models import Encryptedmodel, Filerequestmodel
from web3 import Web3
import os, random, base64, json
from django.utils import timezone

# ------------------ Firebase ------------------
db = settings.FIRESTORE_DB

# ------------------ Templates ------------------
INDEXPAGE = "index.html"
LOGINPAGE = 'login.html'
REGPAGE = 'reg.html'
VIEWOWNERACPT = 'viewalluser.html'
CLOUDHOMEPAGE = 'cloudhome.html'
USERHOMEPAGE = 'userhome.html'
ENCRYPTDATAPAGE = "encrypt.html"
VIEWFILESPAGE = "viewfiles.html"
FILEREQUESTPAGE = "filerequest.html"
DECRYPTPAGE = "decryptpage.html"
VIEWMYFILESPAGE = "viewmyfiles.html"
VIEWCLOUDFILESPAGE = "cloudfile.html"
VIEWFILESREQUESTPAGE = 'filerequestcloud.html'

# ------------------ Blockchain ------------------
ONE_ACCOUNT = "0xeed3d48a9C4c76671FeD8F759AAc5F54b5ec6A84"
USER_CONTRACT_ADDRESS = "0x33a3BD2e4826738d3Fd9dc918f990d7Af23B903F"
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
with open("Blocks/build/contracts/UserContract.json") as abi_file:
    abi = json.load(abi_file)["abi"]
    UserContract = web3.eth.contract(address=USER_CONTRACT_ADDRESS, abi=abi)

# ------------------ Index ------------------
def index(request):
    return render(request, INDEXPAGE)

def viewfilesrequest(req):    
    data = Filerequestmodel.objects.all()
    return render(req,VIEWFILESREQUESTPAGE,{'filedata':data})
    # return render(req,VIEWFILESREQUESTPAGE,{'encrypted_data':encrypted_data,'file':'nofile'})

# ------------------ Login ------------------
def login(request):
    if request.method == "POST":
        login_type = request.POST.get("login_type", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")

        if login_type == "cloudserver":
            if email == "cloud@gmail.com" and password == "cloud":
                request.session["email"] = email
                request.session["name"] = "Cloud Server Admin"
                return render(request, CLOUDHOMEPAGE)
            messages.error(request, "Invalid cloud credentials.")
            return render(request, LOGINPAGE)

        try:
            id, name, email, contact, address, status = UserContract.functions.loginFunction(
                email, password
            ).call({"from": ONE_ACCOUNT})

            if status == "Deactivated":
                messages.error(request, "User not verified.")
            elif name != "Invalid Users":
                request.session["email"] = email
                request.session["name"] = name
                request.session["useremail"] = email
                return render(request, USERHOMEPAGE, {"user": name})
            else:
                messages.error(request, "Invalid user credentials.")
        except Exception as e:
            messages.error(request, f"Login failed: {e}")

    return render(request, LOGINPAGE)

# ------------------ User Registration ------------------
def user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("password2")
        contact = request.POST.get("contact")
        address = request.POST.get("address")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, REGPAGE)

        val = UserContract.functions.checkEmail(email).call({"from": ONE_ACCOUNT})

        if val == "Success":
            UserContract.functions.AddUsers(
                name, email, password, contact, address, "Deactivated"
            ).transact({"from": ONE_ACCOUNT, "gas": 600000})
            messages.success(request, "Registration Successful.")
            return render(request, LOGINPAGE)
        else:
            messages.warning(request, "Email already exists.")
            return redirect("user")

    return render(request, REGPAGE)

# ------------------ Cloud Home ------------------
def cloudhome(request):
    return render(request, CLOUDHOMEPAGE)

# ------------------ View Users ------------------
def viewusers(request):
    ids, names, emails, contacts, addresses, statuses = UserContract.functions.getUsersActivated(
        "Deactivated"
    ).call({"from": ONE_ACCOUNT})

    usersdata = []
    for i in range(len(ids)):
        if ids[i] != 0:
            usersdata.append({
                "id": ids[i],
                "name": names[i],
                "email": emails[i],
                "contact": contacts[i],
                "address": addresses[i],
                "status": statuses[i]
            })

    return render(request, VIEWOWNERACPT, {"usersdata": usersdata})

def acceptuser(request, id):
    UserContract.functions.upldateState(int(id), "Activate").transact({"from": ONE_ACCOUNT})
    messages.success(request, "User activated.")
    return redirect("viewusers")

# ------------------ Encrypt Data ------------------
def encryptdata(request):
    if request.method == "POST":
        data = request.POST.get('message', '')
        algorithm = request.POST.get('algorithm', '')

        if not data:
            messages.warning(request, "No data provided to encrypt.")
            return render(request, ENCRYPTDATAPAGE)

        try:
            if algorithm == "aes":
                randomkey = f"{random.randint(0, 999999):06}"
                aes_key = randomkey.encode()
                encrypted_bytes = encrypt(data.encode(), aes_key)
                encrypted_data = base64.b64encode(encrypted_bytes).decode()
                decrypted = decrypt(base64.b64decode(encrypted_data), aes_key).decode()
                enc_path = "static/AES/encryptedfiles/example.txt"
                dec_path = "static/AES/files/example.txt"
                os.makedirs(os.path.dirname(enc_path), exist_ok=True)
                os.makedirs(os.path.dirname(dec_path), exist_ok=True)
                with open(enc_path, "w") as f: f.write(encrypted_data)
                with open(dec_path, "w") as f: f.write(decrypted)

                # Store in SQLite3
                Encryptedmodel.objects.create(
                    useremail=request.session.get('useremail', ''),
                    textcontent=encrypted_data,
                    filekey=aes_key,
                    encfilepath=enc_path,
                    decfilepath=dec_path
                )
                # Firebase backup
                db.collection("encrypted_files").add({
                    "useremail": request.session.get('useremail', ''),
                    "textcontent": encrypted_data,
                    "filekey": randomkey,
                    "encfilepath": enc_path,
                    "decfilepath": dec_path,
                    "algorithm": "aes",
                    "datetime": timezone.now().isoformat()
                })

            elif algorithm == "ecc":
                fkey = Fernet.generate_key()
                f = Fernet(fkey)
                encrypted_data = f.encrypt(data.encode()).decode()
                decrypted = f.decrypt(encrypted_data.encode()).decode()
                enc_path = "static/ECC/encryptedfiles/example.txt"
                dec_path = "static/ECC/files/example.txt"
                os.makedirs(os.path.dirname(enc_path), exist_ok=True)
                os.makedirs(os.path.dirname(dec_path), exist_ok=True)
                with open(enc_path, "w") as f: f.write(encrypted_data)
                with open(dec_path, "w") as f: f.write(decrypted)

                Encryptedmodel.objects.create(
                    useremail=request.session.get('useremail', ''),
                    textcontent=encrypted_data,
                    filekey=fkey.decode(),
                    encfilepath=enc_path,
                    decfilepath=dec_path
                )
                db.collection("encrypted_files").add({
                    "useremail": request.session.get('useremail', ''),
                    "textcontent": encrypted_data,
                    "filekey": fkey.decode(),
                    "encfilepath": enc_path,
                    "decfilepath": dec_path,
                    "algorithm": "ecc",
                    "datetime": timezone.now().isoformat()
                })
            else:
                messages.warning(request, "Select an encryption algorithm.")
                return render(request, ENCRYPTDATAPAGE)

            messages.success(request, "File encrypted & saved (SQLite3 + Firebase).")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, ENCRYPTDATAPAGE)

# ------------------ View Files ------------------
def viewfiles(request):
    encrypted_data = Encryptedmodel.objects.exclude(useremail=request.session.get('useremail', ''))
    return render(request, VIEWFILESPAGE, {'encrypted_data': encrypted_data, 'file':'nofile'})

def viewcloudfiles(request):
    encrypted_data = Encryptedmodel.objects.all()
    return render(request, VIEWCLOUDFILESPAGE, {'encrypted_data': encrypted_data, 'file':'nofile'})

def viewfilesrequest(request):
    data = Filerequestmodel.objects.all()
    return render(request, VIEWFILESREQUESTPAGE, {'filedata': data})

# ------------------ Send File Request ------------------
# ------------------ Send File Request ------------------
def sendrequest(request, id):
    # Fetch the encrypted file
    data = Encryptedmodel.objects.filter(id=id).first()
    if not data:
        messages.error(request, "File not found.")
        return redirect("viewfiles")

    try:
        # Ensure filekey is a string before saving
        filekey_value = data.filekey
        if isinstance(filekey_value, bytes):
            filekey_value = filekey_value.decode()

        # 1️⃣ Store in SQLite3
        filerequest = Filerequestmodel.objects.create(
            fileid=data.id,
            useremail=data.useremail,
            textcontent=data.textcontent,
            filekey=filekey_value,
            receiveremail=request.session.get('useremail', ''),
            status="pending"
        )
        filerequest.save()  # commit to SQLite

        # 2️⃣ Store in Firebase
        db.collection("filerequest").add({
            "fileid": data.id,
            "useremail": data.useremail,
            "textcontent": data.textcontent,
            "filekey": filekey_value,
            "receiveremail": request.session.get('useremail', ''),
            "status": "pending",
            "datetime": timezone.now().isoformat()
        })

        messages.success(request, "File request sent successfully (SQLite3 + Firebase).")
        print(f"Request sent for file ID: {id}")

    except Exception as e:
        messages.error(request, f"Failed to send request: {e}")

    return redirect("viewfiles")


# ------------------ View Pending Requests ------------------

def filerequest(req):
    data = Filerequestmodel.objects.filter(useremail=req.session['useremail'],status='pending')
    return render(req,FILEREQUESTPAGE,{'filedata':data})

# ------------------ Send Key ------------------
def sendkey(req,fileid):
    print(fileid)
    dc = [(i.filekey,i.receiveremail) for i in Filerequestmodel.objects.filter(fileid=fileid,useremail=req.session['useremail'],status='pending')]
    print(dc)
    
    subject = "No reply"
    cont = 'The private key to decrypt file.'
    key = dc[0][0]
    m1 = "This message is automatic generated so dont reply to this Mail"
    m2 = "Thanking you"
    m3 = "Regards"
    m4 = "Cloud Service Provider."
    Email = dc[0][1]
    print(key)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    text = cont + '\n' + key + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
    send_mail(subject, text, email_from, recipient_list,fail_silently=False,)
    dc = Filerequestmodel.objects.filter(fileid=fileid,useremail=req.session['useremail'],status='pending').last()
    dc.status = 'approved'
    dc.save()
    return redirect("filerequest")

# ------------------ View Approved Files ------------------
def decryptdata(request):
    current_user = request.session.get('useremail', '')
    data = Filerequestmodel.objects.filter(receiveremail=current_user, status='approved')
    return render(request, DECRYPTPAGE, {"filedata": data})

# ------------------ View & Decrypt File ------------------
def viewmyfiles(request, id):
    if request.method == "POST":
        filekey = request.POST.get('filekey', '')
        secret_key = filekey.encode() if isinstance(filekey, str) else filekey
        try:
            dec_path = Encryptedmodel.objects.filter(filekey=secret_key).values_list('decfilepath', flat=True).first()
            if not dec_path:
                raise ValueError("Invalid Key")
            with open(dec_path, "r") as f:
                content = f.read()
            return render(request, VIEWMYFILESPAGE, {"id": id, "content": content, "files": "False"})
        except Exception:
            messages.warning(request, "Key is not valid or file missing!")
            return render(request, VIEWMYFILESPAGE, {"id": id, "files": "True"})
    return render(request, VIEWMYFILESPAGE, {"id": id, "files": "True"})
