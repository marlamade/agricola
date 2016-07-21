

import drawing
reload(drawing)
import between_rounds
reload(between_rounds)

resources = ['wood', 'clay', 'reed', 'stone', 'grain', 'veges', 'food']
print_all = drawing.print_all
new_round = between_rounds.new_round


def new_player():
    p =  {'board': \
                [ [{'type':'empty'} for i in range(5)] for j in range(3)], \
            'resources': \
                {r:500 for r in resources}, \
            'people':2,
            'occupations':['occ1', 'occ2'],
            'improvements':['imp1', 'imp2', 'imp3'],
            'fences':[],
            'house':'wood'
          
            }

    p['board'][1][0] = {'type':'room', 'people':1}
    p['board'][2][0] = {'type':'room', 'people':1}

    #p['board'][1][4] = {'type':'field', 'resource':'grain', 'amt':3}
    #p['board'][0][2] = {'type':'field', 'resource':'vege', 'amt':2}
    #p['board'][2][4] = {'type':'field', 'resource':'vege', 'amt':0}
    #p['board'][2][1] = {'type':'field', 'amt':0}
    
    #p['fences'] = [['h',0,0], ['h', 1,2], ['v',1,3]]
    return p




    
#####
## Add functions
#####

def add_room(player, row, col):
    player['board'][row][col]={'type':'room', 'people':0}

def add_field(player, row, col):
    player['board'][row][col]={'type':'field', 'amt':0}

def add_stable(player, row, col):
    if player['board'][row][col]['type'] != 'pasture':
        print 'error' #FIXME
    else:
        player['board'][row][col]['stables'] = 1
            
##############################
## Actions
###################


def action_rooms(player, kwargs):
    if 'rooms' in kwargs:
        rooms = kwargs['rooms']
    else:
        rooms = []
    if 'stables' in kwargs:
        stables = kwargs['stables']
    else:
        stables = []

    # Actually specifying something to build
    if rooms==[] and stables==[]:
        print "rooms=[[row, col], [row,col]], stables=[[row,col],[row,col]]"
        return False
    
    #Have the resources
    wood_needed = 2 * len(stables)
    reed_needed = 2 * len(rooms)
    clay_needed = 0
    stone_needed = 0
    if player['house']=='wood':
        wood_needed += 5 * len(rooms)
    if player['house']=='clay':
        clay_needed += 5 * len(rooms)
    if player['house']=='stone':
        stone_needed += 5 * len(rooms)
    
    if player['resources']['wood'] < wood_needed or \
       player['resources']['clay'] < clay_needed or \
       player['resources']['reed'] < reed_needed or \
       player['resources']['stone'] < stone_needed:
            print "Not enough resources"
            return False

    #Space is availible FIXME: for stables, pasture is also ok
    for i,j in rooms + stables:
        if player['board'][i][j]['type'] != 'empty':
            print 'Space',i,j,'Not availible'
            return False
        
    for room in rooms:
        add_room(player, room[0], room[1])
        
    for stable in stables:
        add_stable(player, stable[0], stable[1])


    player['resources']['wood'] -= wood_needed
    player['resources']['clay'] -= clay_needed
    player['resources']['reed'] -= reed_needed
    player['resources']['stone'] -= stone_needed

    #print game_log
    #game_log += [['rooms', rooms, 'stables', stables,
    #              'wood', wood_needed, 'clay', clay_needed,
    #              'stone', stone_needed, 'reed', reed_needed  ]]
    
    return True

def action_grain(player, kwargs):
    player['resources']['grain'] += 1
    return True
def action_wood(player, kwargs):
    player['resources']['wood'] += kwargs['amt']
    return True
def action_reed(player, kwargs):
    player['resources']['reed'] += kwargs['amt']
    return True
def action_clay(player, kwargs):
    player['resources']['clay'] += kwargs['amt']
    return True
