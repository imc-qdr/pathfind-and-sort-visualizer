import tkinter as tk
from tkinter import ttk
from list_visualizer import *
from maze import *
import dbs


def v_sort():
    # according to the selected item in the listbox, speed, and size, it run the visualize function.
    if lst_sort.curselection()[0] == 0:
        data = visualize_sort(list_size.get(), v_bubble_sort, sort_delay.get())
    elif lst_sort.curselection()[0] == 1:
        data = visualize_sort(list_size.get(), v_insertion_sort, sort_delay.get())
    else:
        data = visualize_sort(list_size.get(), v_quick_sort, sort_delay.get())
    if data is not None:
        dbs.sort_entry(lst_sort.get(lst_sort.curselection()), list_size.get(), data[0], data[1])
        s_tree.insert('', 'end', values=(dbs.datetime.datetime.now(),
                                         lst_sort.get(lst_sort.curselection()),
                                         list_size.get(),
                                         data[0],
                                         data[1]))


def v_maze():
    # according to the selected item in the listbox, speed, and size, it run the visualize function.
    if path_find.curselection()[0] == 0:
        data = breadth_depth_first(generate_maze(matrix(maze_size.get())), maze_delay.get())
    elif path_find.curselection()[0] == 1:
        data = breadth_depth_first(generate_maze(matrix(maze_size.get())), maze_delay.get(), breadth=False)
    else:
        data = wall_follower(generate_maze(matrix(maze_size.get())), maze_delay.get())
    if data is not None:
        dbs.maze_entry(path_find.get(path_find.curselection()), maze_size.get(), data)
        m_tree.insert('', 'end', values=(dbs.datetime.datetime.now(),
                                         path_find.get(path_find.curselection()),
                                         maze_size.get(),
                                         data))


def clear_maze_table():
    # deletes all rows in the maze table. calls the function from dbs file
    dbs.clear_path()
    m_tree.delete(*m_tree.get_children())


def clear_sort_table():
    # deletes all the rows in the sorting table.
    dbs.clear_sort()
    s_tree.delete(*s_tree.get_children())


def filter_maze():
    if combobox_m.get() == 'All':
        result = dbs.get_path()
    else:
        result = dbs.filter_maze(combobox_m.get())
    m_tree.delete(*m_tree.get_children())
    for i in result:
        m_tree.insert('', 'end', values=tuple(i))


def filter_sort():
    if combobox_s.get() == 'All':
        result = dbs.get_sort()
    else:
        result = dbs.filter_sort(combobox_s.get())
    s_tree.delete(*s_tree.get_children())
    for i in result:
        s_tree.insert('', 'end', values=tuple(i))


def on_closing():
    dbs.connection.close()
    root.destroy()

# tkinter root window, title, and size.
root = tk.Tk()
root.title('algorithm visualizer')
root.geometry('700x500')
root.resizable(0, 0)
# closes the connection with the databases. the connection is made in the dbs file
root.protocol("WM_DELETE_WINDOW", on_closing)

# notebook holds different frames and displays them as tabs
tabs = ttk.Notebook(root)

# first tab for sort visualization
tab1 = ttk.Frame(tabs)
tab1.rowconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)

# second tab for the maze
tab2 = ttk.Frame(tabs)
tab2.rowconfigure(0, weight=1)
tab2.columnconfigure(1, weight=1)

# name the tabs and make them fill the notebook
tabs.add(tab1, text='sorting visualizer')
tabs.add(tab2, text='path finding visualizer')
tabs.pack(expand=1, fill='both')

# list box for the sorting algorithms options
sorting_alg = ('bubble sort', 'insertion sort', 'quick sort')
lst_sort = tk.Listbox(tab1, height=2)
lst_sort.grid(column=0, row=0, sticky='nws', padx=15, pady=15)
lst_sort.insert(tk.END, *sorting_alg)

# scale to choose the size with a label
list_size_l = tk.Label(tab1, text='size')
list_size_l.grid(column=0, row=2)
list_size = tk.Scale(tab1, from_=1, to=300, orient=tk.HORIZONTAL)
list_size.set(150)
list_size.grid(column=1, columnspan=3, row=2, sticky='ew', padx=10)

# scale to choose the speed of the visualization with a label
sort_delay_l = tk.Label(tab1, text='delay')
sort_delay_l.grid(column=0, row=3)
sort_delay = tk.Scale(tab1, from_=0, to=4, orient=tk.HORIZONTAL)
sort_delay.set(2)
sort_delay.grid(column=1, columnspan=3, row=3, sticky='sew', padx=10, pady=5)

