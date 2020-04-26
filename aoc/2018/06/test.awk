function abs(a) {
  return a < 0 ? -a : a
}

function man_dist(x, y, x1, y1) {
  return abs(x - x1) + abs(y - y1)
}

BEGIN {
  FS= ", "
  pointsn=0
}
/[0-9]/{
  points[pointsn][0] = $1
  points[pointsn][1] = $2
  pointsn++
}
END {
  top_x=99999999
  top_y=99999999
  for (pt in points) {
    point_x = points[pt][0]
    point_y=points[pt][1]
    top_x = point_x < top_x ? point_x : top_x
    top_y = point_y < top_y ? point_y : top_y
    bottom_x = point_x > bottom_x ? point_x : bottom_x
    bottom_y = point_y > bottom_y ? point_y : bottom_y
  }
  for(y=top_y;y<=bottom_y;y++) {
    for(x=top_x;x<=bottom_x;x++) {
      tie=0
      min_dist=99999999999
      for (pt in points) {

        cur_dist = man_dist(x, y, points[pt][0], points[pt][1])
        if (cur_dist == min_dist) {
          tie=1
        }
        if (cur_dist < min_dist) {
          tie=0
          min_dist = cur_dist
          min_pt = pt
        }
      }
      if (!tie) {
        if (min_dist == 0) {
#           printf "!"
        } else {
#           printf min_pt
        }
        # filter infinite
        if (x == top_x || x == bottom_x || y == top_y || y == bottom_y || inf[min_pt]) {
          inf[min_pt] = 1
          continue
        }
        area[min_pt]++
      } else {
#         printf "."
      }
    }
#     print ""
  }

  for(pt in area) {
    if (area[pt] > max_area && !inf[pt]) {
      max_area = area[pt]
      max_pt = pt
    }
  }
  print max_pt
  print max_area
}
