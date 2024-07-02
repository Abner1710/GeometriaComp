import point

def find_intersection(x1,y1,x2,y2,x3,y3,x4,y4):
  try:
      uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
      uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
  except:
      return None
  if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
      intersectionX = x1 + (uA * (x2-x1))
      intersectionY = y1 + (uA * (y2-y1))
      return point.Point(intersectionX, intersectionY)
  return None

def check_intersections(polygon):
    poly = polygon[:]
    poly.append(polygon[0])
    tmp = poly[:]
    intersections = []
    for l1, l2 in zip(poly, poly[1:]):
        tmp = tmp[1:]
        for n1,n2 in zip(tmp,tmp[1:]):
            ret = find_intersection(l1[0],l1[1],l2[0],l2[1],n1[0],n1[1],n2[0],n2[1])
            if ret and (ret != l2) and (ret != l1):
                intersections.append(ret)
    return intersections

def collinear(x1, y1, x2, y2, x3, y3): 
    a = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
    return (a==0)

def check_points_on_line(polygon):
    pts = []
    poly = polygon[:]
    poly.append(polygon[0])
    for p1, p2, p3 in zip(poly, poly[1:], poly[2:]):
        if(collinear(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1])):
            pts.append(p2)    
    out = []
    for p in polygon:
        if p not in pts:
            out.append(p)
            
    return out,pts

def rotate_list(l, shift):
    n = []
    for i in range(shift, len(l)):
        n.append(l[i])
    for i in range(0, shift):
        n.append(l[i])
    return n
