"""  本程序增加了半透明的圆形蔗罩mask，跟着拖曳的猴子移动。它的作用显示发射半径及提示不能在路径上放猴子。
发射原理是随机选择一只猴子,查找离它最近距离的泡泡。如果这个泡泡在发射半径，则计算方向向量，生成一枚子弹。
猴子是不能放在路径上的,如果靠得太近,则mask会切换造型进行提示,这时候松开鼠标指针是无法放置猴子。

操作方法：拖曳右上角的猴子，把它们放在离路径最近的地方。

本程序只是演示游戏基本原理，多关卡设计可以如下所示：
1、首先画好不同关卡的地图，画好后文件名为bg1.png,bg2.png,bg3.png.....
2、用程序“0_记录路径坐标.py”，加载不同的背景，自己拖曳鼠标指针，则会记录路径的坐标点，形成相应的path1.txt，path2.txt，path3.txt...
3、每关卡的泡泡数量不同，可以让泡泡数量随着关卡号的增加而增加，如建立self.pops_amount列表以记录每个关卡将会出现的泡泡数量。建立self.monkeys_amount列表存储每关可拖曳的猴子数量。
4、当有一个泡泡走完了整条路径，则表示防守失败。
5、当所有的泡泡被消灭，进入下一关，重新运行self.setup程序，加载新的path和背景等。


"""
import math
import random
import arcade

SCREEN_WIDTH = 1024                     # 常量定义，屏幕宽度
SCREEN_HEIGHT = 768                     # 常量定义,屏幕高度
SCREEN_TITLE = "猴子射汽球_arcade实现塔防游戏_原形程序by李兴球"# 常量定义,屏幕标题


