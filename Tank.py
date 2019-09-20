import pygame,time,random
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0,0,0)
TEXT_COLOR = pygame.Color(255,0,0)
class MainGame():
    window = None
    my_tank = None
    #地方坦克列表
    enemyTankList = []
    enemyTankCount = 5
    def __init__(self):
        pass
    #开始游戏
    def startGame(self):
        #加载主窗口
        #初始化窗口
        pygame.display.init()
        #设置窗口的大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        #设置窗口的标题
        pygame.display.set_caption('坦克大战')
        MainGame.my_tank = Tank(350,250)
        self.createEnemyTank()
        #初始化地方坦克
        while True:
            #设置填充色
            time.sleep(0.02)
            MainGame.window.fill(BG_COLOR)
            self.getEvent()
            #绘制文字
            MainGame.window.blit(self.getTextSuface('敌方坦克剩余数量：%d'%5),(10,10))
            MainGame.my_tank.displayTank()
            self.blitEnemyTank()
            if not MainGame.my_tank.stop:
                MainGame.my_tank.move()
            pygame.display.update()

    #初始化地方坦克，并将坦克添加到列表中
    def createEnemyTank(self):
        top = 100
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0,600)
            speed = random.randint(1,4)
            enemy = EnemyTank(left,top,speed)
            MainGame.enemyTankList.append(enemy)

    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            enemyTank.displayTank()
    #结束游戏
    def endGame(self):
        print('谢谢使用，bye')
        exit()
    #左上角文字的绘制
    def getTextSuface(self,text):
        pygame.font.init()
        #查看所有可用的字体名称
        #print(pygame.font.get_font())
        #获取字体Font对象
        font = pygame.font.SysFont('kaiti',18)
        textSurface = font.render(text,True,TEXT_COLOR)
        return textSurface
    #获取事件
    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    MainGame.my_tank.direction = 'L'
                    # MainGame.my_tank.move()
                    MainGame.my_tank.stop = False
                    print('左键被按下，坦克向左移动')
                elif event.key == pygame.K_RIGHT:
                    MainGame.my_tank.direction = 'R'
                    # MainGame.my_tank.move()
                    MainGame.my_tank.stop = False
                    print('右键被按下，坦克向右移动')
                elif event.key == pygame.K_UP:
                    MainGame.my_tank.direction = 'U'
                    # MainGame.my_tank.move()
                    MainGame.my_tank.stop = False
                    print('上键被按下，坦克向上移动')
                elif event.key == pygame.K_DOWN:
                    MainGame.my_tank.direction = 'D'
                    # MainGame.my_tank.move()
                    MainGame.my_tank.stop = False
                    print('下键被按下，坦克向下移动')
                elif event.key == pygame.K_SPACE:
                    print('发射子弹')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT\
                        or event.key == pygame.K_RIGHT:
                    MainGame.my_tank.stop = True

class Tank:
    def __init__(self,left,top):
        self.images = {
            'U':pygame.image.load('icon/tank_U.png'),
            'L':pygame.image.load('icon/tank_L.png'),
            'R':pygame.image.load('icon/tank_R.png'),
            'D':pygame.image.load('icon/tank_D.png'),
        }
        self.direction = 'R'
        #根据当前图片的方向获取图片
        self.image = self.images[self.direction]
        #获取区域
        self.rect = self.image.get_rect()
        #设置区域的top和left
        self.rect.left = left
        self.rect.top = top
        self.speed = 10
        #坦克移动开关
        self.stop = True
    #移动
    def move(self):
        #判断坦克的方向进行移动
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left  -= self.speed
        elif self.direction == 'U':
            if self.rect.top >0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top +=self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed

    # 射击
    def shot(self):
        pass

    # 展示坦克方法
    def displayTank(self):
        #获取展示的对象
        self.image = self.images[self.direction]
        #blit方法展示
        MainGame.window.blit(self.image,self.rect)


#我方坦克
class MyTank(Tank):
    def __init__(self):
        pass


#敌方坦克
class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        #加载图片集
        self.images = {
            'U':pygame.image.load('icon/EnemyTank_U.png'),
            'R':pygame.image.load('icon/EnemyTank_R.png'),
            'L':pygame.image.load('icon/EnemyTank_L.png'),
            'D':pygame.image.load('icon/EnemyTank_D.png')
        }
        #方向,随机坦克方向

        self.direction=self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.flag = True



    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'
# 子弹类
class Bullet():
    def __init__(self):
        pass
    # 移动

    def move(self):
        pass

    #展示子弹的方法
    def displayBullet(self):
        pass
#墙壁类
class Wall():
    def __init__(self):
        pass

    #展示墙壁方法
    def displayWall(self):
        pass
#爆炸类
class Explode():
    def __init__(self):
        pass

    #展示爆炸效果方法
    def displayExplode(self):
        pass
#音乐类
class Music():
    def __init__(self):
        pass
    #播放音乐
    def play(self):
        pass

if __name__ == '__main__':
    MainGame().startGame()
