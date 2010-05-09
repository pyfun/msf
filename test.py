a
# OUT: {'medians': [<matplotlib.lines.Line2D object at 0x2e2b850>, <matplotlib.lines.Line2D object at 0x2e312d0>], 'fliers': [<matplotlib.lines.Line2D object at 0x2e2bb90>, <matplotlib.lines.Line2D object at 0x2e2bed0>, <matplotlib.lines.Line2D object at 0x2e31610>, <matplotlib.lines.Line2D object at 0x2e31950>], 'whiskers': [<matplotlib.lines.Line2D object at 0x2e26850>, <matplotlib.lines.Line2D object at 0x2e26b10>, <matplotlib.lines.Line2D object at 0x2e2d250>, <matplotlib.lines.Line2D object at 0x2e2d590>], 'boxes': [<matplotlib.lines.Line2D object at 0x2e2b510>, <matplotlib.lines.Line2D object at 0x2e2df50>], 'caps': [<matplotlib.lines.Line2D object at 0x2e26e50>, <matplotlib.lines.Line2D object at 0x2e2b1d0>, <matplotlib.lines.Line2D object at 0x2e2d8d0>, <matplotlib.lines.Line2D object at 0x2e2dc10>]}
a['medians']
# OUT: [<matplotlib.lines.Line2D object at 0x2e2b850>, <matplotlib.lines.Line2D object at 0x2e312d0>]
a['medians'].value
lwater = watertown(np.where(watertown<=np.max(belmont)))
lwater = watertown[np.where(watertown<=np.max(belmont))]
lwater
# OUT: array([ 3324.,   304.,     0.,  5772.,  1888.,  5404.,  3912.,     0.,
# OUT:         2215.,  -184.,  6664.,  2933.,  3740.,  3882.,     0.,  4218.,
# OUT:         3609.,  5502.,     0.,     0.,  3332.,  1408.,  4030.,  6036.,
# OUT:         2580.,  3845.,     0.,  2703.,  3851.,  3292.,  1405.,  4009.,
# OUT:            0.,  2727.,  3888.,  3504.,  4923.,     0.,  2667.,  3774.,
# OUT:         3561.,  4502.,  -222.,  4402.,  3620.,  1989.,  5034.,  6609.,
# OUT:         3456.,  3801.,     0.,  1259.,  3307.,  4930.,  3403.,  5505.,
# OUT:            0.,  7000.,  3546.,  4888.,  6320.,  2828.,  3662.,     0.,
# OUT:         3827.,  6828.,  3882.,  2029.,  4455.,  3845.,   379.,  4403.,
# OUT:            0.,  3502.,     0.,  4421.,  3102.,   597.,  3680.,  3375.,
# OUT:            0.,  2359.,  3443.,  2347.,     0.,  4005.,  3709.,  2615.,
# OUT:            0.,  3455.,  2867.,  4501.])
len(lwater)
# OUT: 92
np.mean(lwater)+2*np.std(lwater)/np.sqrt(92.)
# OUT: 3362.708418187724
np.mean(lwater)-2*np.std(lwater)/np.sqrt(92.)
# OUT: 2554.313320942711
np.mean(belmont)-2*np.std(belmont)/np.sqrt(92.)
# OUT: 1460.5596994237794
np.mean(belmont)+2*np.std(belmont)/np.sqrt(92.)
# OUT: 2131.0403005762205
