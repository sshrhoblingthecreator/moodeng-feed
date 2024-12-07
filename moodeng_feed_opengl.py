@ -0,0 +1,358 @@
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random, math,time  # นำเข้าเวลา

# สร้างหน้าต่างเกม
app = Ursina()
#----------------------------------------------------
# อัปเดตโค้ดที่เกี่ยวข้องกับฟีเจอร์หลอดแสดงคะแนน
class ScoreBar(Entity):
    def __init__(self, max_score=500, **kwargs):
        super().__init__(parent=camera.ui, model='quad', color=color.dark_gray, scale=(0.5, 0.05), position=(-0.5, 0.45))
        self.bar = Entity(parent=self, model='quad', color=color.green, scale=(0, 1), origin=(-0.5, 0))
        self.max_score = max_score
        self.score = 0

    def update_score(self, score):
        self.score = score
        progress = min(self.score / self.max_score, 1)
        self.bar.scale_x = progress

# ฟังก์ชันแสดงเส้นระยะ
def draw_trajectory_line(start, end, steps=10):
    positions = [lerp(start, end, n / steps) for n in range(steps + 1)]
    lines = [Entity(model=Mesh(vertices=[positions[i], positions[i + 1]], mode='line'), color=color.red) for i in range(steps)]
    invoke(destroy_lines, lines, delay=0.5)

def destroy_lines(lines):
    for line in lines:
        destroy(line)

# เริ่มต้นด้วยการเพิ่มหลอดคะแนน
score_bar = ScoreBar()
#----------------------------------------------------
# พื้นดิน
ground = Entity(
    model='Floorwater_p.obj',
    texture='Floorwater_Floorwater_BaseColor.1001.png',
    scale=(2.3, 1, 2.3),
    position=(0, -1, 0),
    collider='box',
    texture_scale=(1, 1),
    texture_rotation=(90,0,0)
)

# ผนัง
wall = Entity(
    model='model/wall_p.obj',
    texture='sourceimages/wall_main_BaseColor.png',
    scale=(2.1, 1, 2.1),
    position=(0, 0, 0)
)

# โมเดลต้นไม้ 2
tree2 = Entity(
    model='model/tree2_p.obj',
    texture='sourceimages/tree2_main_BaseColor.png',
    scale=(1, 1.3, 1),
    position=(-13, 0, -10),
    collider='box'
)

# โมเดลต้นไม้ 1
tree1 = Entity(
    model='model/tree1_p.obj',
    texture='sourceimages/tree1_main_BaseColor.png',
    scale=(1, 1.3, 1.),
    position=(15, 0, -15),
    rotation=(0, 45, 0),
    collider='box'
)

# โมเดลหิน 1
rock1 = Entity(
    model='model/rock1_p.obj',
    texture='rock1_skinrock1_BaseColor.1001.png',
    scale=(2, 2, 2),
    position=(11, -0.3, 12),
    rotation=(0, 0, 0),
    collider='box',
)

# โมเดลหิน 2
rock2 = Entity(
    model='model/rock2_p.obj',
    texture='rock2_skinrock2_BaseColor.1001.png',
    scale=(2, 2, 2),
    position=(11, -0.3, 5),
    rotation=(0, 0, 0),
    collider='box',
)

flower1 = Entity(
    model='model/flower_small_p.obj',
    texture='flowersmall_standardSurface1_BaseColor.1001.png',
    scale=(2, 2, 2),
    position=(8, -0.3, 5),
    rotation=(0, 0, 0),
    collider='box',
)

