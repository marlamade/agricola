#####
## Drawing
####
resources = ['wood', 'clay', 'reed', 'stone', 'grain', 'veges', 'food']


def print_all(player, actions, width=7, height=3):
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
            if sq['type']=='field':
                draw_field(board, i, j, sq, width, height)

    for f in player['fences']:
        dir, row, col = f
        if dir in 'hH':
            i = row * (height+1) 
            jj = col * (width+1) + 2
            for j in range(jj, jj+width-2):
                board[i][j] = '#'
        else:# dir in 'vV':
            ii = row * (height+1) + 1  
            j = col * (width+1)
            for i in range(ii, ii+height):
                board[i][j] = '#'


    for i,ac in enumerate(actions):
        print i, ' '*(i<10),
        print ac['taken']*'@ ', (1-ac['taken'])*'  ',
        print ac['name'],
        if ac['amt'] > 0:
            print '('+str(ac['amt'])+')'
        else:
            print
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

        
def draw_field(board, row, col, sq, width=7, height=3):
    for i in range(row*(height+1)+1, (row+1)*(height+1)):
        for j in range(col*(width+1)+2, (col+1)*(width+1)-1):
            board[i][j]='.'
    if sq['amt']>0:
        if sq['resource']  in ['vege','veges']:
            r = 'V'
        else:
            r = 'G'
        i = int((row+.5)*(height+1))
        jj = int((col+.5)*(width+1)) - 1
        for j in range(jj, jj+sq['amt']):
            board[i][j]=r

def draw_pasture(board, row, col, sq, width, height):
    # draw animals
    # draw stables
    pass

            
def fill_square(board, row, col, ch, width=7, height=3):
    for i in range(row*(height+1)+1, (row+1)*(height+1)):
        for j in range(col*(width+1)+2, (col+1)*(width+1)-1):
            board[i][j]=ch
