import csv
from reportlab.lib.colors import black
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont

c = canvas.Canvas("intervals.pdf")
gridwidth = 25  #resolution?
gridhor = [10]  #leftmost point of grid. List contains horizontal locations of vertical lines of grid
gridvert = [50]  #uppermost point of grid. List contains vert locations of horizontal lines of grid
num_days = [31,28,31,30,31,30,31,31,30,31,30,31]
legend_colours = [[106,190,69], [240,86,49], [114,206,227]]  #green, red, blue
stream_names = []  #contains names of streams for legend
streams = []  #contains the intervals of each stream, for drawing on grid
msperday = 86400000

def assemble_gridsize(num_months):
  for i in range (31):
    gridhor.append(gridhor[-1]+gridwidth)
  for i in range (num_months):
    gridvert.append(gridvert[-1]+gridwidth*len(stream_names))


def drawbackground(num_months):
  months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  c.setPageSize( (gridhor[-1]+100, gridvert[-1]+10) )

  #draw grid
  c.setStrokeColorRGB(220/255, 220/255, 220/255)
  c.grid(gridhor, gridvert)


  #draw month names
  c.setFont("Helvetica",17)
  for i in range (num_months):
    c.drawString(gridhor[-1]+10, gridvert[num_months-i]-30, months[i])


  #draw numbers of days
  c.setFont("Helvetica",13)
  for i in range (31):
    c.drawString(gridhor[i]+8, gridvert[0]-15, str(i+1))

  c.setFont("Helvetica",17)
  c.drawString(gridhor[7], gridvert[0]-40, "Day of Month")


def drawlegend(): 
  c.setFont("Helvetica",17)

  #draw coloured squares and stream names
  for i in range(len(stream_names)):
    c.setFillColor(black)
    c.drawString(gridhor[14+i*6]+22, gridvert[0]-40, stream_names[i])
    c.setFillColorRGB(legend_colours[i][0]/255, legend_colours[i][1]/255, legend_colours[i][2]/255) 
    c.rect(gridhor[14+i*6], gridvert[0]-40, 12, 12, stroke = 0, fill=1)


#store stream name in stream_names, store list of intervals in streams
def readfile(filename):
  intervals = []
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if line_count ==0:
        stream_names.append(row[0])
        line_count+=1
      else:
        row[0] = int(row[0])
        row[1] = int(row[1])
        if row[0]!=row[1]:
          intervals.append(row)
  streams.append(intervals)


def drawintervals(intervals, stream_num): #stream_num is for ordering in figure and colour
  #set the colour for each stream
  c.setFillColorRGB(legend_colours[stream_num][0]/255,legend_colours[stream_num][1]/255, legend_colours[stream_num][2]/255) 

  for i in intervals:
    starttime = i[0]
    endtime = i[1]

    startmonth = 0
    seccount = msperday*num_days[startmonth]
    while (starttime>seccount):
      startmonth+=1
      seccount +=msperday*num_days[startmonth]
    
    starttime -= seccount-msperday*num_days[startmonth]
    horizstart = gridhor[0]+starttime/msperday*gridwidth  #where in width of a month to start

    endmonth = 0
    seccount = msperday*num_days[endmonth]
    while (endtime>seccount):
      endmonth+=1
      seccount +=msperday*num_days[endmonth]

    endtime -= seccount-msperday*num_days[endmonth]
    horizend = gridhor[0]+endtime/msperday*gridwidth

    if endmonth == startmonth:  #interval doesn't cross to next month
      c.rect(horizstart, gridvert[len(gridvert)-1-startmonth]-22*(stream_num+1), horizend - horizstart, 20, stroke = 0, fill=1)

    else:  #interval crosses to next month
      width = gridhor[0] + num_days[startmonth]*gridwidth - horizstart
      c.rect(horizstart, gridvert[len(gridvert)-1-startmonth]-22*(stream_num+1), width, 20, stroke = 0, fill=1)  #fill in rest of month
      c.rect(gridhor[0], gridvert[len(gridvert)-1-endmonth]-22*(stream_num+1), horizend - gridhor[0], 20, stroke = 0, fill=1)


def countmonths(intervals):
  endts = intervals[-1][1]
  month = 0
  seccount = msperday*num_days[month]
  while (endts>seccount):
    month+=1
    seccount +=msperday*num_days[month]
  return month+1


if __name__ == "__main__":

  filenames = ["sample_input.csv", "sample_input.csv", "sample_input.csv"]
  for i in filenames:
    readfile(i)  #add stream names and intervals

  num_months = 0
  for i in streams:
    month_count = countmonths(i)
    if month_count>num_months:
      num_months = month_count  #find min number of months to include in figure
  
  assemble_gridsize(num_months)  #set grid size
  drawbackground(num_months)  #draw grid, month labels
  drawlegend()  #draw stream names and colours

  for i in range(len(streams)):
    drawintervals(streams[i], i)  #draw intervals on grid

  c.save()

