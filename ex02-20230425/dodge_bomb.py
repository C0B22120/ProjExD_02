import random
import sys

import pygame as pg

delta = {
        pg.K_UP:[0,-1],
        pg.K_DOWN:[0,+1],
        pg.K_LEFT:[-1,0],
        pg.K_RIGHT:[+1,0] 
         }  #移動用辞書
def check_bound(scr_rct: pg.rect,obj_rct: pg.rect) -> tuple[bool,bool]: 
    """
    オブジェクトが画面内か画面外であるかを判定しその真偽値タプルを返す
    引数１：画面Surfaceのrect
    引数２：こうかとん または 爆弾のSurfaceのract
    戻り値：横、縦のはみ出し判定結果　（画面内:True、画面外:False）
    """
    yoko , tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02-20230425/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02-20230425/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect() #こうかとんのrect
    lv_count=0
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20,20))  #bombの描画
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))  #爆弾の透過
    x,y = random.randint(0,1600) , random.randint(0,900)  #ランダムな座標の指定
    #screen.blit(bb_img,[x,y])
    
    vx,vy = +1 , +1
    bb_rct=bb_img.get_rect()
    bb_rct.center = x , y
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1
        key_lst = pg.key.get_pressed()
        for k,mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)

        if check_bound(screen.get_rect(),kk_rct) != (True,True):  #画面端を越えようとしていないか確認する
            for k,mv in delta.items():
                if key_lst[k] :
                    kk_rct.move_ip(-mv[0],-mv[1])
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(screen.get_rect(),bb_rct)
        if not yoko:  #横方向にはみ出ていたら
            vx *= -1
        if not tate:
            vy *=  -1  #縦方向にはみ出ていたら
        if tmr % 600 == 0:  #一定時間経過で加速->レベルアップ
            lv_count +=1
            if lv_count <= 10 :  #加速する回数は10まで
                vx *= 1.2
                vy *= 1.2

        screen.blit(bb_img,bb_rct)  #爆弾の表示
        fonto  = pg.font.Font(None, 100)
        tm_txt = fonto.render(str(tmr), True, (0, 0,0))  
        lv_txt = fonto.render(str(lv_count),True,(0,0,0))
        screen.blit(tm_txt, [0, 0])  #経過時間表示
        screen.blit(lv_txt,[0,100])  #レベル表示

        if kk_rct.colliderect(bb_rct):  
            kk_img = pg.image.load("ex02-20230425/fig/8.png")
            screen.blit(bg_img,[0,0])
            screen.blit(tm_txt, [0, 0])
            screen.blit(lv_txt,[0,100])
            screen.blit(kk_img,[800,400])

            pg.display.update()
            pg.time.wait(5000)  #一定の時間の間止める
            return

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()