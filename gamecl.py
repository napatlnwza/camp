"""
🚀 ASTEROID SHOOTER - เกมเครื่องบินรบยิงอุกาบาต
=====================================================
วิธีเล่น:
  - ลูกศรซ้าย/ขวา หรือ A/D  → เคลื่อนที่
  - กระสุนยิงอัตโนมัติตลอดเวลา
  - ยิงอุกาบาตแตก = +1 คะแนน
  - HP อุกาบาต = 100, ดาเมจ = 7-18 ต่อกระสุน
"""

import pygame
import random
import sys
import math

# ─────────────────────────────────────────
#  เริ่มต้น pygame
# ─────────────────────────────────────────
pygame.init()
pygame.font.init()

# ─────────────────────────────────────────
#  ค่าคงที่ (Constants)
# ─────────────────────────────────────────
SCREEN_W, SCREEN_H = 800, 700      # ขนาดหน้าจอ
FPS            = 60                 # เฟรมต่อวินาที
BULLET_SPEED   = 12                 # ความเร็วกระสุน (px/frame)
BULLET_RATE    = 12                 # ยิงทุกกี่เฟรม (น้อย = ยิงถี่)
ASTEROID_SPEED_MIN = 1.5           # ความเร็วอุกาบาตต่ำสุด
ASTEROID_SPEED_MAX = 3.5           # ความเร็วอุกาบาตสูงสุด
ASTEROID_SPAWN_RATE = 90           # สร้างอุกาบาตทุกกี่เฟรม
ASTEROID_HP    = 100               # HP อุกาบาต
DMG_MIN, DMG_MAX = 10, 18          # ช่วงดาเมจ

# ─────────────────────────────────────────
#  สี (Colors) - ธีม Neon Space
# ─────────────────────────────────────────
BLACK   = (0,   0,   0  )
WHITE   = (255, 255, 255)
CYAN    = (0,   220, 255)
ORANGE  = (255, 140, 0  )
RED     = (255, 60,  60 )
YELLOW  = (255, 230, 0  )
GRAY    = (150, 150, 150)
DARK_BG = (5,   5,   20 )          # พื้นหลังสีเข้มอวกาศ
STAR_COL= (180, 180, 220)
GREEN   = (80,  255, 120)
PURPLE  = (180, 80,  255)
DMGCOL  = (255, 255, 80 )          # สีตัวเลขดาเมจ

# ─────────────────────────────────────────
#  สร้างหน้าจอ
# ─────────────────────────────────────────
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("🚀 Asteroid Shooter")
clock  = pygame.time.Clock()

# ─────────────────────────────────────────
#  โหลดฟอนต์
# ─────────────────────────────────────────
font_big   = pygame.font.SysFont("Arial", 48, bold=True)
font_med   = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 20)
font_dmg   = pygame.font.SysFont("Arial", 22, bold=True)  # ฟอนต์ดาเมจ

# ─────────────────────────────────────────
#  ฟังก์ชันสร้างดาวพื้นหลัง
# ─────────────────────────────────────────
def make_stars(n=120):
    """สร้างดาวสุ่มตำแหน่งบนพื้นหลัง"""
    return [(random.randint(0, SCREEN_W),
             random.randint(0, SCREEN_H),
             random.choice([1, 1, 1, 2])) for _ in range(n)]

STARS = make_stars()

def draw_stars():
    """วาดดาวพื้นหลัง"""
    for x, y, r in STARS:
        pygame.draw.circle(screen, STAR_COL, (x, y), r)

