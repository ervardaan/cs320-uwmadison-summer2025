# SSH

1. In the menu on the left, open the "Compute Engine" menu, and find "Metadata" by scrolling down.

<img src="img/13.png" width=300>

2. Go to "SSH Keys" and click "ADD SSH KEY".  There will be a box
where we need to paste a key, which we haven't generated yet.

<img src="img/14.png" width=600>

3. Open your terminal(MacOS) or PowerShell(Windows), and run the
command `ssh-keygen -t rsa`.  You should be able to just use the defaults by
hitting enter a few times (I don't recommend setting a password for
this or a passphrase). It looks like the following on a Mac, but
should work the same on Windows.  If `ssh-keygen -t rsa` isn't found, then
you should skip the rest of this section and go back to the next steps
on the [main page](README.md) for now (feel free to get help more
specific to your setup during office hours).

Note that the `ssh-keygen -t rsa` creates a "private key" on the computer
where you run it that will let you connect to your VM without a
password via SSH this semester.  If you switch computers at some
point, you'll need to revisit this part of the lab.

**Sometimes `ssh-keygen -t rsa` creates SSH keys with usernames that only consist of numbers.** 
**This is an invalid SSH key for GCP.** You can generate a new SSH key specifiying a 
username by `ssh-keygen -C USERNAME`

<img src="img/15.png" width=600>

4. Run `cat ~/.ssh/id_rsa.pub`.  Then copy the output (the part
highlighted in the following screenshot).  (If your using windows, run the command using windows powershell)

<img src="img/16.png" width=600>

5. Go back to where you were adding an SSH key in the Google cloud
console and paste your key (as copied in step 4).  Then click "Save".

<img src="img/17.png" width=600>

6. Make a note of the
username that appears to the left of the box --
you'll need it later.

<img src="img/30.png" width=700>
