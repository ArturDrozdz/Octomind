import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.utils import timezone
from octo_site.models import Game, GameDetails, Room, Players, Teams

num_col = 28 #number of coloumns in the registration gsheet


room_dict = {
    'Debby\'s Doll': 1  
}
def sync():
    try:
        print("Authorizing credentials...")
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        print("Accessing worksheet...")
        sheets = client.open_by_key("1RRx2XM7fhFoYxeGlEeKog1xHeU06eAUXLm1zOXfO5nk").worksheet("MM Registration Form Responses")

        beg_col = 1
        beg_row = Game.objects.all().count()
        end_row = sheets.row_count
        end_col = sheets.col_count
        #end_col = num_col

        data = sheets.range(beg_row+2,beg_col,end_row,end_col)

        now_datetime = timezone.now() + timezone.timedelta(hours=8)
        curr_row = 0
        data_obj = {}
        player_cnt = 0
        for cell in data:
            if(cell.row != curr_row):

                if(data_obj != {}):
                    print(data_obj)
                    gamedets = GameDetails(teamname = data_obj['teamname'])
                    gamedets.save()
                    game = Game(room_id = data_obj['room_id'], game_details_id = gamedets.game_details_id, game_keeper_id = data_obj['game_keeper_id'])
                    game.save()
                    for i in data_obj['players']:
                        players = Players(firstname = i['firstname'], lastname = i['lastname'], contact = i['contact'], gender = i['gender'], email = i['email'], age = i['age'], loc_dictionary_id = i['loc'])
                        players.save()
                        teams = Teams(game_id = game.game_id, players_players_id = players.players_id)
                        teams.save()
                    print("Finish scanning data")
                curr_row = cell.row
                if(cell.value == ''):
                    break
                
                data_obj = {}
            else:
                if (cell.col == 2):
                    data_obj['game_keeper_id'] = 1
                elif (cell.col == 4):
                    data_obj['room_id'] =  Room.objects.get(room_name = cell.value).room_id
                elif (cell.col == 5):
                    player_cnt = (int)(cell.value)
                    data_obj['players'] = []
                    for i in range(0, player_cnt):
                        player_obj = {}
                        data_obj['players'].append(player_obj)
                elif (cell.col == 6):
                    data_obj['teamname'] = cell.value
                elif (cell.col > 8 and cell.value != ''):
                    p_col = cell.col - 9 #player coloumn, starts from 9 but normalize to 0 
                    cur_p = p_col//7 #each player has 7 cols so this is to check if its same player
                    cur_c = p_col%7 #this is get current coloumn with normalization
                    if(cur_c == 0):
                        data_obj['players'][cur_p]['firstname'] = cell.value
                    elif(cur_c == 1):
                        data_obj['players'][cur_p]['lastname'] = cell.value
                    elif(cur_c == 2):
                        data_obj['players'][cur_p]['email'] = cell.value
                    elif(cur_c == 3):
                        gender = 0
                        if(cell.value == 'Male'):
                            gender = 1
                        data_obj['players'][cur_p]['gender'] = gender
                    elif(cur_c == 4):
                        data_obj['players'][cur_p]['contact'] = cell.value
                    elif(cur_c == 5):
                        data_obj['players'][cur_p]['age'] = (int)(cell.value)
                    elif(cur_c == 6):
                        data_obj['players'][cur_p]['loc'] = (int)(cell.value)
                    pass
                pass
            '''
                do the updatng here from count to watever
                DB : {
                    Games,
                    GamesDetails,
                    Clues,
                    ClueDetails,
                    Players,
                    Teams
                },
                Excel: {
                    row1 : [ Games, GameDetails, Clues, ClueDetails, ...],
                    row2 : [ Games, GameDetails, Clues, ClueDetails, ...]
                }
                appened lng sa db
            '''
            pass
        
        # gamedets = GameDetails(timestart = now_datetime, teamname = "yes")
        # gamedets = GameDetails(teamname = data_obj['teamname'])
        # game = Game(room_id = data_obj['room_id'], game_details_id = gamedets.game_details_id)
        # for i in data_obj['players']:
        #     players = Players(firstname = i.firstname, lastname = i.lastname, contact = i.contact, gender = i.gender, email = i.email)
        #     teams = Teams(game_id = game.game_id, players_players_id = players.players_id)
        # yes.save()
        # print("Finish scanning data")



        return True
    except Exception as e:
        print("ERROR: " + str(e))
        print(">> Worksheet not found.")

        return False