cave1 = Entity(
    model='model/rock1_p.obj',
    texture='rock1_skinrock1_BaseColor.1001.png',
    scale=(2, 2, 2),
    position=(-20, 2, -10),
    rotation=(0, 30, 0),
    collider='box',
)
cave2 = Entity(
    model='model/rock2_p.obj',
    texture='rock2_skinrock2_BaseColor.1001.png',
    scale=(2, 2, 2),
    position=(-21, -0.3, -10),
    rotation=(0, 0, 0),
    collider='box',
)
cave3 = Entity(
    model='model/rock2_p.obj',
    texture='rock2_skinrock2_BaseColor.1001.png',
    scale=(3, 5, 2),
    position=(-17, -0.3, -14),
    rotation=(0, 0, 0),
    collider='box',
)
cave4 = Entity(
    model='model/rock2_p.obj',
    texture='rock2_skinrock2_BaseColor.1001.png',
    scale=(3, 5, 3),
    position=(-12, -0.3, -16),
    rotation=(15, 77, 20),
    collider='box',
)
cave5 = Entity(
    model='model/rock1_p.obj',
    texture='rock1_skinrock1_BaseColor.1001.png',
    scale=(2, 2, 2),
    position=(-2, -0.3, -10),
    rotation=(10, 20, 0),
    collider='box',
)
cave6 = Entity(
    model='model/rock2_p.obj',
    texture='rock2_skinrock2_BaseColor.1001.png',
    scale=(2, 2, 2),
    position=(-5, -0.3, -15.5),
    rotation=(60, 0, 0),
    collider='box',
)
cave4 = Entity(
    model='model/rock2_p.obj',
    texture='rock2_skinrock2_BaseColor.1001.png',
    scale=(7, 2, 8),
    position=(-12, 3, -16),
    rotation=(15, 77, 20),
    collider='box',
)
# water_basin = Entity(
#     model='model/basin_p.obj',
#     texture='sourceimages/basin_standardSurface2SG_BaseColor.png',
#     scale=(1, 1, 1),
#     position=(7, 0.2, 10),
#     rotation=(0, 0, 0),
#     collider='box'
# )

water_feed = Entity(
    model='model/water_feeder_p.obj',
    texture='sourceimages/water_feeder_water_feeder_aiStandardSurface1SG_BaseColor.1001.png',
    scale=(1, 1, 1),
    position=(7, 0.2, 10),
    rotation=(0, 0, 0),
    collider='box',
)

log_wood = Entity(
    model='model/log_p.obj',
    texture='sourceimages/log_standardSurface2SG_BaseColor.png',
    scale=(2, 2, 3),
    position=(5,-1.5, 15),
    rotation=(0, 90, 0),
    collider='box',
)

# หมูเด้ง
hippo = Entity(
    model='model/moodeng_p.obj',
    texture='modeng_modeng_BaseColor.1001.png',
    scale=(1, 0.8, 1),
    position=(0, 0.5, 0),
    collider='box',
    collider_scale=(2, 3, 2),
)

# ขอบเขตการเคลื่อนไหว
bound_x = (-20, 20)
bound_z = (-20, 20)

# ความเร็วในการเคลื่อนไหว
speed = 3

# ทิศทางการเคลื่อนไหวเริ่มต้น
direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()

# ตัวละครผู้เล่น FPS
player = FirstPersonController(
    position=(-10, 1, 0),
    collider='box'
)

# ตัวแปรเก็บคะแนน
score = 0
score_text = Text(f"Score: {score}", position=(-0.85, 0.45), scale=2)

# โมเดลอาหารที่สุ่มได้
food_models = [
    {'model': 'fruit.obj', 'texture': 'fruit_straw_BaseColor.png', 'points': 10},
    {'model': 'fruit.obj', 'texture': 'fruit_orange_BaseColor.png', 'points': 5},
    {'model': 'fruit.obj', 'texture': 'fruit_melonn_BaseColor.png', 'points': 15},
    {'model': 'fruit.obj', 'texture': 'tree1_main_BaseColor.png', 'points': -10}
]

# สุ่มอาหารเริ่มต้น
current_food = random.choice(food_models)

# ฟังก์ชันการสุ่มอาหาร
def spawn_food():
    global current_food
    current_food = random.choice(food_models)  # อัปเดต current_food ทุกครั้งที่เรียก spawn_food

    # อัปเดต texture ของ hand_item
    hand_item.texture = current_food['texture']

    food = Entity(
        model='fruit.obj',
        texture=current_food['texture'],
        scale=0.5,
        position=player.position + player.forward * 2 + Vec3(0, 1.5, 0),
        collider='box',
        visible=True
    )
    food.points = current_food['points']
    food.animate_position(food.position + player.forward * 5, duration=1, curve=curve.linear)
    return food

hand_item = Entity(
    model='fruit.obj',
    texture=current_food['texture'],
    scale=(0.3, 0.3, 0.3),
    position=(0.5, -0.5, 1),
    parent=camera,
    rotation=(10, -10, 0)
)

