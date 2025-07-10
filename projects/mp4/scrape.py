'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 4 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP4
Student 1: vardaan kapoor, vkapoor5
'''
from collections import deque
import pandas as pd
import os
from selenium.webdriver.common.by import By

class GraphSearcher:
    def __init__(self):
        # tracks which nodes have been visited
        self.visited = set()
        # records the order in which nodes are first seen
        self.order = []

    def visit_and_get_children(self, node):
        """
        MUST be overridden in subclasses.
        Should append `node` to self.order and return an iterable
        of its children.
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, start_node):
        """
        Public entry point: clears state, kicks off the recursion,
        and returns the final visitation order.
        """
        # reset visited & order
        self.visited.clear()
        self.order.clear()

        # start the recursive DFS
        self.dfs_visit(start_node)

        # return the recorded order
        return self.order

    def dfs_visit(self, node):
        """
        Recursive DFS:
          1. If already seen, return immediately.
          2. Mark as seen.
          3. Ask subclass for children (and record node in order).
          4. Recurse on each child.
        """

        # 1) base case
        if node in self.visited:
            return

        # 2) mark visited
        self.visited.add(node)

        # 3) get children (subclass must record node in self.order here)
        children = self.visit_and_get_children(node)

        # 4) recurse
        for child in children:
            self.dfs_visit(child)
    
    def bfs_search(self,node):
        self.visited.clear()
        self.order.clear()
        queue=deque()
        queue.append(node)
        self.bfs_visit(queue)
        return self.order
    
    def bfs_visit(self,queue):
        size=len(queue)
        if size==0:
            return
        for i in range(size):
            node=queue.popleft()
            if node in self.visited:
                continue
            self.visited.add(node)
            children=self.visit_and_get_children(node)
            for child in children:
                queue.append(child)
        self.bfs_visit(queue)

class MatrixSearcher(GraphSearcher):
    def __init__(self, df: pd.DataFrame):
        """
        df should be a square DataFrame whose index and columns
        are the same set of node labels, and entries are 0/1.
        """
        super().__init__()
        self.df = df

    def visit_and_get_children(self, node):
        """
        1) append the node to the visitation order
        2) look across df.loc[node] for entries == 1
           and return those column‐labels as children
        """
        # record the visitation
        self.order.append(node)

        # df.loc[node] is a Series of 0/1; .items() yields (col_label, value)
        children = [
            col
            for col, val in self.df.loc[node].items()
            if val == 1
        ]
        return children
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
    
    def visit_and_get_children(self,file):
        path = os.path.join("file_nodes", file)
        with open(path, "r") as f:
            lines=[]
            for line in f.readlines():
                lines.append(line.strip())
        node_value=lines[0]
        self.order.append(node_value)
        children=[]
        for child in lines[1].split(","):
            if child.strip():
                children.append(child.strip())
        return children
                
    
    def concat_order(self):
        s=""
        for node in self.order:
            s+=node
        return s
    
class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        """
        driver: a Selenium WebDriver instance (e.g., headless Chrome).
        """
        super().__init__()
        self.driver    = driver
        self.fragments = []   # will hold only the “clue” tables in visit order

    def visit_and_get_children(self, url: str):
        """
        1) Navigate the driver to `url`.
        2) Append `url` to self.order.
        3) Scrape only the first <table> (the clue table) and append it to self.fragments.
        4) Return every href found in <a> tags on the page as children.
        """
        # 1) Visit page
        self.driver.get(url)

        # 2) Record visitation
        self.order.append(url)

        # 3) Read all tables but only keep the first one
        tables = pd.read_html(self.driver.page_source)
        if tables:
            self.fragments.append(tables[0])

        # 4) Find all hyperlinks
        anchors = self.driver.find_elements(By.TAG_NAME, "a")
        children = []
        for a in anchors:
            href = a.get_attribute("href")
            if href:
                children.append(href)
        return children

    def table(self) -> pd.DataFrame:
        """
        Concatenate all collected clue tables (in visitation order)
        into one DataFrame with a fresh integer index.
        """
        if not self.fragments:
            return pd.DataFrame()
        return pd.concat(self.fragments, ignore_index=True)

import time
import requests
from selenium.webdriver.common.by import By
import pandas as pd

def reveal_secrets(driver, url, travellog):
    
    password = "".join(travellog["clue"].astype(str))
    
    driver.get(url)
    #firs button to click->the GO BUTTON
    password_input = driver.find_element(By.ID, "password-textbox")
    password_input.send_keys(password)
    
    submit_button = driver.find_element(By.ID, "submit-button")
    submit_button.click()
    #give some time break so that the password can be validated and the next page can be opened which gives us another button to get the actual secret string
    time.sleep(1)
    #second button to click->the find secret button on the next webpage which opens up when we click the GO BUTTON
    view_location_button = driver.find_element(By.ID, "location-button")
    view_location_button.click()
    # now we again wait for the final next webpage to open after we click this second button->this webpage gives us an image and secret message
    time.sleep(1)
    
    image = driver.find_element(By.TAG_NAME, "img")
    image_link = image.get_attribute("src")
    
    response = requests.get(image_link)
    
    if response.status_code == 200:
        with open("Current_Location.jpg", "wb") as f:
            f.write(response.content)
    # the location text is the text which has id of "location" so we get that text and return this secret string(the text we get using find_element method)        
    location_element = driver.find_element(By.ID, "location")
    current_location = location_element.text
    
    return current_location

        