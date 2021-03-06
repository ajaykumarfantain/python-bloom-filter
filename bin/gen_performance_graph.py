#!/usr/bin/python

import sys
import anydbm
from pychart import *

def get_timing(kind):
    database = anydbm.open('performance-numbers', 'r')
    list_ = []
    for key in database.keys():
        fields = key.split()
        #print fields[0], kind
        if fields[0] == kind:
            set_size = float(fields[1])
            duration = float(database[key])
            list_.append( ( set_size, duration ) )
    database.close()
    list_.sort()
    return list_

#def get_timing(filename):
#    file_ = open(filename, 'r')
#    list_ = []
#    for line in file_:
#        fields = line.split()
#        set_size = float(fields[0])
#        duration = float(fields[1])
#        list_.append( ( set_size, duration ) )
#    file_.close()
#    return list_

def get_hybrid_timing():
    return get_timing('hybrid')

def get_array_timing():
    return get_timing('array')

def get_seek_timing():
    return get_timing('seek')

def get_mmap_timing():
    return get_timing('mmap')

def desired_y_max(*list_):
    maximum = 0.0
    for element in list_:
        for set_size, duration in element:
            maximum = max(duration, maximum)
    return maximum

def main():
    theme.get_options()
    theme.output_format = 'pdf'
    theme.use_color = 1
    theme.output_file = 'performance-graph.pdf'
    theme.default_font_size = 15
    theme.reinitialize()

    width = 800
    height = width * 4 // 5
    size = (width, height)

    hybrid_timing_data = get_hybrid_timing()
    print 'hybrid', hybrid_timing_data
    array_timing_data = get_array_timing()
    print 'array', array_timing_data
    seek_timing_data = get_seek_timing()
    print 'seek', seek_timing_data
    mmap_timing_data = get_mmap_timing()
    print 'mmap', mmap_timing_data

    y_max = desired_y_max(array_timing_data, seek_timing_data, hybrid_timing_data, mmap_timing_data)

    can = canvas.default_canvas()

    ar = area.T(
        size = size,
        legend=legend.T(),
        x_range = (1, None),
        y_range = (0.0001, y_max + 100),
        #x_coord = log_coord.T(),
        #y_coord = log_coord.T(),
        x_coord = linear_coord.T(),
        y_coord = linear_coord.T(),
        x_axis = axis.X(format="%g", label="Number of elements in set"),
        y_axis = axis.Y(format="%g", label="Seconds"),
        )

    lp = line_plot.T(data=array_timing_data, label="Array")
    ar.add_plot(lp)
                    
    lp = line_plot.T(data=seek_timing_data, label="Seek")
    ar.add_plot(lp)
                    
    lp = line_plot.T(data=hybrid_timing_data, label="Hybrid")
    ar.add_plot(lp)
                    
    lp = line_plot.T(data=mmap_timing_data, label="mmap")
    ar.add_plot(lp)
                    
    ar.draw()

    #can.show(ar.x_pos(4), ar.y_pos(970), "/a50{}seek")

main()


