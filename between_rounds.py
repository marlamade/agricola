def new_round(player, actions):
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
                    
        

    
