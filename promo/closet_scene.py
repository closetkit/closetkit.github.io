# Closet Kit 홍보 영상 — 3D "옷장 레일" 샷
# 사용: python closet_scene.py --  (pip 의 bpy 5.x, OIDN 디노이저 포함)
#   또는 blender -b -P closet_scene.py -- <aspect: v|h> <out_dir> [frame_start frame_end] [scale%] [samples]
import bpy, json, math, random, sys, os

argv = sys.argv[sys.argv.index('--') + 1:]
ASPECT = argv[0]
OUT = argv[1]
F0 = int(argv[2]) if len(argv) > 2 else 1
F1 = int(argv[3]) if len(argv) > 3 else 150
SCALE = int(argv[4]) if len(argv) > 4 else 100
SAMPLES = int(argv[5]) if len(argv) > 5 else 48
HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = json.load(open(os.path.join(HERE, 'cards', 'cards.json')))

FPS, LEN = 30, 150
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, LEN

def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]

BG = srgb('#13111c'); ACCENT = srgb('#9b83ff')

# --- 월드 / 렌더 설정 ---
world = bpy.data.worlds.new('W'); sc.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = BG
r = sc.render
r.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = SAMPLES
sc.cycles.use_adaptive_sampling = True
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 1
sc.cycles.diffuse_bounces = sc.cycles.glossy_bounces = sc.cycles.transmission_bounces = 0
sc.cycles.transparent_max_bounces = 16
sc.view_settings.view_transform = 'Standard'
sc.view_settings.look = 'None'
if ASPECT == 'v': r.resolution_x, r.resolution_y = 1080, 1920
else: r.resolution_x, r.resolution_y = 1920, 1080
r.resolution_percentage = SCALE
r.image_settings.file_format = 'PNG'
r.image_settings.color_mode = 'RGB'
r.filepath = os.path.join(OUT, '####')

# --- 재질 ---
def card_mat(path):
    m = bpy.data.materials.new(os.path.basename(path)); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(path); tex.interpolation = 'Cubic'
    emi = nt.nodes.new('ShaderNodeEmission')
    back = nt.nodes.new('ShaderNodeEmission'); back.inputs[0].default_value = srgb('#241f36')
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    face = nt.nodes.new('ShaderNodeMixShader')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    L = nt.links
    L.new(tex.outputs['Color'], emi.inputs['Color'])
    L.new(geo.outputs['Backfacing'], face.inputs[0]); L.new(emi.outputs[0], face.inputs[1]); L.new(back.outputs[0], face.inputs[2])
    L.new(tex.outputs['Alpha'], mix.inputs[0]); L.new(tr.outputs[0], mix.inputs[1]); L.new(face.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], out.inputs[0])
    return m

def glow_mat(name, col, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True
    e = m.node_tree.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = col; e.inputs[1].default_value = strength
    m.node_tree.links.new(e.outputs[0], m.node_tree.nodes['Material Output'].inputs[0])
    return m

# --- 두 줄의 옷장 레일 ---
H = 1.5; GAP = 0.32
random.seed(7)
order = list(range(len(CARDS))); random.shuffle(order)
rings = [order[0::2], order[1::2]]
ZS = [0.86, -0.86]
rail_m = glow_mat('rail', ACCENT, 2.5)
pivots = []
for ri, idx in enumerate(rings):
    widths = [H * CARDS[i]['w'] / CARDS[i]['h'] for i in idx]
    circ = sum(widths) + GAP * len(widths)
    R = circ / (2 * math.pi)
    piv = bpy.data.objects.new(f'ring{ri}', None); sc.collection.objects.link(piv); piv.location = (0, 0, ZS[ri])
    s = 0
    for i, w in zip(idx, widths):
        a = -math.pi / 2 + (s + w / 2) / R   # 0번 카드가 카메라 정면(-Y)
        s += w + GAP
        bpy.ops.mesh.primitive_plane_add(size=1)
        p = bpy.context.object
        p.scale = (w, H, 1)
        p.rotation_euler = (math.pi / 2, 0, a + math.pi / 2)
        p.location = (R * math.cos(a), R * math.sin(a), 0)
        p.data.materials.append(card_mat(os.path.join(HERE, 'cards', CARDS[i]['path'])))
        p.parent = piv
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=0.012, major_segments=192, minor_segments=8,
                                     location=(0, 0, ZS[ri] + H / 2 + 0.1))
    bpy.context.object.data.materials.append(rail_m)
    pivots.append((piv, R))

# 회전: 위 줄은 시계 반대, 아래 줄은 시계 방향 (일정한 속도)
prefs = bpy.context.preferences.edit
prefs.keyframe_new_interpolation_type = 'LINEAR'
for (piv, R), sgn in zip(pivots, (1, -1)):
    piv.rotation_euler = (0, 0, 0); piv.keyframe_insert('rotation_euler', index=2, frame=1)
    piv.rotation_euler = (0, 0, sgn * math.radians(48)); piv.keyframe_insert('rotation_euler', index=2, frame=LEN)
prefs.keyframe_new_interpolation_type = 'BEZIER'  # 카메라는 부드럽게 시작·정지

# --- 보케 조명 ---
cols = [srgb('#9b83ff'), srgb('#c4b5ff'), srgb('#ff8fd8'), srgb('#7fb4ff')]
bm = [glow_mat(f'b{i}', c, 4) for i, c in enumerate(cols)]
random.seed(3)
for i in range(70):
    x = random.uniform(-9, 9); y = random.uniform(1.5, 12); z = random.uniform(-5, 5)
    if abs(x) < 4 and y < 4: y += 4
    bpy.ops.mesh.primitive_uv_sphere_add(radius=random.uniform(0.05, 0.16), segments=12, ring_count=8, location=(x, y, z))
    bpy.context.object.data.materials.append(random.choice(bm))

# --- 카메라 ---
Rf = max(R for _, R in pivots)
focus = bpy.data.objects.new('focus', None); sc.collection.objects.link(focus); focus.location = (0, -Rf, 0)
cam_d = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam_d.sensor_fit = 'AUTO'; cam_d.sensor_width = 36
cam_d.lens = 36 if ASPECT == 'v' else 24
cam_d.dof.use_dof = True; cam_d.dof.focus_object = focus; cam_d.dof.aperture_fstop = 0.07
look = bpy.data.objects.new('look', None); sc.collection.objects.link(look); look.location = (0, -Rf, 0)
tc = cam.constraints.new('TRACK_TO'); tc.target = look; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
d0, d1 = (6.6, 5.6) if ASPECT == 'v' else (6.0, 5.0)
for f, d, x, z in ((1, d0, -0.35, 0.45), (LEN, d1, 0.35, -0.15)):
    cam.location = (x, -Rf - d, z); cam.keyframe_insert('location', frame=f)

os.makedirs(OUT, exist_ok=True)
sc.frame_start, sc.frame_end = F0, F1
bpy.ops.render.render(animation=True)