# create a table with the widget treeview. the table displays the runs of sorting visualizations
s_tree_columns = ('Time', 'Algorithm', 'List size', 'Swaps', 'Comparisons')
s_tree = ttk.Treeview(tab1, columns=s_tree_columns, show='headings')
for i in s_tree_columns:
    s_tree.heading(i, text=i)
    s_tree.column(i, width=80)
s_tree.column('Time', width=110)
s_tree.grid(column=1, row=0, sticky='news', pady=15)
s_data = list(dbs.get_sort())
for i in s_data:
    s_tree.insert('', 'end', values=tuple(i))
s_tree_scroll = ttk.Scrollbar(tab1,
                              orient="vertical",
                              command=s_tree.yview)
s_tree_scroll.grid(column=2, row=0, sticky='ns', pady=15)
s_tree.configure(yscrollcommand=s_tree_scroll.set)

# 2 buttons to run the visualization and clear the table in the database
v_sort_button = tk.Button(tab1, text='Visualize', command=v_sort, width=20)
v_sort_button.grid(column=1, row=4, pady=10)
clear_sort_h = tk.Button(tab1, text='Clear history', command=clear_sort_table, width=20)
clear_sort_h.grid(column=0, row=4, pady=10, padx=15)

# listbox to choose the path finding algorithms options
maze_algs = ('breath first search', 'depth first search', 'wall follower')
path_find = tk.Listbox(tab2, height=1)
path_find.grid(column=0, row=0, sticky='nws', padx=15, pady=15)
path_find.insert(tk.END, *maze_algs)

# scale for the maze size
maze_size_l = tk.Label(tab2, text='size')
maze_size_l.grid(column=0, row=2)
maze_size = tk.Scale(tab2, from_=5, to=60, orient=tk.HORIZONTAL)
maze_size.set(20)
maze_size.grid(column=1, columnspan=3, row=2, sticky='ew', padx=10)

# scale for the speed of the visualization
maze_delay_l = tk.Label(tab2, text='delay')
maze_delay_l.grid(column=0, row=3)
maze_delay = tk.Scale(tab2, from_=0, to=4, orient=tk.HORIZONTAL)
maze_delay.set(2)
maze_delay.grid(column=1, columnspan=3, row=3, sticky='sew', padx=10, pady=5)

# table for the history of runs of the path finding algorithms
m_tree_columns = ('Time', 'Algorithm', 'maze size', 'cells scanned')
m_tree = ttk.Treeview(tab2, columns=m_tree_columns, show='headings')
for i in m_tree_columns:
    m_tree.heading(i, text=i)
    m_tree.column(i, width=80)
m_tree.column('Time', width=110)
m_tree.grid(column=1, row=0, sticky='news', pady=15)
m_data = list(dbs.get_path())
for i in m_data:
    m_tree.insert('', 'end', values=tuple(i))
m_tree_scroll = ttk.Scrollbar(tab2,
                              orient="vertical",
                              command=m_tree.yview)
m_tree_scroll.grid(column=2, row=0, sticky='ns', pady=15)
m_tree.configure(yscrollcommand=m_tree_scroll.set)

# 2 buttons to run the visualization and to clear the table in the database
v_maze_button = tk.Button(tab2, text='Visualize', command=v_maze, width=20)
v_maze_button.grid(column=1, row=4, pady=10)
clear_maze_h = tk.Button(tab2, text='Clear history', command=clear_maze_table, width=20)
clear_maze_h.grid(column=0, row=4, pady=10, padx=15)


combobox_m = ttk.Combobox(tab2, width=15, value=['All', *maze_algs])
combobox_m.grid(column=1, row=1, pady=20)
combobox_m.set('All')
combobox_m_button = tk.Button(tab2, text='Filter history', width=20, command=filter_maze)
combobox_m_button.grid(column=1, row=1, sticky='e')


combobox_s = ttk.Combobox(tab1, width=15, value=['All', *sorting_alg])
combobox_s.grid(column=1, row=1, pady=20)
combobox_s.set('All')
combobox_s_button = tk.Button(tab1, text='Filter history', width=20, command=filter_sort)
combobox_s_button.grid(column=1, row=1, sticky='e')


tk.mainloop()
