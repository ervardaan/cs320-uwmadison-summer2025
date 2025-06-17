# Machine Project 8: Selling Laptops - Smart Marketing

## Overview

In this machine project, you are the owner of a retail website. You're planning on 
running a promotion on a laptop and you want to send emails out about
it. However, you only want to send it to people that may be interested
in it so as not to annoy people that aren't interested.  You're
looking to use your data about who clicked on similar emails in 2020
to help you predict which users may be interested in the promotion.

You should create your classifier in a `main.py` file, which will be
the only thing you'll submit.

You can collaborate with your team on the **entire** machine project (no
individual part!).  As usual, you cannot work with anybody outside of
your team and can only get help from 320 staff.

<hr/>

## Learning Objectives

During this machine project, students will:
- Extract, transform, and load data from multiple data sources into one DataFrame for training
machine learning models.
- Analyze machine learning model performance using several different metrics and factoring in feature
impact on the model score.

<hr/>

## Grading Guidelines

You can decide what features to consider and how to create your
classifier. Your grade will correspond to the accuracy of your
predictions. 50% accuracy and below will give a grade of 0%, whereas
accuracy of 75% and above will give a grade of 100%; any accuracy
between 50 and 75 will be rescaled to a 0-100% grade.  Some models can
get better than 90% accuracy, so we encourage you to keep improving
your model beyond what is necessary for full credit if you have time.

<hr/>

## Setup

Before you begin working on the project make sure you run the following commands from the `projects` directory:

```bash
cd mp8 # navigate to the project directory
git checkout main # switch to the main branch
git pull # pull remote changes to your local branch
git checkout MP8 # switch to MP8 branch
git merge main # merge changes from main to MP8
```