# ฟังก์ชันตรวจสอบการชน
def check_collision(food):
    global score
    if food and food.collider:
        if food.intersects(hippo).hit:  # ตรวจสอบการชนโดยตรงกับ hippo
            score += food.points
            score_text.text = f"Score: {score}"
            print(f"Food collided with hippo! Score: {score}")
        else:
            print("Food is not hitting the hippo.")
    destroy(food)

# ฟังก์ชันการโยนอาหารและการวาดเส้น
def throw_item():
    global current_food, score
    food = spawn_food()
    invoke(check_collision, food, delay=0.5)

# ฟังก์ชันสำหรับแสดง/ซ่อน Hitbox ของ Hippo
def toggle_hitbox():
    hippo.show_hitbox = not getattr(hippo, 'show_hitbox', False)
    if hippo.show_hitbox:
        hippo.collider.visible = True
        print("Hitbox ของ Hippo เปิดใช้งาน")
    else:
        hippo.collider.visible = False
        print("Hitbox ของ Hippo ถูกซ่อน")

# ฟังก์ชันวาดวงกลมใต้ Player
def draw_circle_under_player():
    center = player.position
    radius = 3  # กำหนดรัศมีวงกลม
    segments = 36
    angle_step = 360 / segments

    circle_points = [
        Vec3(center.x + math.cos(math.radians(angle_step * i)) * radius, center.y, center.z + math.sin(math.radians(angle_step * i)) * radius)
        for i in range(segments + 1)
    ]

    circle_mesh = Mesh(vertices=circle_points, mode='line')
    circle_entity = Entity(model=circle_mesh, color=color.blue)
    invoke(destroy, circle_entity, delay=0.5)  # ลบวงกลมหลังแสดง 0.5 วินาที

# ฟังก์ชันอินพุตเพื่อเพิ่มการกดปุ่ม Alt
def input(key):
    global mouse_locked
    if key == 'shift':
        mouse.locked = not mouse.locked
        Cursor.visible = not Cursor.visible

    if key == 'scroll up':
        camera.fov = max(camera.fov - 2, 20)
    elif key == 'scroll down':
        camera.fov = min(camera.fov + 2, 100)

    # กด Alt เพื่อสลับแสดงผล Hitbox และวงกลมใต้ Player
    if key == 'alt':
        toggle_hitbox()
        draw_circle_under_player()

# ตัวแปรเก็บเวลาคลิกล่าสุด
last_click_time = 0
cooldown_time = 0.5  # เวลาหน่วง 0.5 วินาที

# ฟังก์ชันการตรวจสอบการคลิกซ้าย
def update():
    global last_click_time, score, direction, speed

    current_time = time.time()  # เวลาปัจจุบันในวินาที


    score_bar.update_score(score)  # อัปเดตหลอดคะแนน

    if mouse.left and (current_time - last_click_time) >= cooldown_time:  # ถ้าคลิกซ้ายและยังไม่หมดเวลา cooldown
        last_click_time = current_time  # อัปเดตเวลาคลิกล่าสุด
        throw_item()  # เรียกใช้ฟังก์ชันโยนอาหาร

    # เฟส 1: คะแนน < 100 หมูเด้งอยู่นิ่ง
    if score < 100:
        speed = 0

    # เฟส 2: คะแนน 100-199 หมูเด้งเคลื่อนที่ด้วยความเร็วปกติ
    elif 100 <= score < 200:
        speed = 3

    # เฟส 3: คะแนน 200-299 หมูเด้งเคลื่อนที่และกระโดด
    elif 200 <= score < 300:
        speed = 5

    # เฟส 4: คะแนน >= 300 หมูเด้งเคลื่อนที่เร็วขึ้นและหยุดกระโดด
    else:
        speed = 9

    # เคลื่อนที่ไปตามทิศทางที่กำหนด
    hippo.position += direction * speed * time.dt

    # การหมุนให้นุ่มนวล
    target_rotation_y = -math.degrees(math.atan2(direction.x, direction.z))
    hippo.rotation_y = lerp(hippo.rotation_y, target_rotation_y, 4 * time.dt)

    # ตรวจสอบการชนกับขอบเขต
    if hippo.x <= bound_x[0] or hippo.x >= bound_x[1]:
        direction.x *= -1
    if hippo.z <= bound_z[0]