# ─────────────────────────────────────────
#  คลาส: กระสุน (Bullet)
# ─────────────────────────────────────────
class Bullet:
    """กระสุนที่เครื่องบินยิงออกมา"""

    WIDTH, HEIGHT = 5, 18          # ขนาดกระสุน
    COLOR         = CYAN           # สีกระสุน
    GLOW          = (0, 100, 180)  # สีเรืองแสง

    def __init__(self, x, y):
        # x, y คือตำแหน่งเริ่มต้นของกระสุน (ตรงหัวเครื่องบิน)
        self.rect   = pygame.Rect(x - self.WIDTH // 2, y, self.WIDTH, self.HEIGHT)
        self.damage = random.randint(DMG_MIN, DMG_MAX)  # สุ่มดาเมจ 7-18
        self.alive  = True

    def update(self):
        """เลื่อนกระสุนขึ้นทุกเฟรม"""
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:   # ออกนอกจอ → ลบทิ้ง
            self.alive = False

    def draw(self):
        """วาดกระสุนพร้อม glow effect"""
        # วาด glow (เรืองแสงด้านนอก)
        glow_rect = self.rect.inflate(4, 4)
        pygame.draw.rect(screen, self.GLOW, glow_rect, border_radius=4)
        # วาดตัวกระสุน
        pygame.draw.rect(screen, self.COLOR, self.rect, border_radius=3)

# ─────────────────────────────────────────
#  คลาส: อุกาบาต (Asteroid)
# ─────────────────────────────────────────
class Asteroid:
    """อุกาบาตที่ตกลงมาจากด้านบน"""

    def __init__(self):
        self.radius = random.randint(28, 55)     # รัศมีสุ่ม
        self.x      = random.randint(self.radius, SCREEN_W - self.radius)
        self.y      = -self.radius               # เริ่มเหนือจอ
        self.speed  = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
        self.hp     = ASTEROID_HP                # HP เต็ม
        self.max_hp = ASTEROID_HP
        self.alive  = True
        self.angle  = 0                          # มุมหมุน
        self.spin   = random.uniform(-2, 2)      # ความเร็วหมุน
        # สร้างรูปทรงอุกาบาต (polygon สุ่ม)
        self.shape  = self._make_shape()
        self.color  = (random.randint(130, 180),
                       random.randint(100, 150),
                       random.randint(80, 120))  # สีน้ำตาลหินสุ่ม

    def _make_shape(self):
        """สร้างรูป polygon สุ่มสำหรับอุกาบาต"""
        pts = []
        sides = random.randint(7, 11)
        for i in range(sides):
            a = math.radians(i * 360 / sides)
            r = self.radius * random.uniform(0.75, 1.0)
            pts.append((math.cos(a) * r, math.sin(a) * r))
        return pts

    def _rotated_points(self):
        """คำนวณจุดหลังหมุนและย้ายตำแหน่ง"""
        rad = math.radians(self.angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        result = []
        for px, py in self.shape:
            rx = px * cos_a - py * sin_a + self.x
            ry = px * sin_a + py * cos_a + self.y
            result.append((rx, ry))
        return result

    def update(self):
        """เคลื่อนที่ลงและหมุน"""
        self.y     += self.speed
        self.angle += self.spin
        if self.y - self.radius > SCREEN_H:   # ออกนอกจอด้านล่าง
            self.alive = False

    def draw(self):
        """วาดอุกาบาตพร้อม HP bar"""
        pts = self._rotated_points()
        # คำนวณสีตามเปอร์เซ็นต์ HP (เต็ม=น้ำตาล, น้อย=แดง)
        hp_pct    = self.hp / self.max_hp
        r_col     = int(self.color[0] * hp_pct + 255 * (1 - hp_pct))
        g_col     = int(self.color[1] * hp_pct)
        b_col     = int(self.color[2] * hp_pct)
        draw_col  = (min(255, r_col), max(0, g_col), max(0, b_col))

        # วาดตัวอุกาบาต
        pygame.draw.polygon(screen, draw_col, pts)
        pygame.draw.polygon(screen, WHITE, pts, 2)

        # ─── HP Bar ─────────────────────────
        bar_w  = self.radius * 2
        bar_h  = 7
        bar_x  = int(self.x - self.radius)
        bar_y  = int(self.y - self.radius - 14)
        # พื้นหลัง HP bar (แดงเข้ม)
        pygame.draw.rect(screen, (100, 0, 0),
                         (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        # HP ที่เหลือ (เขียว → เหลือง → แดง)
        fill_w = int(bar_w * hp_pct)
        if hp_pct > 0.5:
            hp_color = GREEN
        elif hp_pct > 0.25:
            hp_color = YELLOW
        else:
            hp_color = RED
        if fill_w > 0:
            pygame.draw.rect(screen, hp_color,
                             (bar_x, bar_y, fill_w, bar_h), border_radius=3)
        # กรอบ HP bar
        pygame.draw.rect(screen, WHITE,
                         (bar_x, bar_y, bar_w, bar_h), 1, border_radius=3)

    def hit(self, damage):
        """ถูกกระสุน ลด HP"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp    = 0
            self.alive = False
            return True   # ตายแล้ว
        return False

    def collide_bullet(self, bullet):
        """ตรวจสอบว่ากระสุนชนอุกาบาตหรือเปล่า (วงกลม vs สี่เหลี่ยม)"""
        cx = bullet.rect.centerx
        cy = bullet.rect.centery
        dist = math.hypot(cx - self.x, cy - self.y)
        return dist < self.radius + 4

    def collide_player(self, player):
        """ตรวจสอบว่าอุกาบาตชนเครื่องบินหรือเปล่า (วงกลม vs วงกลม)"""
        dist = math.hypot(self.x - player.x, self.y - player.y)
        return dist < self.radius + 20   # 20 = รัศมีเครื่องบินโดยประมาณ

# ─────────────────────────────────────────
#  คลาส: ตัวเลขดาเมจ (DamageNumber)
# ─────────────────────────────────────────
class DamageNumber:
    """ตัวเลขที่ลอยขึ้นเมื่อยิงโดน"""

    def __init__(self, x, y, damage):
        self.x      = x + random.randint(-15, 15)  # กระจายนิดหน่อย
        self.y      = float(y)
        self.damage = damage
        self.life   = 50        # อายุ (เฟรม)
        self.alive  = True
        # สีตามดาเมจ: สูง=ส้ม, ต่ำ=เหลือง
        if damage >= 15:
            self.color = ORANGE
        elif damage >= 11:
            self.color = YELLOW
        else:
            self.color = WHITE

    def update(self):
        """ลอยขึ้นและลดความโปร่งใส"""
        self.y    -= 1.5       # ลอยขึ้น
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self):
        """วาดตัวเลขดาเมจพร้อม alpha"""
        alpha = int(255 * (self.life / 50))
        surf  = font_dmg.render(f"-{self.damage}", True, self.color)
        surf.set_alpha(alpha)
        screen.blit(surf, (int(self.x), int(self.y)))

# ─────────────────────────────────────────
#  คลาส: อนุภาคระเบิด (ExplosionParticle)
# ─────────────────────────────────────────
class ExplosionParticle:
    """อนุภาคระเบิดเมื่อเครื่องบินถูกชน"""

    def __init__(self, x, y):
        angle      = random.uniform(0, math.pi * 2)
        speed      = random.uniform(2, 9)
        self.vx    = math.cos(angle) * speed
        self.vy    = math.sin(angle) * speed
        self.x     = float(x)
        self.y     = float(y)
        self.life  = random.randint(25, 55)
        self.max_life = self.life
        self.alive = True
        self.r     = random.randint(3, 7)
        # สีแบบสุ่มระหว่างเหลือง-ส้ม-แดง
        self.color = random.choice([YELLOW, ORANGE, RED, WHITE, CYAN])

    def update(self):
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += 0.15          # แรงโน้มถ่วงเบาๆ
        self.vx   *= 0.97          # แรงต้านอากาศ
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self):
        alpha = int(255 * self.life / self.max_life)
        surf  = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (self.r, self.r), self.r)
        screen.blit(surf, (int(self.x) - self.r, int(self.y) - self.r))

# ─────────────────────────────────────────
#  คลาส: เครื่องบิน (Player)
# ─────────────────────────────────────────
class Player:
    """เครื่องบินรบของผู้เล่น"""

    SPEED = 6                         # ความเร็วเคลื่อนที่
    W, H  = 44, 56                    # ขนาดเครื่องบิน

    def __init__(self):
        self.x     = SCREEN_W // 2
        self.y     = SCREEN_H - 80
        self.rect  = pygame.Rect(self.x - self.W // 2,
                                 self.y - self.H // 2,
                                 self.W, self.H)

    def update(self, keys):
        """อัปเดตตำแหน่งตาม input"""
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.x -= self.SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.SPEED
        # จำกัดขอบจอ
        self.x = max(self.W // 2, min(SCREEN_W - self.W // 2, self.x))
        self.rect.centerx = self.x
        self.rect.centery  = self.y

    def draw(self):
        """วาดเครื่องบินด้วย polygon"""
        cx, cy = self.x, self.y
        # ─── ตัวเครื่องบิน ─────────────────
        body = [
            (cx,       cy - 26),   # หัว
            (cx + 18,  cy + 22),   # ปีกขวาล่าง
            (cx + 8,   cy + 14),   # เว้าขวา
            (cx,       cy + 20),   # ท้าย
            (cx - 8,   cy + 14),   # เว้าซ้าย
            (cx - 18,  cy + 22),   # ปีกซ้ายล่าง
        ]
        pygame.draw.polygon(screen, CYAN, body)
        pygame.draw.polygon(screen, WHITE, body, 2)

        # ─── กระจกนักบิน ──────────────────
        cockpit = [
            (cx,      cy - 16),
            (cx + 6,  cy),
            (cx,      cy + 4),
            (cx - 6,  cy),
        ]
        pygame.draw.polygon(screen, PURPLE, cockpit)

        # ─── เปลวไฟเครื่องยนต์ ─────────────
        flame_h = random.randint(14, 24)   # สั่นไหวแบบสุ่ม
        flame = [
            (cx - 6,  cy + 20),
            (cx,      cy + 20 + flame_h),
            (cx + 6,  cy + 20),
        ]
        pygame.draw.polygon(screen, ORANGE, flame)
        # ชั้นใน (สีเหลือง)
        inner_flame = [
            (cx - 3,  cy + 20),
            (cx,      cy + 20 + flame_h * 0.6),
            (cx + 3,  cy + 20),
        ]
        pygame.draw.polygon(screen, YELLOW, inner_flame)

    @property
    def gun_pos(self):
        """ตำแหน่งปืน (หัวเครื่องบิน)"""
        return (self.x, self.y - 28)

# ─────────────────────────────────────────
#  ฟังก์ชัน: วาด UI (คะแนน, ฯลฯ)
# ─────────────────────────────────────────
def draw_ui(score, frame):
    # ─── คะแนน ─────────────────────────
    score_surf = font_med.render(f"⭐ SCORE: {score}", True, YELLOW)
    screen.blit(score_surf, (16, 12))

    # ─── เฟรมนับ (debug/ข้อมูล) ────────
    info_surf = font_small.render(
        f"DMG: {DMG_MIN}-{DMG_MAX}  |  Asteroid HP: {ASTEROID_HP}", True, GRAY)
    screen.blit(info_surf, (16, SCREEN_H - 28))

    # ─── คำสั่งควบคุม ──────────────────
    ctrl_surf = font_small.render("← → / A D : เคลื่อนที่", True, GRAY)
    screen.blit(ctrl_surf, (SCREEN_W - ctrl_surf.get_width() - 16, SCREEN_H - 28))

def draw_score_popup(score, prev_score):
    """แสดง +1 เมื่อคะแนนเพิ่ม"""
    if score > prev_score:
        popup = font_med.render("+1 !", True, GREEN)
        screen.blit(popup, (SCREEN_W // 2 - 20, SCREEN_H // 2 - 20))

def draw_game_over(score):
    """หน้าจอ Game Over"""
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title   = font_big.render("GAME OVER", True, RED)
    sc_text = font_med.render(f"SCORE: {score}", True, YELLOW)
    retry   = font_med.render(" R play again  |  ESC escape", True, WHITE)

    screen.blit(title,   (SCREEN_W // 2 - title.get_width()   // 2, 240))
    screen.blit(sc_text, (SCREEN_W // 2 - sc_text.get_width() // 2, 310))
    screen.blit(retry,   (SCREEN_W // 2 - retry.get_width()   // 2, 380))

# ─────────────────────────────────────────
#  ฟังก์ชัน: รีเซ็ตเกม
# ─────────────────────────────────────────
def reset_game():
    return {
        "player"       : Player(),
        "bullets"      : [],
        "asteroids"    : [],
        "dmg_numbers"  : [],
        "particles"    : [],          # ← อนุภาคระเบิดเครื่องบิน
        "score"        : 0,
        "prev_score"   : 0,
        "frame"        : 0,
        "bullet_timer" : 0,
        "spawn_timer"  : 0,
        "game_over"    : False,
        "popup_timer"  : 0,
    }

# ─────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────
def main():
    state = reset_game()

    while True:
        clock.tick(FPS)

        # ─── ดึง event ─────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_r and state["game_over"]:
                    state = reset_game()   # เล่นใหม่

        if not state["game_over"]:
            keys = pygame.key.get_pressed()

            # ─── อัปเดตเครื่องบิน ─────────────
            state["player"].update(keys)

            # ─── ยิงกระสุนอัตโนมัติ ───────────
            state["bullet_timer"] += 1
            if state["bullet_timer"] >= BULLET_RATE:
                state["bullet_timer"] = 0
                gx, gy = state["player"].gun_pos
                state["bullets"].append(Bullet(gx, gy))

            # ─── สร้างอุกาบาต ──────────────────
            state["spawn_timer"] += 1
            if state["spawn_timer"] >= ASTEROID_SPAWN_RATE:
                state["spawn_timer"] = 0
                state["asteroids"].append(Asteroid())

            # ─── อัปเดตกระสุน ──────────────────
            for b in state["bullets"]:
                b.update()
            state["bullets"] = [b for b in state["bullets"] if b.alive]

            # ─── อัปเดตอุกาบาต ─────────────────
            for ast in state["asteroids"]:
                ast.update()

            # ─── ตรวจการชน: กระสุน <-> อุกาบาต ─
            state["prev_score"] = state["score"]
            state["popup_timer"] = max(0, state["popup_timer"] - 1)

            for ast in state["asteroids"]:
                if not ast.alive:
                    continue
                for b in state["bullets"]:
                    if not b.alive:
                        continue
                    if ast.collide_bullet(b):
                        # ─── โดนกระสุน! ─────────────
                        dmg = b.damage
                        dead = ast.hit(dmg)
                        b.alive = False          # กระสุนหายไป

                        # สร้างตัวเลขดาเมจ
                        state["dmg_numbers"].append(
                            DamageNumber(b.rect.centerx, b.rect.centery, dmg))

                        if dead:
                            state["score"] += 1   # +1 คะแนน
                            state["popup_timer"] = 30

            # ─── ลบออบเจกต์ที่ตายแล้ว ──────────
            state["asteroids"]   = [a for a in state["asteroids"]   if a.alive]
            state["dmg_numbers"] = [d for d in state["dmg_numbers"] if d.alive]

            # ─── ตรวจการชน: อุกาบาต <-> เครื่องบิน ─
            for ast in state["asteroids"]:
                if ast.collide_player(state["player"]):
                    # สร้างระเบิด 60 อนุภาค
                    px, py = state["player"].x, state["player"].y
                    for _ in range(60):
                        state["particles"].append(ExplosionParticle(px, py))
                    state["game_over"] = True
                    break

            # ─── อัปเดตตัวเลขดาเมจ ─────────────
            for dn in state["dmg_numbers"]:
                dn.update()

            # ─── อัปเดตอนุภาคระเบิด ────────────
            for p in state["particles"]:
                p.update()
            state["particles"] = [p for p in state["particles"] if p.alive]

            state["frame"] += 1

        # ─────────────────────────────────────
        #  วาด (Draw Phase)
        # ─────────────────────────────────────
        screen.fill(DARK_BG)         # พื้นหลังสีอวกาศ
        draw_stars()                 # วาดดาว

        # วาดอุกาบาต
        for ast in state["asteroids"]:
            ast.draw()

        # วาดกระสุน
        for b in state["bullets"]:
            b.draw()

        # วาดเครื่องบิน (ซ่อนเมื่อ game over)
        if not state["game_over"]:
            state["player"].draw()

        # วาดอนุภาคระเบิด
        for p in state["particles"]:
            p.draw()

        # วาดตัวเลขดาเมจ
        for dn in state["dmg_numbers"]:
            dn.draw()

        # วาด UI
        draw_ui(state["score"], state["frame"])

        # แสดง +1 popup
        if state["popup_timer"] > 0:
            alpha = int(255 * state["popup_timer"] / 30)
            surf  = font_med.render("+1 !", True, GREEN)
            surf.set_alpha(alpha)
            screen.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2,
                               SCREEN_H // 2 - 60))

        if state["game_over"]:
            draw_game_over(state["score"])

        pygame.display.flip()

# ─────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────
if __name__ == "__main__":
    main()