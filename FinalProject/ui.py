# Manush Murali
# mpmurali@uci.edu
# 14568752

# Shreyas V Chandramouli
# svchand1@uci.edu
# 70688884

# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.



# Class, Module, & Library Imports
import tkinter as tk
from tkinter import Message, Toplevel, ttk, filedialog
from tkinter.constants import DISABLED
from tkinter.font import BOLD, NORMAL
from tkinter import *
from tkinter import simpledialog
from pathlib import Path
from urllib import request,error
from functools import partial
from Profile import Messages, Profile
from Profile import Post
from ds_messenger import DirectMessenger
from ds_messenger import DirectMessage
import json, time, os
import ds_protocol 
import re




class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._posts = [Messages]
        self._recs = []
        self._other_user = ""
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    def get_login_details(self, username: str, password: str):
        """
        Gets the login details of the user who is accessing the messenger.
        """
        self._username = username
        self._password = password
        self._finalmsg = ""
    
    def node_select(self, event=None):
        """
        Updates the entry_editor with the full post entry when the corresponding node in the posts_user
        is selected.
        """

        try:
            index = int(self.posts_tree.selection()[0])
            self.entry_frame.configure(state=NORMAL)
            self.entry_frame.delete(1.0, "end")
            rec = self._recs[index]
            self._other_user = rec
            self.set_messages(rec)
            return rec
        except:
            index = 0
            self.entry_frame.configure(state=NORMAL)
            self.entry_frame.delete(1.0, "end")
            rec = self._recs[index]
            self._other_user = rec
            self.set_messages(rec)
            return rec

    def set_messages(self, recipient):
        user = ""
        msg_list = []
        self.entry_frame.config(state= NORMAL) 
        self.entry_frame.delete(1.0,END)
        for message_obj in self._select_callback._messages:
            if(message_obj.otheruser==recipient):
                for i in message_obj["sent_messages"]:
                    msg_list.append(i)
                for i in message_obj["received_messages"]:
                    msg_list.append(i)
        for i in msg_list:
            for message_obj in self._select_callback._messages:
                if(i.get_recipient() == recipient):
                    if(i in message_obj["sent_messages"]):
                        user = self._username
                    elif(i in message_obj["received_messages"]):
                        user = recipient 

            self.insert_message(user, i.get_message())
    
    def insert_message(self, user, message):
        """
        Inserts a single message into the entry editor after send message button is clicked
        """
        self.entry_frame.configure(state = NORMAL)
        final_msg  = f"{user}: {message}\n"
        self.entry_frame.insert(END, final_msg)             
        self.entry_frame.configure(state = DISABLED)
        self.entry_frame.see(END)
    
    def get_text_entry(self) -> str:
        """
        Returns the text that is currently displayed in the entry_editor widget.
        """
        return self.entry_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        """
        Sets the text to be displayed in the entry_editor widget.
        """
        self.entry_editor.delete(0.0, "end")
        self.entry_editor.insert(0.0, text)

    def set_messenger_entry(self, text:str):
        """
        Sets the text to be displayed in the entry_frame widget.
        """
        self.entry_frame.delete(0.0, "end")
        self.entry_frame.insert(0.0, text)
    
    def set_posts(self, messages:list):
        """
        Populates the self._posts attribute with posts from the active DSU file.
        """
        self._posts = []
        for i in messages:
            self.insert_user(i)     

    def insert_user(self, message:Messages):
        """
        Inserts a single post to the post_user widget.
        """
        if (message.otheruser not in self._recs):
            self._recs.append(message.otheruser)
            id = len(self._recs) - 1 #adjust id for 0-base of treeview widget
            self._insert_user_tree(id, message)

    def reset_ui(self):
        """
        Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DSU file is loaded, for example.
        """
        self.set_text_entry("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    def _insert_user_tree(self, id, message:Messages):
        """
        Inserts a post entry into the posts_user widget.
        """
        rec = message.otheruser
        self.posts_tree.insert('', id, id, text=rec)      
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame.
        """
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        self.editor_frame = tk.Frame(master=self, bg="#28c1c1")
        self.editor_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, pady=5)

        self.entry_editor = tk.Text(self.editor_frame, height=5, bg='#2c2c31', fg='white', font=100, highlightbackground="white", highlightthickness=3)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=5, pady=5)
        
        self.entry_frame = tk.Text(master=self.editor_frame, height=25, bg="#2c2c31", fg='white', font=100, highlightbackground="white")
        self.entry_frame.configure(state=DISABLED)
        self.entry_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=5, pady=5)
        
        scroll_frame = tk.Frame(master=self.entry_frame, bg="blue", width=5)
        scroll_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, save_callback=None, add_callback=None, mode_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._add_callback = add_callback
        self._mode_callback = mode_callback
        self.b = False
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        
    def save_click(self):
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._save_callback is not None:
            self._save_callback()
    
    def add_click(self):
        """
        Calls the callback function specified in the add_callback class attribute, if
        available, when the add_button has been clicked.
        """
        if self._add_callback is not None:
            self._add_callback()

    def mode_click(self):
        """
        Calls the callback function specified in the mode_callback class attribute, if
        available, when the mode_button has been clicked.
        """
        if self._mode_callback is not None:
            self._mode_callback()
    
    def set_status(self, message, color):
        """
        Updates the text that is displayed in the footer_label widget.
        """
        if(color == "green"):
            self.footer_label.configure(text=message, fg='green')
        elif(color == "red"):
            self.footer_label.configure(text=message, fg='red')
    
    def _draw(self):        
        """
        Call only once upon initialization to add widgets to the frame.
        """
        save_button = tk.Button(master=self, text="Send", width=10, highlightbackground="#48b8b6")
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        
        adduser_button = tk.Button(master=self, text="Add User", width=10, highlightbackground="#48b8b6")
        adduser_button.configure(command=self.add_click)
        adduser_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.darkmode_button = tk.Button(master=self, text="Light Mode", width=10, highlightbackground="#48b8b6")
        self.darkmode_button.configure(command=self.mode_click)
        self.darkmode_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.", fg='green')
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the Profile class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._current_profile = Profile()
        self._path = ""
        self._is_created = False
        self._is_logged = False
        self._token = ""
        self._id = 0
        self._is_dark = False
        self._username = ""
        self._password = ""

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def dark_mode(self):
        """
        Sets the mode of the messegnger from dark mode to light mode and vice versa upon clicking of the mode_button.
        """
        if (self._is_dark is True):
            self.footer.darkmode_button.configure(text="Light Mode")
            self.body.entry_frame.configure(state=NORMAL)
            self.body.entry_editor.configure(bg='#2c2c31', fg='white')
            self.body.entry_frame.configure(bg='#2c2c31', fg='white')
            self.body.editor_frame.configure(bg='#28c1c1')
            self.body.entry_frame.configure(state=DISABLED)
            self._is_dark = False
        elif (self._is_dark is False):
            self.footer.darkmode_button.configure(text="Dark Mode")
            self.body.entry_frame.configure(state=NORMAL)
            self.body.entry_editor.configure(bg='#e0f8dc', fg='black')
            self.body.entry_frame.configure(bg='#e0f8dc', fg='black')
            self.body.editor_frame.configure(bg='#000080')
            self.body.entry_frame.configure(state=DISABLED)
            self._is_dark = True
    
    def new_recipient(self):
        """
        Creates a new user (DSU File) when the add_button (Add User) item is clicked.
        """
        username = tk.simpledialog.askstring(title="New Recipient", prompt="Receiver Name:-")
        if(username != None):
            if(username not in self.body._recs):
                message = Messages(otheruser=username, sent_messages=[], received_messages=[])
                self._current_profile._messages.append(message)
                self._current_profile.save_profile(self._path)
                self.body.insert_user(message)
                self.footer.set_status("Recipient Added", "green")
                self.is_created = True
            else:
               self.footer.set_status("Recipient Already Exists", "red") 
        else:
            self.footer.set_status("No Recipient Name Entered", "red")
     
    def user_login(self, username:str, password:str):
        """
        Allows the user to login using a username and password to a third-party server on the internet. 
        Stores the username to bring all the recipients to the UI.
        """
        self._username = username
        self._password = password
        msg = ds_protocol.join_command(self._username, self._password)    
        p = re.compile('(?<!\\\\)\'')
        someString = p.sub('\"', msg)
        sendingwithjson = json.loads(someString)
        ds = DirectMessenger(username=self._username, password=self._password)
        js_msg = ds.senddata(server="168.235.86.101", port=3021, username=self._username, password=self._password, message=sendingwithjson)
        ds_msg = json.loads(js_msg)
        msg = ds_msg['response']['message']
        self._token = ds_msg['response']['token']
        path_name = os.getcwd()
        final_path = Path(f"{path_name}/{self._username}.dsu")
        path_name = str(final_path)
        self._path = path_name 
        if (final_path.exists() == False):
            final_path.touch(exist_ok = True)
            self._current_profile = Profile(username=self._username, password=self._password)
            self._current_profile.save_profile(path_name)
        else:
            self._current_profile.load_profile(path_name)
            self.body.set_posts(self._current_profile.get_messages())
            if (len(self._current_profile.get_messages()) != 0):
                self.is_created = True
        self.footer.set_status(msg, "green")
        self._is_logged = True
            
    
    def close(self):
        """
        Closes the program when the 'Close' cascade item is clicked.
        """
        self.root.destroy()

    def save_post(self):
        """
        Saves the text currently in the entry_editor widget to the active user (DSU file) 
        in the form of a message post into a dictionary. Sends and receives messages from another 
        user using the third-party server and displays them in the entry_frame widget.
        """
        message = self.body.get_text_entry()
        self.body._other_user = self.body.node_select()
        self.body.insert_message(self._username, message)
        self.body.set_text_entry("")
        ds = DirectMessenger(username=self._username, password=self._password)
        x = ds.send(message, self.body._other_user)
        if (x == True):
            self.footer.set_status("Message Sent", "green")
        else:
            self.footer.set_status("Message Unsuccessful", "red")
        for i in self._current_profile._messages:
            if (i.otheruser == self.body._other_user):
                p = Post()
                p.set_message(message)
                p.set_recipient(self.body._other_user)
                i.add_sent_msg(p)
                self._current_profile.save_profile(self._path)
        self.retrieve_messages()
        # elif(self._is_logged==False):
        #     self.body.set_text_entry("")
        #     self.footer.set_status("First Login or Sign Up to Send Messages", "red")
        # elif(self._is_created==False):
        #     self.body.set_text_entry("")
        #     self.footer.set_status("Add an User to Send Messages", "red")
        
    def retrieve_messages(self):
        """
        Retrieves messages from the server.
        """
        if (self._is_logged == True):
            ds = DirectMessenger(username=self._username, password=self._password)
            msg_list = ds.retrieve_new() 
            for i in msg_list:
                p = Post()
                p.set_message(i.get_message())
                p.set_recipient(i.get_recipient())
                p.set_time(i.get_time())
                print(i.get_recipient())
                if (i.get_recipient() not in self.body._recs):
                    message = Messages(otheruser=i.get_recipient(), sent_messages=[], received_messages=[])
                    self.body.insert_user(message)
                    self._current_profile._messages.append(message)
                    x = self._current_profile._messages[len(self._current_profile._messages) - 1]
                    x.add_receieved_msg(p)
                    self._current_profile.save_profile(self._path)
                else:
                    for j in self._current_profile._messages:
                        if (i.get_recipient() == j.otheruser):
                            j.add_receieved_msg(p)
                            self.body.insert_message(i.get_recipient(), i.get_message())
            self.root.after(2000,self.retrieve_messages)

    
    def edit_login_variables(self, username, password, login_window):
        """
        Sets the new username and password to the respective attributes of the Profile() class.
        """
        new_username = username.get()
        new_password = password.get()
        self._current_profile.username = str(new_username)
        self._current_profile.password = str(new_password)
        self.body.get_login_details(self._current_profile.username, self._current_profile.password)
        self.user_login(self._current_profile.username, self._current_profile.password)
        login_window.destroy()   
    
    def edit_login(self):
        """
        Generates the tKinter User Interface for editing the username and password of the profile.
        """
        login_window = Toplevel(bg='#2c2c31')
        login_window.geometry("480x360")
        login_window.title("Login")
        username = tk.StringVar()
        password = tk.StringVar()
        tk.Label(login_window, text="", bg='#2c2c31').pack()
        tk.Label(login_window, text="", bg='#2c2c31').pack()
        tk.Label(login_window, text="", bg='#2c2c31').pack()
        tk.Label(login_window, text="", bg='#2c2c31').pack()    
        tk.Label(login_window, text="Username", bg='#2c2c31', fg='white').pack()    
        username_entry = tk.Entry(login_window, textvariable=username, bg='#2c2c31', fg='white')
        username_entry.pack()
        tk.Label(login_window, text="Password", bg='#2c2c31', fg='white').pack()
        password__entry = tk.Entry(login_window, textvariable=password, show= '*', bg='#2c2c31', fg='white')
        password__entry.pack()
        tk.Label(login_window, text="", bg='#2c2c31').pack()
        edit_login_variables = partial(self.edit_login_variables, username, password, login_window)
        tk.Button(login_window, text="Save", width=10, height=1,command=edit_login_variables, bg='white', fg='black').pack()
    
    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame.
        """
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_bar.add_cascade(menu=menu_settings, label='Profile')
        menu_file.add_command(label='Close', command=self.close)
        menu_settings.add_command(label='Login', command=self.edit_login)

        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.footer = Footer(self.root, save_callback=self.save_post, add_callback=self.new_recipient, mode_callback=self.dark_mode)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    """
    Main Function
    """
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Messenger Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    mainapp = MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.after(2000, mainapp.retrieve_messages) 
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
    