Once you run these commands, you should verify that you are on the `MP8` branch by running `git branch`, you should also be able to run `ls` to see that this machine project and all of its files are present. Additional instructions can be found in the [git-workflows](../../git-workflows/README.md/#starting-a-machine-project) document.

You are now ready to begin the machine project. Make sure that you add-commit-push your code as you go.

<hr/>

## Project Structure
This project consists of a **Group Part** worth 100%.

* **Group Part:**
    * `UserPredictor` class _(`main.py`)_
 
<hr/>

## Testing

Running `python3 tester.py` defaults to `python3 tester.py main test1`.  This will give you a general estimate of your final grade, but we'll run `python3 tester.py main test2` to actually compute that; you cannot run on test2, as we are not releasing `test2_users.csv`, etc. Based on noise, your grade may be better or worse for test1 vs. test2.  

Here are some tips to avoid surprises:

  * Don't read any CSVs directly in your `main.py`; just use the DataFrames passed to your methods to avoid inadvertently hardcoding paths

  * Accuracy of 75 corresponds to a grade of 100%.  We suggest you work to overshoot 75% by a bit in case you do slightly worse on test2 than test1

  * Some models are more vulnerable than others to noise in accuracy scores for different train/test datasets.  You may want to do cross validation in your `fit` method and prints some stats.  How will depend on other design choices you make, but you could, for example, have a debug print -- something like the following in `fit` (a high standard deviation would indicate I'm more likely to be unlucky with getting a very different score on test2 than test1):

```python
scores = cross_val_score(model, train_users[self.xcols], train_y["y"])
print(f"AVG: {scores.mean()}, STD: {scores.std()}\n")
```

<hr/>

## Submission

**Required Files**
* `main.py`: A Python module which has the `UserPredictor` class in it.

To submit the machine project, make sure that you have followed the instructions for "submitting a machine project"
in the [git-workflows](../../git-workflows/README.md/#submitting-a-machine-project) document for the required file(s) above.

When following the submission instructions from above, the final output should look similar to this in GitLab:

<img src="img/successful-submission.PNG">

If you do not know how to get to this screen, review the link above. If you are having issues, please come to office hours.

<hr/>

## Important Notes:
1. Hardcoding of any kind or trying to "cheat" the autograder **will be penalized heavily and can also result in 0 marks for all the projects**. If you are confused about your code, please reach out to the teaching staff before submission.

<hr/>

## **Follow these instructions to complete MP8**

<hr/>

## Dataset

We have generated 3 datasets:

1. train
2. test1
3. test2 (secret)

You'll fit your classifier to the training data, then estimate your
accuracy using the test1 data.  We'll compute your final grade based
on test2 data, which is similar but not identical to test1 data.

Each of the 3 datasets consist of 3 files (so there are 9 files total, of which we give you 6):

1. `???_users.csv`: information about each user
2. `???_logs.csv`: details about webpages visited by each user
3. `???_y.csv`: y=1 means they clicked the email; y=0 means they did not

Here is some data in `train_users.csv`, which represents user accounts on our website:

<img width=400 src="img/users.png">

Here is the corresponding data from `train_y.csv`, which shows us which users
ended up clicking on the promotional email:

<img width=200 src="img/y.png">

After matching the IDs and considering the `y` column, we can see
Adriana (user_id 0) did not click the ad (y=False).

Here is some data in `train_logs.csv`:

<img width=400 src="img/logs.png">

Each row represents a visit to a webpage on the site.  Each row
contains the date, the id of the user who visited the page, the url
that they visited, and the number of minutes spent on the page.  We
see Adriana visited 4 pages on the website for varying amounts of time
(including one for laptop.html).

User browsing history has the potential to be a good indicator for
user clicks, but to make use of it with a machine learning model,
you'll need to find ways to compute summary stats per user based on
multiple page visits (or sometimes no page visits).

## Requirement: `UserPredictor` class
> 📄 **Work in:** [`main.py`](main.py)

The goal of this machine project is to build a classifier that, given user and
log data, can predict whether those users will be interested in our
product.  There are a number of ways that you can go about this and a
number of ways that you can use the data (or not use portions of the
data); the freedom is yours.

You'll write your classifier as a class called `UserPredictor` in your
`main.py` file.  We require two methods (feel free to add more as
useful): `fit` and `predict`.

**We recommend reading `tester.py` to understand how we expect your
class to work.  We intentionally made tester.py very simple this time
-- only 80 lines of code!**

### Method 1: `fit`

Somebody using your class (and the tester) will call `fit` something
like this:

```python
from main import UserPredictor
model = UserPredictor()
train_users = pd.read_csv("data/train_users.csv")
train_logs = pd.read_csv("data/train_logs.csv")
train_y = pd.read_csv("data/train_y.csv")
model.fit(train_users, train_logs, train_y)
```

We don't have any requirements on what `fit` does (no need to output
or return anything), but you'll **probably** want to fit an underlying
`sklearn` model to the data (for example, a `LogisticRegression`) which can be used to make predictions later, outside of the `fit` method.

### Method 2: `predict`

Somebody using your class (and the tester) will call `predict` something
like this:

```python
test_users = pd.read_csv("data/test1_users.csv")
test_logs = pd.read_csv("data/test1_logs.csv")
y_pred = model.predict(test_users, test_logs)
```

`predict` should return a numpy array.  If `y_pred[n]` is True, that
means you predict the user at index `n` will click the email;
otherwise, you're predicting they will not.

<hr/>

## Hints and Suggestions

* You can implement a custom classifier from scratch if you like, but we imagine most of you will have an sklearn pipeline as an attribute in your class, with your `fit` method fitting the pipeline and your `predict` method using the pipeline for predictions

* Start simple, then add complexity.  For example, you only need to get >50% accuracy to get some points, and a simple `LogisticRegression` based only on `past_purchase_amt` should have an accuracy score around 60%.

* As you consider features for your model, it's easier to start with just the `???_users.csv` file (ignoring the logs data), as each user row corresponds to exactly one outcome/prediction.  We were able to train a simple model just based on the user data that achieved an accuracy of 72%, completely ignoring the log data.

* To reach a grade of 100%, you'll probably need to use the logs data that describes how long each user spent on various pages.  You can decide how to use the logs data, but the simplest way might be to write a method that adds feature columns to the user DataFrame, based on per-user stats of your choosing calculated from the logs data.  For example, you could add a column describing how many total minutes each user spent on the site.  Using a separate method to add such information can help you avoid repeat work between your `fit` and `predict` methods (you'll presumably need the same additional columns for both training and predicting). For example, we have a
`UserPredictor.add_logs_as_features(...)` method that does this for us.

* Some users may not have any rows in logs if they didn't visit the website at all.  Consider how you'll deal with this.

* You're welcome to learn new classification models in sklearn and use them for this machine project, but we imagine most of you will build pipelines based on LogisticRegression, the classifier we learned in class.  Remember that in many scenarios LogisticRegression does best in a pipeline where there is a preceding StandardScaler.  LogisticRegression doesn't like large/small numbers or non-centered data, so StandardScaler transforms the data to work better with LogisticRegression.


* If you plan to work with your team members (not required, as usual), consider how you may want to divide the work.  One possibility: each team member could try a different model; after comparing them, all team members could submit the one model that scores best.  Alternatively, each team member could be responsible for computing different per-user stats to use as features for training/predicting.  Of course, avoid getting in a situation where you are dependent on any one person to complete the machine project; this machine project should be a reasonable amount of work, even for somebody working individually.