def action_stone(player, kwargs):
    player['resources']['stone'] += kwargs['amt']
    return True
def action_fishing(player, kwargs):
    player['resources']['food'] += kwargs['amt']
    return True
def action_daylaborer(player, kwargs):
    player['resources']['food'] += 2
    return True

def action_plow(player, kwargs):
    if 'field' not in kwargs:
        print "field=[row,col]"
        return False
    
    i,j = kwargs['field']
    #Space is availible
    if player['board'][i][j]['type'] != 'empty':
        print 'Space',i,j,'Not availible'
        return False
        
    add_field(player, i,j)
    return True

def action_pass(player, kwargs):
    pass

######
## Action handler
####
actions = [{'name':'', 'fxn':False, 'taken':0, 'amt':0} for i in range(10)]

def action(player, action_id, **kwargs):
    #find a person
    sq = False
    for i in range(3):
        for j in range(5):
            sq_ = player['board'][i][j]
            if sq_['type'] == 'room' and sq_['people'] >= 1:
                sq = sq_
    if not sq:
        print "No people left"
        return False

    if actions[action_id]['taken']:
        print "Action already taken this round"
        return False

    kwargs['amt'] = actions[action_id]['amt']
    
    if actions[action_id]['fxn'](player, kwargs):
        actions[action_id]['taken'] = 1
        actions[action_id]['amt'] = 0
        sq['people'] -= 1
        return True

actions[0]['name'] = 'Rooms + Stables -'
actions[0]['fxn'] = action_rooms
actions[1]['name'] = 'Minor Improvement --'
actions[1]['fxn'] = action_pass
actions[2]['name'] = 'Grain'
actions[2]['fxn'] = action_grain
actions[3]['name'] = 'Plow'
actions[3]['fxn'] = action_plow
actions[4]['name'] = 'Occupation --'
actions[4]['fxn'] = action_pass
actions[5]['name'] = 'Day Laborer'
actions[5]['fxn'] = action_daylaborer
actions[6]['name'] = 'Wood'
actions[6]['fxn'] = action_wood
actions[7]['name'] = 'Clay'
actions[7]['fxn'] = action_clay
actions[8]['name'] = 'Reed'
actions[8]['fxn'] = action_reed
actions[9]['name'] = 'Fishing'
actions[9]['fxn'] = action_fishing

#actions.append({'name':'Stone', 'fxn':action_stone, 'amt':0, 'taken':0})

action_cards = [
    [
        {'name':'Sheep', 'fxn':action_pass, 'amt':0, 'taken':0},
        {'name':'Fences --','fxn':action_pass, 'amt':0, 'taken':0},
        {'name':'M/m Improvement --','fxn':action_pass, 'amt':0, 'taken':0},
        {'name':'Sow & Bake --','fxn':action_pass, 'amt':0, 'taken':0}
    ],
    [
        {'name':'Family Growth -> m', 'fxn':action_pass, 'amt':0, 'taken':0},
        {'name':'Rennovation -> M/m', 'fxn':action_pass, 'amt':0, 'taken':0},
        {'name':'Stone', 'fxn':action_stone, 'amt':0, 'taken':0},
    ],
    [
        {'name':'Veges', 'fxn':action_pass, 'amt':0, 'taken':0},
        {'name':'Boars', 'fxn':action_pass, 'amt':0, 'taken':0},
    ],
    [
        {'name':'Stone', 'fxn':action_stone, 'amt':0, 'taken':0},
        {'name':'Cattle', 'fxn':action_pass, 'amt':0, 'taken':0},
    ],
    [
        {'name':'Family w/o Space', 'fxn':action_pass, 'amt':0, 'taken':0},
        {'name':'Plow & Sow', 'fxn':action_pass, 'amt':0, 'taken':0},
    ],
    [
        {'name':'Rennovate & Fences', 'fxn':action_pass, 'amt':0, 'taken':0},
    ]

]

####
## Rounds
###
