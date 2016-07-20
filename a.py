
resources = ['wood', 'clay', 'reed', 'stone', 'grain', 'veges', 'food']

def new_player():
    p =  {'board': \
                [ [{'type':'empty'} for i in range(5)] for j in range(3)], \
            'resources': \
                {r:0 for r in resources}, \
            'people':2,
            'occupations':['occ1', 'occ2'],
            'improvements':['imp1', 'imp2', 'imp3'],
            'fences':[]
            }

    p['board'][1][0] = {'type':'room', 'people':1}
    p['board'][2][0] = {'type':'room', 'people':1}
    return p

    

def print_player(player, width=7, height=3):
    divider_row = list(('+'+'-'*width)*5+'+')
    plain_row = list(('|'+' '*width)*5+'|')
    board = [ divider_row + []]
    for i in range(3):
        for j in range(height):
            board.append(plain_row+[])
        board.append(divider_row+[])

    for i,row in enumerate(board):
        row.append('\t')
        if i < len(resources):
            rsrc = resources[i]
            amt = player['resources'][rsrc]
            row.append(rsrc + ": ")
            if len(rsrc)==4:
                row.append(' ')
            row.append(str(amt))
                
    for i in range(3):
        for j in range(5):
            sq = player['board'][i][j]
            if sq['type']=='room':
                draw_room(board, i,j , sq['people'],width, height)

    
    for row in board:
        print ''.join(row)
        

def draw_room(board, row, col, people, width, height):
    top = row*(height+1) + 1
    bot = (row+1)*(height+1)-1     
    left=col*(width+1)+2
    right=(col+1)*(width+1)-2    
    for j in range(left+1, right):
        board[top][j]="'"
        board[bot][j]=","
    for i in range(top, bot+1):
        board[i][left]="("
        board[i][right]=")"

    if people >= 1:
        board[(top+bot)/2][(left+right)/2] = '@'
    if people >= 2:
        board[(top+bot)/2][(left+right)/2+1] = '@'
    if people >= 3:
        board[(top+bot)/2][(left+right)/2-1] = '@'

        
def fill_square(board, row, col, ch, width=7, height=3):
    for i in range(row*(height+1)+1, (row+1)*(height+1)):
        for j in range(col*(width+1)+2, (col+1)*(width+1)-1):
            board[i][j]=ch
    
        
