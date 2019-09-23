import pygame,time,random
from pygame.sprite import Sprite
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BG_COLOR = pygame.Color(0,0,0)
TEXT_COLOR = pygame.Color(255,0,0)
class BaseItem(Sprite):
    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)
class MainGame():
    window = None
    my_tank = None
    #地方坦克列表
    enemyTankList = []
    enemyTankCount = 5
    myBulletList = []
    enemyBulletlist = []
    explodeList = []
    wallList = []
    def __init__(self):
        pass
    #开始游戏
    def startGame(self):
        #加载主窗口
        #初始化窗口
        pygame.display.init()
        #设置窗口的大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        self.createMytank()
        #设置窗口的标题
        pygame.display.set_caption('坦克大战')
        MainGame.my_tank = Tank(350,350)
        self.createEnemyTank()
        self.createWall()
        #初始化地方坦克
        while True:
            #设置填充色
            time.sleep(0.02)
            MainGame.window.fill(BG_COLOR)
            self.getEvent()
            #绘制文字
            MainGame.window.blit(self.getTextSuface('敌方坦克剩余数量：%d'%len(MainGame.enemyTankList)),(10,10))
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
            else:
                del MainGame.my_tank
                MainGame.my_tank = None
            # MainGame.my_tank.displayTank()
            self.blitEnemyTank()
            self.blitMyBullet()
            self.blitEnemyBullet()
            self.blitExplode()
            self.blitWall()
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    #检测碰撞
                    MainGame.my_tank.hitWall()
            pygame.display.update()
    def createWall(self):
        for i in range(6):
            wall = Wall(i*130,220)
            MainGame.wallList.append(wall)
    #创建我方坦克的方法
    def createMytank(self):
        MainGame.my_tank = Tank(350,350)
    #初始化地方坦克，并将坦克添加到列表中
    def createEnemyTank(self):
        top = 100
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0,600)
            speed = random.randint(1,2)
            enemy = EnemyTank(left,top,speed)
            MainGame.enemyTankList.append(enemy)

    def blitWall(self):
        for wall in MainGame.wallList:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.wallList.remove(wall)
    def blitMyBullet(self):
        for myBullet in  MainGame.myBulletList:
            if myBullet.live:
                myBullet.displayBullet()
                myBullet.move()
                myBullet.myBullet_hit_enemyTank()
                myBullet.hitWall()
            else:
                MainGame.myBulletList.remove(myBullet)

    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            for enemyTank in MainGame.enemyTankList:
                if enemyTank.live:
                    enemyTank.displayTank()
                    enemyTank.randMove()
                    enemyBullet = enemyTank.shot()
                    if enemyBullet:
                        MainGame.enemyBulletlist.append(enemyBullet)
                else:
                    MainGame.enemyTankList.remove(enemyTank)
    def blitEnemyBullet(self):
        for enemyBullet in MainGame.enemyBulletlist:
            if enemyBullet.live:
                enemyBullet.displayBullet()
                enemyBullet.move()
                enemyBullet.enemyBullet_hit_myTank()
                enemyBullet.hitWall()
            else:
                MainGame.enemyBulletlist.remove(enemyBullet)

    def blitExplode(self):
        for explode in MainGame.explodeList:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.explodeList.remove(explode)

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
                #当坦克不存在或者死亡
                if not MainGame.my_tank:
                    #判断按下的是esc，让坦克重生
                    if event.key == pygame.K_ESCAPE:
                        self.createMytank()
                if MainGame.my_tank and MainGame.my_tank.live:
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
                        if len(MainGame.myBulletList) < 3:
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT\
                        or event.key == pygame.K_RIGHT:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        MainGame.my_tank.stop = True

class Tank(BaseItem):
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
        self.live = True
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    #移动
    def move(self):
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        #判断坦克的方向进行移动
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left  -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top +=self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed

    # 射击
    def shot(self):
        return Bullet(self)
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top  = self.oldTop
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                self.stay()
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
        super(EnemyTank,self).__init__(left,top)
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
        self.step = 40

    def randMove(self):
        if self.step <=0 :
            self.direction = self.randDirection()
            self.step = 40
        else :
            self.move()
            self.step -=1



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

    def shot(self):
        num = random.randint(1,20)
        if num <2:
            return Bullet(self)
# 子弹类
class Bullet(BaseItem):
    def __init__(self,tank):
        self.image = pygame.image.load('icon/bullet.png')
        self.direction = tank.direction
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left +tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top -self.rect.height
        elif self.direction == 'D':
            self.rect.left =tank.rect.left +tank.rect.width/2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width /2
            self.rect.top = tank.rect.top + tank.rect.width /2 -self.rect.width /2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2

        self.speed = 15
        self.live = True
    # 移动

    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0 :
                self.rect.top -= self.speed
            else :
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left +=self.speed
            else :
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top +=self.speed
            else :
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -=self.speed
            else:
                self.live = False

    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                self.live = False
                wall.hp -=1
                if wall.hp<=0:
                    #修改墙壁的生存状态
                    wall.live = False


    #展示子弹的方法
    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)

    def myBullet_hit_enemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_circle(enemyTank,self):
                enemyTank.live = False
                self.live = False
                explode = Explode(enemyTank)
                MainGame.explodeList.append(explode)

    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                # 产生爆炸对象
                explode = Explode(self)
                MainGame.explodeList.append(explode)
                self.live = False
                MainGame.my_tank.live = False


#墙壁类
class Wall():
    def __init__(self,left,top):
        self.image = pygame.image.load('icon/wall_1.bmp')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 3
        #设置生命值


    #展示墙壁方法
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)
#爆炸类
class Explode():
    def __init__(self,tank):
        self.rect = tank.rect
        self.images = [
            pygame.image.load('icon/b0.png'),
            pygame.image.load('icon/b1.png'),
            pygame.image.load('icon/b2.png'),
            pygame.image.load('icon/b3.png'),
            pygame.image.load('icon/b4.png'),
            pygame.image.load('icon/b5.png'),
            pygame.image.load('icon/b6.png'),
        ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True

    #展示爆炸效果方法
    def displayExplode(self):
        if self.step<len(self.images):
            self.image = self.images[self.step]
            self.step+=1
            MainGame.window.blit(self.image,self.rect)
        else:
            self.live = False
            self.step = 0

#音乐类
class Music():
    def __init__(self):
        pass
    #播放音乐
    def play(self):
        pass

if __name__ == '__main__':
    MainGame().startGame()
