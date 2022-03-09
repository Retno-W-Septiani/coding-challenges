import os
import shutil

# # # creating root directory
os.mkdir('C:/CC3')
root_directory = 'C:/CC3'
folder = ['draft_code', 'includes', 'layouts', 'site']
for i in folder:
    os.mkdir(os.path.join(root_directory, i))

# # creating branch1 directory
branch1 = 'C:/CC3/draft_code'
draft_code = ['pending', 'complete']
for b in draft_code:
    os.mkdir(os.path.join(branch1, b))

# # creating branch1 directory
branch2 = 'C:/CC3/layouts'
layouts = ['default', 'post']
for c in layouts:
    os.mkdir(os.path.join(branch2, c))

# # creating leave directory under branch 2
leave = 'C:/CC3/layouts/post'
post = ['posted']
for d in post:
    os.mkdir(os.path.join(leave, d))

# # # deleting all created directory
shutil.rmtree(root_directory)
