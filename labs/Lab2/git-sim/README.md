# Git Simulator

Let's start by practicing in the Git simulator <a
href="https://tyler.caraza-harter.com/cs320/learnGitBranching/index.html"
target="_blank">here</a>.  

Useful commands for the above problem:
* `git commit`: make a new commit
* `git branch bname`: create a branch named `bname`
* `git checkout bname`: move `HEAD` to the commit referenced by the `bname`
* `git checkout c1`: move `HEAD` to the `c1` commit
* `git merge bname`: merge changes on the `bname` branch into the current branch
* `git branch -D bname`: delete the branch named `bname`

These are just for git simulator and will **not** work when actually using Git
* `undo`: undo the most recent command
* `reset`: brings you back to just having C0

Try to run commands to get to the following state (if you get stuck, check the [solution here](solution.md)):

<img src="1.png" width=500>

### When submitting projects this semester, we will be using a Git workflow. The suggested general order that we will do this is as follows:
- Pull all files needed for the different projects while on the main branch. 
- Work through the projects while on this main branch and pull any updates to files that there may be.
- Once ready to submit, *git checkout* to the respective project branch (ex. MP1).
- *git merge main* while on the project branch to get all of your work to the project branch.
- *git push* all of your work to the remote branch for the respective project.
- *git checkout main* to be ready to start with your next project.

Here is an example of what that might *look* like:

<img src="3.png" width=800>

If you have some free time at the end of the lab, you can try out the following challenge. 

Try to get to this state (no answer to check for this one, so you'll need to work for it!): 

<img src="2.png" width=500>

**Hint:** Start by creating commits on four branches, b1, b2, b3, and b4.
Merge b2 into b1 and b4 into b3.  Then merge the two merge commits
with a third merge commit.
