import math, linecache

start_l = int(input("Start reading from line: "))
end_l = int(input("Stop reading from line: "))

d = input("Distance to shift (km): ") #distance in km
brng = math.radians(int(input("Bearing (Decimal Degrees): "))) #bearing, in decimal degrees

sct_path = "D:\Documents\GitHub\Hong-Kong-Sector-Package\Data\Sector\Hong-Kong-Sector-File.sct" #replace with the path to your.sct
ese_path = "D:\Documents\GitHub\Hong-Kong-Sector-Package\Data\Sector\Hong-Kong-Sector-File.ese" #replace with the path to your.ese
op_path = "D:\Downloads\VHHX_ese_v2.txt" #replace with where you want to store your output'

## formatting
def toDD(coord): ## converting d/m/s to decimal degrees
  coord = coord.strip("NESW")
  d, m, s = "", "",""
  for i, v in enumerate(coord):
    if v != "." and i in range(0, 3):
      d += v
    elif v != "." and i in range(4, 6):
      m += v
    elif i in range(7, 13):
      s += v
  return int(d) / 1 + int(m) / 60 + float(s) / 3600

def toDMS(coord): ## converting decimal degrees to d/m/s
  dec, deg = math.modf(coord)
  d = int(deg)
  m = int(dec * 60 // 1)
  s = "{:.3f}".format(((dec * 60) % 1) * 60)
  return(str(d).zfill(3) + "." + str(m).zfill(2) + "." + str(s.zfill(6)))

## calculating the new coords
def convert(lat1, long1):
  lat, long = math.radians(toDD(lat1)), math.radians(toDD(long1))
              
  a = math.sin(lat) * math.cos(d/6371) + math.cos(lat) * math.sin(d/6371) * math.cos(brng)
  newlat = math.asin(a)
  newlong = long + math.atan2((math.sin(brng) * math.sin(d/6371) * math.cos(lat)), (math.cos(d/6371) - math.sin(lat) * math.sin(newlat)))

  # i have very little idea of what it's doing, but it works
  # Haversine formula: https://www.movable-type.co.uk/scripts/latlong.html

  return(math.degrees(newlat), math.degrees(newlong)) 

## output
op_f = open(op_path, "a")

## writing output
def groundlayout(): #for GEO
  for l in range(start_l, end_l): #for VHHX, (16025, 16978)
    line = linecache.getline(sct_path, l)
    if "N022." in line:
      coord_i = str(line).find("N0")
      lat1, long1 = convert(line[coord_i:coord_i + 14], line[coord_i + 15:coord_i + 29])
      lat1_prefix, long1_prefix = "N" if lat1 > 0 else "S", "E" if long1 > 0 else "W"

      lat2, long2 = convert(line[coord_i + 30:coord_i + 44], line[coord_i + 45:coord_i + 69])
      lat2_prefix, long2_prefix = "N" if lat2 > 0 else "S", "E" if long2 > 0 else "W"

      try:
        if line[70].isalpha():
          colour = line[70:] 
      except:
        pass

      op_f.write(lat1_prefix + str(toDMS(lat1)) + " " + long1_prefix + str(toDMS(long1)) + " " + lat2_prefix + str(toDMS(lat2)) + " " + long2_prefix + str(toDMS(long2)) + " " + colour + "\n")

def smr(): #for Regions
  for l in range(start_l, end_l): #for VHHX, (72176, 73464)
    line = linecache.getline(sct_path, l)
    if "N022." in line:
      coord_i = str(line).find("N0")
      lat1, long1 = convert(line[coord_i:coord_i + 14], line[coord_i + 15:coord_i + 29])
      lat1_prefix, long1_prefix = "N" if lat1 > 0 else "S", "E" if long1 > 0 else "W"
      
      colour = ""

      if line[1].isalpha():
        colour = line.split(" ")[0] + "    "
      
      op_f.write(colour + lat1_prefix + str(toDMS(lat1)) + " " + long1_prefix + str(toDMS(long1)) + "\n")
    elif "REGIONNAME" in line: 
      op_f.write(line + "\n")

def ese(): #for Free text
  for l in range(start_l, end_l): #for VHHX, (4159, 4259)
    line = linecache.getline(ese_path, l)
    if "N022." in line:
      coord_i = str(line).find("N0")
      lat1, long1 = convert(line[coord_i:coord_i + 14], line[coord_i + 15:coord_i + 29])
      lat1_prefix, long1_prefix = "N" if lat1 > 0 else "S", "E" if long1 > 0 else "W"

      details = line[29:]

      op_f.write(lat1_prefix + str(toDMS(lat1)) + ":" + long1_prefix + str(toDMS(long1)) + details)
    elif line[0] == ";":
      op_f.write(line)

t = input("Please choose the type of file you are shifting \n 1 - GEO (.sct) \n 2 - Regions (.sct) \n 3 - Free text (.ese) \n")
if t == "1":
  groundlayout()
elif t == "2":
  smr()
elif t == "3":
  ese()
else:
  print("Invalid input")

op_f.close()
