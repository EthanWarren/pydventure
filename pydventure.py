import cmd
class Game() :
    def __init__(self,name) :
        self.name=name
        self.world={}
        self.player=None
    def set_player(self,player) :
        self.player=player
    def new_room(self,room) :
        self.world[room.name]=room
class Player() :
    def __init__(self,startroom) :
        self.flags={}
        self.inventory=[]
        self.currentroom=startroom
    def set_location(self,location) :
        self.currentroom=location
    def set_flag(self,flag) :
        self.flags[flag]=True
    def get_flag(self,flag) :
        return self.flags[flag]
    def unset_flag(self,flag) :
        self.flags[flag]=False
class Item() :
    def __init__(self,grounddesc,shortdesc,longdesc,descwords,edible=False,drinkible=False,openable=False,open=False) :
        self.grounddesc=grounddesc
        self.contents=[]
        self.openable=openable
        self.open=open
        self.shortdesc=shortdesc
        self.longdesc=longdesc
        self.descwords=descwords
        self.edible=edible
        self.drinkible=drinkible
        self.flags={}
    def new_item(self,item) :
        self.contents.append(item)
    def set_flag(self,flag) :
        self.flags[flag]=True
    def unset_flag(self,flag) :
        self.flags[flag]=False
    def get_flag(self,flag) :
        return self.flags[flag]
    def remove_item(self,item) :
        self.contents.remove(item)
class Npc() :
    def __init__(self,name,description,descwords,askstrings={}) :
        self.name=name
        self.description=description
        self.descwords=descwords
        self.askstrings=askstrings
        self.flags={}
    def say(self,message) :
        print "{} says \"{}\"".format(self.name,message)
    def set_flag(self,flag) :
        self.flags[flag]=True
    def unset_flag(self,flag) :
        self.flags[flag]=False
    def get_flag(self,flag) :
        return self.flags[flag]
class Room() :
    def __init__(self,name,description,north=None,south=None,east=None,west=None,northwest=None,northeast=None,southwest=None,southeast=None,up=None,down=None) :
        self.exits={"north":north,"south":south,"east":east,"west":west,"northeast":northeast,"northwest":northwest,"southeast":southeast,"southwest":southwest,"up":up,"down":down}
        self.name=name
        self.description=description
        self.items=[]
        self.npcs=[]
        self.flags={}
    def set_flag(self,flag) :
        self.flags[flag]=True
    def unset_flag(self,flag) :
        self.flags[flag]=False
    def get_flag(self,flag) :
        return self.flags[flag]
    def new_item(self,item) :
        self.items.append(item)
    def new_npc(self,npc) :
        self.npcs.append(npc)
    def say_npc(self,npc,message) :
        self.npcs[self.npcs.index(npc)].say(message)
    def remove_npc(self,npc) :
        self.npcs.remove(npc)
    def new_exit(self,exit,room) :
        self.exits[exit]=room
    def remove_item(self,item) :
        self.items.remove(item)
    def remove_exit(self,exit) :
        self.exits[exit]=None
def printitems(itemlist) :
    istr=""
    for item in itemlist :
        istr=istr+"\n"+item.shortdesc
    if istr == "" :
        istr="nothing"
    return istr
def roomdesc(room) :
    print room.name+"==="+room.description
    for item in room.items :
        print "\n"+item.grounddesc
    for i in room.npcs :
        print "\n"+"{} stands here".format(i.name)
    for exit in room.exits.keys() :
        if room.exits[exit] != None :
            print "\n"+exit+":"+room.exits[exit].name
def move(game,player,direction) :
    if game.world[player.currentroom.name].exits[direction] != None :
        player.currentroom=game.world[player.currentroom.name].exits[direction]
        roomdesc(player.currentroom)
    else :
        print "You cannot move that way."
