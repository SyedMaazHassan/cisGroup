from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from django.contrib.auth.models import User, auth
from django.contrib import messages
import sqlite3

# Create your views here.


def chatting(request):
    if request.method == "POST":
        msg = request.POST['userMsg']
        print(request.user.first_name)
        print("============>", msg)

        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("INSERT INTO myweb_mymsg(sent_by, msg) VALUES {}".format(str((request.user.first_name, msg))))
        conn.commit()
        return redirect("discussion")

def chat(request):
    return redirect("discussion")

def discussion(request):
    try:
        all_msgs = myMsg.objects.all()

        a = str(getSkills_by_id(request.user.id))
        if len(a) > 5:
            a = a[5:]

        context = {
            'notify': get_all_notifications(),
            'msgs': all_msgs,
            'user': request.user,
            'skill': a,

        }
        return render(request, "chatting.html", context)
    except:
        return redirect("login")

def dashboard(request):
    all_tasks = list(myTasks.objects.all())
    all_tasks.reverse()

    all_notifications = list(myNotification.objects.all())
    all_notifications.reverse()

    return render(request, "dashboard.html", {'notify':all_notifications, 'tasks':all_tasks})

def register(request):
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        rollNo = request.POST['rollNo']

        tempR = rollNo.split("-")

        allowed_list = [
            '18054',
            '18041',
            '18049',
            '18032',
            '18043',
            '18039',
            '18070',
            '18075',
            '18012',
            '18020',
            '18113',
            '18067',
            '18073',
            '18064'
        ]

        dept_list = ["CS", "cs", 'Cs', 'cS']

        if pass1 != pass2:
            messages.info(request, "your password doesn't match!")
            return redirect("/")
        elif len(pass1) <= 3:
            messages.info(request, "Password must be at least 4 characters")
            return redirect("/")
        elif len(tempR) != 2 or len(tempR[1]) != 5:
            messages.info(request, "Kindly! follow the pattern to enter the roll no. (CS-18054)")
            return redirect("/")
        elif tempR[0] not in dept_list:
            messages.info(request, "Sorry! only CIS students are allowed to register.")
            return redirect("/")
        elif tempR[1] not in allowed_list:
            messages.info(request, "This Roll no. is not allowed to register right now! Please! get the permission from the whatsApp group of ForTheGreaterGood (03472533106) to register here.")
            return redirect("/")
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Sorry! this email address has already been registered")
            return redirect("/")
        elif User.objects.filter(username=rollNo).exists():
            messages.info(request, "Sorry! this Roll number has already been registered")
            return redirect("/")
        else:
            my_user = User.objects.create_user(username=rollNo, email=email, password=pass1, first_name=full_name)
            my_user.save()
            #getting id of person who is registered
            ID = get_id_of(email)
            #add the row in skills for this person
            add_into_skills(ID)
            #add the row in online status
            add_into_status(ID)
            #add task column
            add_task_colmn_for(ID)
            print("user is registered successfully")
            messages.info(request, "Congratulations! You have been registered successfully")
            return redirect("login")

def do_login(request):
    if request.method == 'POST':
        entry = request.POST["emailOrPass"]
        myPass = request.POST["pass"]


        if("@" in entry) and (".com" in entry):
            conn = sqlite3.connect('db.sqlite3')
            c = conn.cursor()
            c.execute("SELECT username FROM auth_user WHERE email='{}'".format(entry))
            username = c.fetchall()
            conn.commit()


            if len(username)>0:
                username = username[0][0]
                print(username)
                user = auth.authenticate(username=username, password=myPass)
                if user:
                    auth.login(request, user)
                    make_user_online(request.user.id)
                    return redirect("tasks")

        user = auth.authenticate(username=entry, password=myPass)

        if user:
            auth.login(request, user)
            make_user_online(request.user.id)

            return redirect("tasks")
        else:
            messages.info(request, "Oops! Wrong Entries. Kindly enter the valid info.")
            return redirect("login")


def task_done(request):
    if request.method == 'POST':
        task_id = request.POST["thisTask"]
        task_id = task_id.split("-")
        print("this is the task => ", task_id)

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("UPDATE myweb_task_complete SET person_{}='1' WHERE id_task='{}'".format(request.user.id, task_id[0]))
        conn.commit()

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT skills FROM myweb_skills WHERE id_person='{}'".format(request.user.id))
        mySkills = cursor.fetchall()
        conn.commit()

        mySkills = mySkills[0][0]+"-"
        mySkills += task_id[1]


        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("UPDATE myweb_skills SET skills='{}' WHERE id_person='{}'".format(mySkills, request.user.id))
        conn.commit()
        return redirect("tasks")

def tasks(request):
    # getting
    try:
        a = str(getSkills_by_id(request.user.id))
        if len(a) > 5:
            a = a[5:]
        context = {
            'completed_task': get_completed_task(request.user.id),
            'user': request.user,
            'skill': a,
            'notify': get_all_notifications(),
            'tasks': get_all_tasks()
        }

        return render(request, 'dashboard.html', context)
    except:
        return redirect("login")

