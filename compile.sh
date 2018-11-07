#import py_compile

# explicitly compile this module
#py_compile.compile("main.py")

cython --embed ./main.py
gcc main.c $(pkg-config --cflags --libs python3) -o py