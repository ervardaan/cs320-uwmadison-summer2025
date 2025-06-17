# Jupyter

1. Connect via SSH (or the Google Cloud Console) to your virtual machine.

2. Before we install Jupyter, let's get pip.  Run the following:

Please run the commands one at a time so if an error occurs, you are able to catch it. 

- `sudo apt update`

- `sudo apt upgrade`

- `sudo apt install python3-pip`

If prompted, enter "Y" (for yes) when prompted.  If you're using an
international keyboard, be careful about what mode you're typing in --
we've heard that sometimes a character that looks like a "Y" to a
human isn't recognized by the installer.  If prompted about services (as below), just hit the ENTER key to accept the recommendation:

<img src="img/28.png" width=400>

The `apt` program lets you install software on an Ubuntu system; think
of it like `pip`, for more general (you can install stuff not related
to Python).  Putting `sudo` in front of the command means "do this as
a super user".  You're signed in as a regular user, without permission
to install software by default, so you'll use `sudo` often for
installing tools and other tasks.

You might be prompted with a "Restarting services" menu after running `sudo apt upgrade`.  If so, enter "9". 

<img src="img/31.png" width=700>

3. Now let's use pip3 to install Jupyter (don't use sudo for this one):

```
pip3 install jupyterlab==3.4.5 MarkupSafe==2.0.1
```

4. When you start Jupyter notebook remotely, you'll want to set a
password for connecting to it.  Make it a good one, or anybody will be
able to take over your VM! (Whenever you need to enter something, like a password, 
in the terminal, don't worry if nothing is appearing as you're typing. Your keystrokes 
are still registering; the terminal just isn't displaying them!) 
Run the following:

```
python3 -m jupyterlab password
```

**Important!** Choose a strong password.  Anybody on the Internet can
  guess your password an unlimited number of times.  Most semesters at
  least one student loses their VM to malicious actors.

5. Now let's start Jupyter.  Run the following:

```
nohup python3 -m jupyterlab --no-browser --ip=0.0.0.0 --port=2020 &
```

You can now close the terminal window.

6. Now, open up a new browser window, and type `IP:2020` for the URL
(IP should be the External IP of the virtual machine).  You can enter
the same password that you set in step 4:

<img src="img/26.png" width=600>

7. After you login, make sure the setup works (e.g., you can create a
notebook and run code).

**Before continuing:
Make sure that you have followed the directions in git-workflow directions and cloned your repository.**

8. Assuming you have already completed the git-workflows directions, you will be able to run the following steps to install the remaining dependencies for CS320. If not, please go into the git-workflows section of GitLab and complete those steps.

9. Run the following commands to install the remaining necessary dependencies for CS320.

```
# cd into the installation directory
cd labs-and-projects/installation
```

Run the following command to ensure that you have the correct permissions to execute the script `cs-320-requirements.sh`:

```
chmod +x cs-320-requirements.sh
```

```
# execute the requirements.sh file
./cs-320-requirements.sh
```


Good work on getting Jupyter running on your virtual machine!  We
suggest you bookmark the login page so you can come back to it later.