def all_members(request):
    return redirect("members")

def members(request):
    try:
        all_members_data = collect_the_data()
        main_row_data = []
        for i in all_members_data:
            if i[5] != "None":
                edited = i[5].split("-")
                temp = edited[1:]
                temp = " - ".join(temp)
            else:
                temp = i[5]
            one_person = data_collection(i[0], i[1], i[2], i[3], i[4], temp, i[6])
            main_row_data.append(one_person)

        a = str(getSkills_by_id(request.user.id))
        if len(a) > 5:
            a = a[5:]

        context = {
            'all_members': main_row_data,
            'user': request.user,
            'notify': get_all_notifications(),
            'skill': a
        }

        return render(request, 'all_members.html', context)
    except:
        return redirect("login")

def logout(request):
    try:
        make_user_offline(request.user.id)
        auth.logout(request)
        return redirect("login")
    except:
        return redirect("login")


def collect_the_data():
    all_list_data = []

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id,first_name,email,username FROM auth_user WHERE is_staff='0' ORDER BY id")
    all_data = cursor.fetchall()
    conn.commit()
    print("only is_staff=fasle", all_data)

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT isonline FROM myweb_onlinestatus ORDER BY id_person")
    all_onlines = cursor.fetchall()
    conn.commit()

    for i in range(0, len(all_data)):
        make_list = list(all_data[i])
        make_list.append(all_onlines[i][0])
        make_list.append(getSkills_by_id(make_list[0]))
        completed_task = get_completed_task(make_list[0])
        all_tasks = get_all_tasks()
        progress = (len(completed_task)/len(all_tasks))*100
        rounded_progress = round(progress, 1)
        make_list.append(rounded_progress)
        all_list_data.append(make_list)

    print(all_list_data)
    print("=====================")
    for i in all_list_data:
        print(i)
    return all_list_data


def equalize():
    all_tasks = list(myTasks.objects.all())
    all_tasks_ids = []

    for i in all_tasks:
        all_tasks_ids.append(i.id)


    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id_task from myweb_task_complete")
    all_task_complete_ids = cursor.fetchall()
    conn.commit()

    if len(all_task_complete_ids)!= len(all_tasks_ids):
        for i in range(len(all_task_complete_ids), len(all_tasks_ids)):
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO myweb_task_complete(id_task) VALUES ({})".format(all_tasks_ids[i]))
            conn.commit()

def add_task_colmn_for(id_person):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE myweb_task_complete ADD person_{} INTEGER DEFAULT 0".format(id_person))
    conn.commit()

def get_completed_task(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id_task FROM myweb_task_complete WHERE person_{}='1'".format(id))
    all_completed_task = cursor.fetchall()
    conn.commit()

    all_completed_task2 = []
    for i in all_completed_task:
        all_completed_task2.append(i[0])
    return all_completed_task2

def getSkills_by_id(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT skills FROM myweb_skills WHERE id_person='{}'".format(id))
    mySkills = cursor.fetchall()
    conn.commit()
    return mySkills[0][0]

def get_all_notifications():
    all_notifications = list(myNotification.objects.all())
    all_notifications.reverse()
    return all_notifications

def get_all_tasks():
    all_tasks = list(myTasks.objects.all())
    all_tasks.reverse()
    return all_tasks

def get_id_of(email_or_rollNo):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM auth_user WHERE (email='{}' OR username='{}')".format(email_or_rollNo, email_or_rollNo))
    myID = cursor.fetchall()
    conn.commit()
    return myID[0][0]

def add_into_skills(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO myweb_skills (id_person) VALUES ({})".format(id))
    conn.commit()

def add_into_status(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO myweb_onlinestatus (id_person) VALUES ({})".format(id))
    conn.commit()

def make_user_online(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("UPDATE myweb_onlinestatus SET isonline='True' WHERE id_person='{}'".format(id))
    conn.commit()

def make_user_offline(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("UPDATE myweb_onlinestatus SET isonline='False' WHERE id_person='{}'".format(id))
    conn.commit()

def starting(request):
    return render(request, "starting.html", {'msg':0})

def signup(request):
    # cursor = connection.cursor()
    # cursor.execute("CREATE TABLE myweb_task_complete \
    #                (id_person INTEGER)")

    # connection.commit()
    # a = User.objects.filter(email='hafizmaazhassan33@gmail.com')
    #
    # for i in range(28, 38):
    #     cursor = connection.cursor()
    #     cursor.execute("ALTER TABLE myweb_task_complete DROP COLUMN person_{}".format(i))
    #     connection.commit()
    #
    # collect_the_data()
    collect_the_data()
    equalize()
    # conn = sqlite3.connect('db.sqlite3')
    # c = conn.cursor()
    # c.execute("CREATE TABLE myweb_task_complete ([id_task] INTEGER)")
    # conn.commit()
    return render(request, "signup.html")

def login(request):
    return render(request, "starting.html", {'msg':0})
