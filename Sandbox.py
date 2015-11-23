__author__ = 'Jonathan Spitz'

from matplotlib.pyplot import plot, draw, show

def make_plot():
    plot([1,2,3])
    show(block=False)
    print 'continue computation'

print('Do something before plotting.')
# Now display plot in a window
make_plot()

answer = raw_input('Back to main and window visible? ')
if answer == 'y':
    print('Excellent')
else:
    print('Nope')