class Parser(cmd.Cmd) :
    prompt="\n>"
    def __init__(self,game) :
        cmd.Cmd.__init__(self)
        self.game=game
    def default(self,args) :
        print "Unknown command."
    def do_north(self,args) :
        move(self.game,self.game.player,"north")
    do_n=do_north
    def do_south(self,args) :
        move(self.game,self.game.player,"south")
    do_s=do_south
    def do_east(self,args) :
        move(self.game,self.game.player,"east")
    do_e=do_east
    def do_west(self,args) :
        move(self.game,self.game.player,"west")
    do_w=do_west
    def do_northwest(self,args) :
        move(self.game,self.game.player,"northwest")
    do_nw=do_northwest
    def do_northeast(self,args) :
        move(self.game,self.game.player,"northeast")
    do_ne=do_northeast
    def do_southwest(self,args) :
        move(self.game,self.game.player,"southwest")
    do_sw=do_southwest
    def do_southeast(self,args) :
        move(self.game,self.game.player,"southeast")
    do_se=do_southeast
    def do_up(self,args) :
        move(self.game,self.game.player,"up")
    do_u=do_up
    def do_down(self,args) :
        move(self.game,self.game.player,"down")
    do_d=do_down
    def do_look(self,args) :
        if args == "" :
            roomdesc(self.game.player.currentroom)
        else :
            lookedat=False
            for item in self.game.player.inventory+self.game.player.currentroom.items :
                if args in item.descwords :
                    if item.open :
                        print item.longdesc+", it is open, it contains {}.".format(printitems(item.contents))
                    else :
                        print item.longdesc
                    lookedat=True
            for npc in self.game.player.currentroom.npcs :
                if args in npc.descwords :
                    print npc.description
                    lookedat=True
            if not lookedat :
                print "Cannot look at that."
    do_l=do_look
    def do_quit(self,args) :
        print "Thankyou for playing "+self.game.name
        return True
    do_exit=do_quit
    def do_take(self,args) :
        taken=False
        if args != "" :
            for item in self.game.player.currentroom.items :
                if args in item.descwords :
                    self.game.player.inventory.append(item)
                    print "You took "+item.shortdesc
                    self.game.player.currentroom.items.remove(item)
                    taken=True
            if not taken :
                print "Take what?"
        else :
            print "Take what?"
    do_get=do_take
    def do_drop(self,args) :
        if args !="" :
            dropped=False
            for item in self.game.player.inventory :
                if args in item.descwords :
                    print "You dropped "+item.shortdesc
                    self.game.player.currentroom.items.append(item)
                    self.game.player.inventory.remove(item)
                    dropped=True
            if not dropped :
                print "Drop what?"
        else :
            print "Drop what?"
    def do_inventory(self,args) :
        if self.game.player.inventory != [] :
            print "inventory"
            invstr=printitems(self.game.player.inventory)
            print invstr
        else :
            print "inventory\nnothing"
    do_i=do_inventory
    do_inv=do_inventory
    def do_eat(self,args) :
        if args != "" :
            eaten=False
            for item in self.game.player.inventory :
                if args in item.descwords and item.edible :
                    print "You eat "+item.shortdesc
                    self.game.player.inventory.remove(item)
                    eaten=True
            if not eaten :
                print "Eat what?"
        else :
            print "Eat what?"
    def do_drink(self,args) :
        if args != "" :
            drunk=False
            for item in self.game.player.inventory :
                if args in item.descwords and item.drinkible :
                    print "You drink "+item.shortdesc
                    self.game.player.inventory.remove(item)
                    drunk=True
            if not drunk :
                print "Drink what?"
        else :
            print "Drink what?"
    def do_open(self,args) :
        if args != "" :
            opened=False
            for item in self.game.player.inventory+self.game.player.currentroom.items :
                if args in item.descwords and item.openable and not item.open :
                    print "You open {}".format(item.shortdesc)
                    item.open=True
                    opened=True
            if not opened :
                print "Open what?"
        else :
            print "Open what?"
    def do_close(self,args) :
        if args != "" :
            closed=False
            for item in self.game.player.inventory+self.game.player.currentroom.items :
                if args in item.descwords and item.openable and item.open :
                    print "You close {}".format(item.shortdesc)
                    item.open=False
                    closed=True
            if not closed :
                print "Close what?"
        else :
            print "Close what?"
    def do_remove(self,args) :
        try :
            a=args.split(" from ")[0]
            b=args.split(" from ")[1]
            for item in self.game.player.inventory+self.game.player.currentroom.items :
                if b in item.descwords and item.openable and item.open :
                    bitem=item
            for item in bitem.contents :
                if a in item.descwords :
                    aitem=item
            self.game.player.inventory.append(aitem)
            bitem.contents.remove(aitem)
            print "You removed {} from {}".format(aitem.shortdesc,bitem.shortdesc)
        except :
            print "Remove what from what?"
    def do_put(self,args) :
        try :
            a=args.split(" in ")[0]
            b=args.split(" in ")[1]
            for item in self.game.player.inventory+self.game.player.currentroom.items :
                if b in item.descwords and item.openable and item.open :
                    bitem=item
            for item in self.game.player.inventory :
                if a in item.descwords :
                    aitem=item
            bitem.contents.append(aitem)
            print "You put {} in {}".format(aitem.shortdesc,bitem.shortdesc)
            self.game.player.inventory.remove(aitem)
        except :
            print "Put what in what?"
    def do_ask(self,args) :
        try :
            a=args.split(" about ")[0]
            b=args.split(" about ")[1]
            for npc in self.game.player.currentroom.npcs :
                if a in npc.descwords :
                    an=npc
            for question in an.askstrings.keys() :
                if b == question :
                    bq=question
            print an.askstrings[bq]
        except :
            print "Ask who about what?"
    def logic(self) :
        pass
    def postcmd(self,stop,line) :
        self.logic()
        return cmd.Cmd.postcmd(self,stop,line)