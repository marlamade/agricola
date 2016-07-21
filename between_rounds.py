from random import randint
def new_round(player, actions, action_cards):
    if action_cards == []:
        print "Game Over"
        return False
    if action_cards[0] == []:
        print "Harvest First"
        return False
    x = randint(0,len(action_cards[0])-1)
    actions.append(action_cards[0][x])
    del action_cards[0][x]

    people = 0
    for ac in actions:
        if ac['name'] == 'Wood':
            ac['amt'] += 2
        if ac['name'] in ['Reed','Clay', 'Stone', 'Fishing', 'Sheep','Cattle','Boars']:
            ac['amt'] += 1

        #pick up the players
        people += ac['taken']
        ac['taken']=0

    #put them back
    num_rooms = 0
    for i in range(3):
        for j in range(5):
            if player['board'][i][j]['type'] == 'room':
                num_rooms += 1
                people += player['board'][i][j]['people']
                player['board'][i][j]['people'] = 0
    for i in range(3):
        for j in range(5):
            if player['board'][i][j]['type'] == 'room':
                x = (people-1)/num_rooms + 1
                player['board'][i][j]['people'] = x
                people -= x
                num_rooms -= 1
                    
        
def harvest(player, action, action_cards):
    if action_cards == []:
        print "Game Over"
        return False
    if action_cards[0] != []:
        print "Not Harvest Time"
        return False
    del action_cards[0]
    
