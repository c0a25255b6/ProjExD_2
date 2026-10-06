import os
import sys
import pygame as pg
import random
import time 



WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_RIGHT:(+5,0), 
    pg.K_LEFT:(-5,0)  
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rect: pg.Rect) -> tuple[bool,bool]:
    """""
    引数：こうかとん又は爆弾のRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTure/画面外ならFalse
    """""
    
    yoko,tate = True,True
    if rect.left < 0 or WIDTH < rect.right: #横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom: #縦方向判定
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
        Surface = pg.Surface((WIDTH,HEIGHT))
        pg.draw.rect(Surface,(0,0,0),(0,0,800,600))
        Surface.get_alpha()
        Surface.set_alpha(200)

        fonto = pg.font.Font(None, 80)
        txt =fonto.render("Game Over",True,(255,255,255))
        koukatonSurface = pg.image.load("fig/8.png")
        screen.blit(Surface,[0,0])
        screen.blit(txt,[400,280])
        screen.blit(koukatonSurface,[330,270])#文字の左側にこうかとん
        screen.blit(koukatonSurface,[730,270])#文字の右側にこうかとん
        
        pg.display.update()
        time.sleep(5)
        return

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) 
    pg.draw.circle(bb_img,(255,0,0),(10,10), 10) #赤い爆弾
    bb_img.set_colorkey((0,0,0)) #四隅の黒い部分を透過する
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH) #横方向の乱数
    bb_rct.centery = random.randint(0,HEIGHT) #縦方向の乱数
    vx,vy = +5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): #練習４：kkとbbのrectが重なっていたら
            print("game over")
            gameover(screen)
            return



        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0] #横方向移動量
                sum_mv[1] += tpl[1] #縦方向移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True): #どこかしらはみ出ている
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #先ほどの動きをキャンセルする
        screen.blit(kk_img, kk_rct) 


        bb_rct.move_ip(vx,vy) #練習２：爆弾動く
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct) #練習２：爆弾
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
