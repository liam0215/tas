#!/usr/bin/gnuplot -persist
set terminal pdf
set output "plot.pdf"
set key autotitle columnhead
set key left top
set logscale x 2
              
set key top left
set xlabel "Message Size [Bytes]"
set ylabel "Goodput [Mbps]"
set yrange [0:]

plot "tp.dat" using 1:2:8 with yerrorlines title "virt-tas" linetype 1, \
     "tp.dat" using 1:3:9 with yerrorlines title "container-virtuoso" linetype 2, \
     "tp.dat" using 1:4:10 with yerrorlines title "ovs-tas" linetype 3, \
     "tp.dat" using 1:5:11 with yerrorlines title "container-tas" linetype 4, \
     "tp.dat" using 1:6:12 with yerrorlines title "ovs-linux" linetype 5, \
     "tp.dat" using 1:7:13 with yerrorlines title "container-ovsdpdk" linetype 6, \
     "tp.dat" using 1:8:14 with yerrorlines title "bare-tas" linetype 7