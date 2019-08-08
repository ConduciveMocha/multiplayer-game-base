



def _get_corner_points(x,y,width,height):
 
    return [(x, y), (x + width, y), (x, y + height), (x + width, y + height)]

def get_corner_points(*args):
    if len(args) == 1:
        rect = args[0]
        return _get_corner_points(rect.x,rect.y,rect.width,rect.height)
    elif len(args) == 4:
        return _get_corner_points(args[0],args[1],args[2],args[3])
    
    else:
        raise TypeError('get_corner_points takes 1 or 4 positional arguments')

def contains_point(rect, pt ):
    return (rect.x < pt.x < rect.x + rect.width) and (
        rect.y < pt.y < rect.y + rect.height + rect.y
    )

def rect_collides(rect1,rect2):