class MyGame(arcade.Window):
    """    继承自窗口类的游戏类，在具体的游戏中，重写以下方法，删除不需要重写的方法。    """   

    def __init__(self, width, height, title):
        super().__init__(width, height, title)   #  调用父类的初始化方法新建一个窗口
        self.background = None
        self.path = []                           # 待读取的路径坐标表
        self.pops = None                         # 定义泡泡表
        self.frame_counter = 0                   # 帧计数器     
        
    def setup(self):
        """ 这个方法是在实例化Mygame后对游戏进行一些设置。 """
        self.pop_amounts = 50                  # 泡泡总数量
        self.pop_counter = self.pop_amounts    #
        self.hitedpop_amounts = 0              # 被击中的泡泡数量
        self.game_over = False
        self.success = False
        self.background = arcade.Sprite("images/bg.png")
        self.background.center_x = SCREEN_WIDTH//2
        self.background.center_y = SCREEN_HEIGHT//2
        self.pops = arcade.SpriteList()         # 泡泡列表实例化     
        f = open("poppath.txt")                 # 读取路径上所有坐标点
        for line in f:
            line = line.strip()
            if line=="" :continue
            x,y = line.split(",")
            x,y = int(x),int(y)
            self.path.append((x,y))
        f.close()
        #print(self.path)

        self.clicked_rect = (885,723,105,100)        # 右上角单击猴子矩形(left,top,width,height)
        self.clicked_monkey = arcade.Sprite("images/monkey.png")
        self.clicked_show = 0                        # 自定义属性，是否显示（重画）

        self.monkey_list = arcade.SpriteList()       # 发射子弹的猴子表

        self.mask = arcade.Sprite("images/mask.png") # 新建蒙板对象，猴子上面的那半透明圆圈
        self.mask.textures.append(arcade.load_texture("images/mask2.png")) # 增加纹理造型(有字:此处不能放)
        self.shoot_radius = self.mask.width//2
        # print("self.shoot_radius",self.shoot_radius) # 发射半径
        self.bullet_list = arcade.SpriteList()       # 子弹发射组

        
        
    def spawn_pop(self):
        """产生泡泡"""
        if self.game_over:return
        if self.pop_counter == 0 : return
        self.pop_counter = self.pop_counter - 1
        pop = arcade.Sprite("images/balloon.png")        
        pop.index = 0                             # 从0开始引用路径中坐标
        pop.center_x = self.path[pop.index][0]    # 起始点x坐标
        pop.center_y = self.path[pop.index][1]    # 起始点y坐标
        
        self.pops.append(pop)
        
    def on_draw(self):
        """ 渲染屏幕  ，帧率为60左右，即每60份之一秒会自动调用此方法  """        
        arcade.start_render()    # 此命令会用背景色填充屏幕，
        self.background.draw()
        if self.game_over == False:
            self.pops.draw()         # 画所有泡泡
            if  self.clicked_show >10:
                self.clicked_monkey.draw() # 单击后此猴显示
                self.mask.draw()
            self.monkey_list.draw()  # 画所有能发射子弹的猴子
            self.bullet_list.draw()  # 画子弹
        else:
            x = SCREEN_WIDTH//2
            y = SCREEN_HEIGHT//2
            if self.success:
               end_string = "防守成功！"
            else:
               end_string = "有个泡泡逃走了..." 
            arcade.draw_text(end_string,x,y, arcade.color.RED,24,font_name="simhei")            
            

    def update(self, delta_time):
        """ 所有的角色移动等游戏逻辑都在这里编写代码   """
        self.frame_counter +=1
        if self.frame_counter % 60 == 0 :       # 约1秒产生一个泡泡，可对数量进行限制
            self.spawn_pop()
        if self.pops:
            for pop in self.pops:
                if pop.index < len(self.path):  # 把每个泡泡放在路径坐标                 
                    pop.center_x = self.path[pop.index][0] # 起始点x坐标
                    pop.center_y = self.path[pop.index][1] # 起始点y坐标
                    pop.index += 1
                else:
                    pop.kill()                  # 超出路径则删除它,防守失败!
                    self.game_over = True
                    # print("Game Over")
                    
        if self.clicked_show > 0: self.clicked_show += 1


        # 随机选择一只猴子，让它发射
        if self.monkey_list and random.randint(1,10) == 1:  #   这里修改发射击的几率
           monkey = random.choice(self.monkey_list)     
          
           # 查找离它最近的泡泡,如果小于发射半径,则计算角度,让子弹从那个方向发射
           min_distance = 10000
           for pop in self.pops:   # 每个泡泡
               distance = arcade.get_distance_between_sprites(pop,monkey)
               if distance < min_distance :
                   min_distance = distance                  # 记录更小距离
                   min_pop = pop                            # 记录更小距离的泡泡
           if min_distance < self.shoot_radius:             # 找到小于发射半径的,则发射一颗子弹
                dy =  (min_pop.center_y - monkey.center_y )//8
                dx =  (min_pop.center_x-monkey.center_x   )//8
                bullet = arcade.Sprite("images/bullet.png")
                bullet.center_x = monkey.center_x
                bullet.center_y = monkey.center_y
                bullet.change_x = dx
                bullet.change_y = dy
                self.bullet_list.append(bullet)

        # 子弹组和泡泡组的碰撞检测
        for bullet in self.bullet_list:
           bs = arcade.check_for_collision_with_list(bullet,self.pops)# 返回碰到的泡泡列表
           if bs: bullet.kill() ;  self.hitedpop_amounts += len([pop.kill() for pop in bs])
           if self.hitedpop_amounts == self.pop_amounts :            # 击中的泡泡和总数相等，胜利结束。
               self.game_over = True
               self.success = True
               break
        self.bullet_list.update()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ 当按鼠标键时会自动地调用此方法     """
        if self.game_over:return
        if point_in_rect(x,y,self.clicked_rect ):
            # print("选中了右上角的猴子")
            self.clicked_show = 1          # 此变量一旦等于1,则在update中会自增
            # 以下代码可以对限制所放置的猴子的数量
   
    
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ 当鼠标移动时会自动地调用此方法 """
        if  self.clicked_show > 10:
            self.clicked_monkey.center_x = x
            self.clicked_monkey.center_y = y
            self.mask.center_x = x
            self.mask.center_y = y
            # 如果到path中某个坐标点距离太近,则不能放，下面查找距离鼠标指针最近的路径点
            min_distance = 100000
            for x2,y2 in self.path:
                dx = x - x2
                dy = y - y2
                distance = math.sqrt(dx*dx+dy*dy) # 鼠标指针和路径上的点的距离
                if distance < min_distance : min_distance = distance
            print("最小距离:",min_distance)
            if min_distance < (self.shoot_radius - 10): # mask切换到不能放的造型
                self.mask.cur_texture_index = 1
                self.mask.set_texture(1)
            else:
                self.mask.cur_texture_index = 0
                self.mask.set_texture(0)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """松开鼠标时调用此方法"""
        if self.mask.cur_texture_index == 1 : return     # 如果显示的是"此处不能放"造型,直接返回
        if self.clicked_show and self.clicked_show > 10: # 过了一定的帧数后才能生成一个猴子
            monkey = arcade.Sprite("images/monkey.png")
            monkey.center_x = x
            monkey.center_y = y
            self.monkey_list.append(monkey)
        # 松开后不会画它了，在此坐标生成一只自动发射的猴子
        self.clicked_show = 0
 

def point_in_rect(x,y,rect):
    """
       判断点是否rect矩形内。rect[0]:left,rect[1]:top,rect[2]:width,rect[3]:height
    """
    left = rect[0]
    right = rect[0] + rect[2]
    top = rect[1]
    bottom  = rect[1] - rect[3]
    return x > left and x < right  and y < top and y > bottom

def main():
    """主要的函数"""
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)  #  实例化一个游戏
    game.setup()                                      # 对游戏进行设置
    arcade.run()

    
if __name__ == "__main__":
    
      main()
