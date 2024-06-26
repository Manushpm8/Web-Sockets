# Manush Murali
# mpmurali@uci.edu
# 14568752

# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.


# Class, Module, & Library Imports
import tkinter as tk
from tkinter import Toplevel, ttk, filedialog
from tkinter.font import BOLD
from tkinter import simpledialog
from pathlib import Path
from urllib import request,error
from functools import partial
from Profile import Message, Profile
from Profile import Messageß
import json, time, os
import ds_client
import ds_protocol



"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._messages = [Message]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    """
    Updates the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._posts[index].entry
        self.set_text_entry(entry)
    
    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        # TODO: Write code to that deletes all current text in the self.entry_editor widget
        # and inserts the value contained within the text parameter.
        self.entry_editor.delete(0.0, "end")
        self.entry_editor.insert(0.0, text)
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_messages(self, messages:list):
        # TODO: Write code to populate self._posts with the post data passed
        # in the posts parameter and repopulate the UI with the new post entries.
        # HINT: You will have to write the delete code yourself, but you can take 
        # advantage of the self.insert_posttree method for updating the posts_tree
        # widget.
        self._messages = []
        for i in self.messages_tree.get_children():
            self.posts_tree.delete(i)
        for i in posts:
            self._posts.append(i)
            self.insert_post(i)    

    """
    Inserts a single post to the post_tree widget.
    """
    def insert_post(self, post: Post):
        self._posts.append(post)
        id = len(self._posts) - 1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, post)

    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_entry("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_post_tree(self, id, post: Post):
        entry = post.entry
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.        
        if len(entry) > 25:
            entry = entry[:24] + "..."
        self.posts_tree.insert('', id, id, text=entry)
        self.entry_editor.configure(state=tk.NORMAL)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0, bg='#2c2c31', fg='white', font=100)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, online_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using the get() function:
        # chk_value = self.is_online.get()
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
        self.b = False
    
    """
    Calls the callback function specified in the online_callback class attribute, if
    available, when the chk_button widget has been clicked.
    """
    def online_click(self):
        # TODO: Add code that implements a callback to the chk_button click event.
        # The callback should support a single parameter that contains the value
        # of the self.is_online widget variable.
        if self._online_callback is not None:
            self._online_callback(self.is_online.get())

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()
        
    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message, color):
        if(color == "green"):
            self.footer_label.configure(text=message, fg='green')
        elif(color == "red"):
            self.footer_label.configure(text=message, fg='red')
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        save_button = tk.Button(master=self, text="Save Post", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        self.chk_button.configure(command=self.online_click) 
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.footer_label = tk.Label(master=self, text="Ready.", fg='green')
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = NaClProfile()
        self._current_profile.generate_keypair()
        self._is_online = False

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self._profile_filename = None
        self._path = ""
        self.is_created = False
        self.is_opened = False

    """
    Creates a new DSU file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        profile_filename = filename.name

        # TODO Write code to perform whatever operations are necessary to prepare the UI for
        # a new DSU file.
        # HINT: You will probably need to do things like generate encryption keys and reset the ui.
        self.body.reset_ui()
        self._profile_filename = filename.name
        self._current_profile = NaClProfile()
        self._current_profile.generate_keypair()
        self.is_created = True
    
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self):
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        # TODO: Write code to perform whatever operations are necessary to prepare the UI for
        # an existing DSU file.
        # HINT: You will probably need to do things like load a profile, import encryption keys 
        # and update the UI with posts.
        self.body.reset_ui()
        self._profile_filename = filename.name
        self._current_profile = NaClProfile()
        self._current_profile.load_profile(self._profile_filename)
        self._current_profile.import_keypair(self._current_profile.keypair)
        self.body.set_posts(self._current_profile.get_posts())
        self.is_opened = True

    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """
    def save_profile(self):
        # TODO: Write code to perform whatever operations are necessary to save a 
        # post entry when the user clicks the save_button widget.
        # HINT: You will probably need to do things like create a new Post object,
        # fill it with text, add it to the active profile, save the profile, and
        # clear the editor_entry UI for a new post.
        # This might also be a good place to check if the user has selected the online
        # checkbox and if so send the message to the server.
        if (self.is_created==True or self.is_opened==True):
            post = Post(self.body.get_text_entry())
            self.body.insert_post(post)
            self.footer.set_status("Succesfully Saved", "green")
            self._current_profile.add_post(post)
            self._current_profile.save_profile(self._profile_filename)
            self.body.set_posts(self._current_profile.get_posts())
            self.body.set_text_entry("")
            self.online_changed(self._is_online)
            if self._is_online is True:
                self.publish(post)
                self.footer.set_status("Post Published to DS Server", "green")
            else:
                self.footer.set_status("Post Successfully Saved", "green")
        elif (self.is_created==False and self.is_opened==False):
            self.body.set_text_entry("")
            self.footer.set_status("First Create or Open a file to Add Post", "red")

    """
    Sends the posts to the DS Server in a encrypted format to publish the posts. The encrypted messages are decrypted by the DS Server.
    """
    def publish(self, post:Post):
            self.update()
            srv = "168.235.86.101"
            port = 3021
            usr = "Manushpm8"
            pas = "manusara"
            js = ds_protocol.join_command(usr, pas, self._current_profile.public_key)
            js_msg = ds_client.communicator(srv, port, js)
            ds_msg = json.loads(js_msg)
            tok = ds_msg["response"]["token"]
            po = Post(entry = post, timestamp = time.time())
            ts = str(po.get_time())
            u = NaClDSEncoder()
            p_key = self._current_profile.public_key
            pos = self._current_profile.post_decrypter(str(post.get_entry()), u.encode_public_key(p_key))
            post = self._current_profile.encrypt_entry(pos, tok).decode(encoding = "UTF-8")
            js = ds_protocol.post_command(self._current_profile.public_key, post, ts)
            js_msg = ds_client.communicator(srv, port, js)
    
    """
    A callback function for responding to changes to the online chk_button.
    """
    def online_changed(self, value:bool):
        # TODO: 
        # 1. Remove the existing code. It has been left here to demonstrate
        # how to change the text displayed in the footer_label widget and
        # assist you with testing the callback functionality (if the footer_label
        # text changes when you click the chk_button widget, your callback is working!).
        # 2. Write code to support only sending posts to the DSU server when the online chk_button
        # is checked.
        if value == 1:
            self.footer.set_status("Online", "green")
            self._is_online = True
        else:
            self.footer.set_status("Offline", "red")
            self._is_online = False     

    """
    Sets the new username and password to the respective attributes of the Profile() class.
    """
    def edit_settings_variables(self, username, password, settings_window):
        new_username = username.get()
        new_password = password.get()
        self._current_profile.username = new_username
        self._current_profile.password = new_password
        self._current_profile.save_profile(str(self._profile_filename))
        self.footer.set_status("Succesfully Saved", "green")
        settings_window.destroy()   
    
    """
    Generates the tKinter User Interface for editing the username and password of the profile.
    """
    def edit_settings(self):
        if (self.is_created==True or self.is_opened==True):
            settings_window = Toplevel(bg='#2c2c31')
            settings_window.geometry("480x360")
            settings_window.title("Settings")
            username = tk.StringVar()
            password = tk.StringVar()
            current_username = self._current_profile.username
            current_password = self._current_profile.password
            if(current_username is None or current_username.strip()==""):
                current_username = "No Username Set!"
            if(current_password is None or current_password.strip()==""):
                current_password = "No Password Set!"
            tk.Label(settings_window, text="", bg='#2c2c31').pack()
            tk.Label(settings_window, text=f"Username: {current_username}", bg='green', fg='white').pack()
            tk.Label(settings_window, text=f"Password: {current_password}", bg='green', fg='white').pack()
            tk.Label(settings_window, text="", bg='#2c2c31').pack()    
            tk.Label(settings_window, text="Username", bg='#2c2c31', fg='white').pack()    
            username_entry = tk.Entry(settings_window, textvariable=username, bg='#2c2c31', fg='white')
            username_entry.pack()
            tk.Label(settings_window, text="Password", bg='#2c2c31', fg='white').pack()
            password__entry = tk.Entry(settings_window, textvariable=password, show= '*', bg='#2c2c31', fg='white')
            password__entry.pack()
            tk.Label(settings_window, text="", bg='#2c2c31').pack()
            edit_settings_variables = partial(self.edit_settings_variables, username, password, settings_window)
            tk.Button(settings_window, text="Save", width=10, height=1,command=edit_settings_variables, bg='white', fg='black').pack()
        elif (self.is_created==False and self.is_opened==False):
            self.body.set_text_entry("")
            self.footer.set_status("First Create or Open a file to access File Settings", "red")
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_bar.add_cascade(menu=menu_settings, label='Settings')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        menu_settings.add_command(label='File Settings', command=self.edit_settings)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback=self.online_changed)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


"""
Main Function
"""
if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
    