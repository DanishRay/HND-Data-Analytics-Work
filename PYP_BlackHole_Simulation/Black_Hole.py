import math
import numpy as np
import pygame
from dataclasses import dataclass


# CONSTANTS
G = 1.0
M = 100.0
RS = 5.0                 # event horizon
DT = 0.01
NUM_STARS = 200
NUM_DISK_PARTICLES = 3000
NUM_GLOW_PARTICLES = 1200   # bright photon-ring

# Physics constants
INFALL_VELOCITY = 0.01

# Graphical constants 
DISTORTION_STRENGTH = 1.2 
STAR_GLOW_SIZE_MULTIPLIER = 2.5
STAR_GLOW_ALPHA = 40 


# FUNCTIONS
def rotate_vec(v: np.ndarray, axis: np.ndarray, angle: float) -> np.ndarray:
    """Rodrigues' rotation formula – now 100% NumPy safe"""
    axis = axis / np.linalg.norm(axis)
    c = math.cos(angle)
    s = math.sin(angle)
    dot = np.dot(v, axis)
    cross = np.cross(axis, v)
    return v * c + cross * s + axis * dot * (1 - c)

# Function to generate new glow particle properties
def generate_new_glow_particles(count):
    r = np.random.uniform(RS*2.8, RS*3.2, count)
    phi = np.random.uniform(0, 2*math.pi, count)
    h = np.random.normal(0, RS*0.08, count)

    x = r * np.cos(phi)
    z = r * np.sin(phi)
    new_pos = np.stack([x, h, z], axis=1)

    tang = np.stack([-np.sin(phi), np.zeros(count), np.cos(phi)], axis=1)
    rad  = np.stack([ np.cos(phi), np.zeros(count), np.sin(phi)], axis=1)
    
    sqrt_GM_r = np.sqrt(G * M / r)
    
    new_vel = tang * (sqrt_GM_r * 1.1).reshape(-1, 1) - rad * 0.08 
    
    return new_pos, new_vel


# ENGINE
class Engine:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.w, self.h = info.current_w, info.current_h
        # Initialize screen with per-pixel alpha (SRCALPHA) for glow effects
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN | pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('consolas', 18)
        self.center = np.array([self.w/2, self.h/2])

        self.cam_pos = np.array([0.0, 0.0, -200.0])
        self.focal = 85
        self.scale = 5

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.MOUSEWHEEL:
                dist = np.linalg.norm(self.cam_pos)
                dist = max(10, dist * (0.9 if e.y > 0 else 1.11))
                self.cam_pos = self.cam_pos / np.linalg.norm(self.cam_pos) * dist

    def look_at_matrix(self):
        forward = -self.cam_pos / np.linalg.norm(self.cam_pos)
        up = np.array([0.0, 1.0, 0.0])
        right = np.cross(forward, up)
        if np.linalg.norm(right) < 1e-6:
            up = np.array([0.0, 0.0, 1.0])
            right = np.cross(forward, up)
        right = right / np.linalg.norm(right)
        up = np.cross(forward, right)
        return np.stack([right, up, forward])

    # Optimized project method with Distortion
    def project(self, points: np.ndarray) -> np.ndarray:
        rot = self.look_at_matrix()
        rel = points - self.cam_pos                           # Relative position (N, 3)
        rot_rel = rel @ rot.T                                # Apply rotation (N, 3)

        z = rot_rel[:, 2]
        
        in_front = z > 0.1
        
        proj = np.full(rot_rel.shape, np.nan)
        
        if np.any(in_front):
            # 1. Base Perspective Projection
            z_in_front = z[in_front]
            div_factor = (self.focal / z_in_front * self.scale).reshape(-1, 1)
            
            # Base screen coordinates relative to center
            sx_rel = rot_rel[in_front, 0].reshape(-1, 1) * div_factor
            sy_rel = -rot_rel[in_front, 1].reshape(-1, 1) * div_factor
            
            # 2. Distortion/Stretching effect
            distortion = (DISTORTION_STRENGTH / np.maximum(z_in_front, 1.0)).reshape(-1, 1)
            
            # Apply distortion to the relative screen coordinates
            sx_rel_distorted = sx_rel * (1 + distortion)
            sy_rel_distorted = sy_rel * (1 + distortion)
            
            # Final Screen Coordinates
            sx = self.center[0] + sx_rel_distorted
            sy = self.center[1] + sy_rel_distorted
            
            proj[in_front, 0] = sx[:, 0]
            proj[in_front, 1] = sy[:, 0]
            proj[in_front, 2] = z_in_front

        return proj

    def flip(self):
        pygame.display.flip()
        self.screen.fill((0,0,0))
        self.clock.tick(60)


# PARTICLE INITIALISATION
eng = Engine()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# background stars
stars = np.random.uniform(-200, 200, (NUM_STARS, 3))
star_r = np.linalg.norm(stars, axis=1)
tang_vecs = np.cross(stars, [0,1,0]) 
tang_norms = np.linalg.norm(tang_vecs, axis=1)
non_zero_norm = tang_norms > 1e-6
tang_vecs[non_zero_norm] /= tang_norms[non_zero_norm].reshape(-1, 1)
star_vel = tang_vecs * (np.sqrt(G*M/star_r) * 0.3).reshape(-1, 1) 
star_vel[~non_zero_norm] = 0.0

# fast outer disk
disk_r = np.random.uniform(12, 90, NUM_DISK_PARTICLES)
disk_phi = np.random.uniform(0, 2*math.pi, NUM_DISK_PARTICLES)
disk_x = disk_r * np.cos(disk_phi)
disk_z = disk_r * np.sin(disk_phi)
disk = np.stack([disk_x, np.zeros(NUM_DISK_PARTICLES), disk_z], axis=1)
disk_tang = np.stack([-np.sin(disk_phi), np.zeros(NUM_DISK_PARTICLES), np.cos(disk_phi)], axis=1)
disk_vel = disk_tang * (np.sqrt(G*M/disk_r) * 1.0).reshape(-1, 1) 

# glowing photon-ring (razor-thin, slow spiral)
glow_r = np.random.uniform(RS*1.4, RS*3.2, NUM_GLOW_PARTICLES)
glow_phi = (np.arange(NUM_GLOW_PARTICLES) / NUM_GLOW_PARTICLES * 2*math.pi) + np.random.uniform(-0.02, 0.02, NUM_GLOW_PARTICLES)
glow_h = np.random.normal(0, RS*0.08, NUM_GLOW_PARTICLES)

glow_x = glow_r * np.cos(glow_phi)
glow_z = glow_r * np.sin(glow_phi)
glow = np.stack([glow_x, glow_h, glow_z], axis=1)

glow_tang = np.stack([-np.sin(glow_phi), np.zeros(NUM_GLOW_PARTICLES), np.cos(glow_phi)], axis=1)
glow_rad  = np.stack([ np.cos(glow_phi), np.zeros(NUM_GLOW_PARTICLES), np.sin(glow_phi)], axis=1)

sqrt_GM_r = np.sqrt(G * M / glow_r)
glow_vel = glow_tang * (sqrt_GM_r * 1.1).reshape(-1, 1) - glow_rad * 0.08   


# MAIN LOOP
while True:
    eng.handle_events()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
        break

    # ----- mouse orbit (locked on BH) -----
    mx, my = pygame.mouse.get_rel()
    if abs(mx)+abs(my) > 0:
        pos = eng.cam_pos.copy()
        pos = rotate_vec(pos, np.array([0.0,1.0,0.0]), -mx*0.003)
        forward = -pos / np.linalg.norm(pos)
        right = np.cross(forward, np.array([0.0,1.0,0.0]))
        if np.linalg.norm(right) > 1e-6:
            right /= np.linalg.norm(right)
            pos = rotate_vec(pos, right, my*0.003)
        eng.cam_pos = pos

    # physics (Vectorized)
    INFALL_PULL = INFALL_VELOCITY

    for particles, velocities in [(stars, star_vel), (disk, disk_vel)]:
        r_sq = np.sum(particles**2, axis=1)
        r = np.sqrt(r_sq)
        safe_zone = r > RS
        
        r_cube = r_sq * r
        r_cube[~safe_zone] = 1.0 
        
        acc_factor = (-G * M / r_cube).reshape(-1, 1) 
        acc = acc_factor * particles

        r_safe = r[safe_zone]
        particles_safe = particles[safe_zone]
        
        r_unit_safe = np.zeros_like(particles_safe)
        r_unit_safe = particles_safe / r_safe.reshape(-1, 1) 
        
        v_infall_safe = -r_unit_safe * INFALL_PULL
        
        velocities[safe_zone] += acc[safe_zone] * DT
        velocities[safe_zone] += v_infall_safe * DT 
        particles[safe_zone] += velocities[safe_zone] * DT

    # 2. GLOW RING
    p = glow
    r_xy = np.hypot(p[:, 0], p[:, 2])
    
    respawn_idx = r_xy < RS*1.2
    
    if np.any(respawn_idx):
        count = np.sum(respawn_idx)
        new_pos, new_vel = generate_new_glow_particles(count)
        
        glow[respawn_idx] = new_pos
        glow_vel[respawn_idx] = new_vel

    p = glow 
    r_xy = np.hypot(p[:, 0], p[:, 2]) 
    
    phi = np.arctan2(p[:, 2], p[:, 0])
    
    tang = np.stack([-np.sin(phi), np.zeros(NUM_GLOW_PARTICLES), np.cos(phi)], axis=1)
    rad  = np.stack([ np.cos(phi), np.zeros(NUM_GLOW_PARTICLES), np.sin(phi)], axis=1)
    
    sqrt_GM_r = np.sqrt(G * M / r_xy)
    
    glow_vel = tang * (sqrt_GM_r * 1.1).reshape(-1, 1) - rad * 0.08
    
    glow += glow_vel * DT

    # draw (Depth-Sorted with Glow)
    
    proj_stars = eng.project(stars)
    proj_disk = eng.project(disk)
    proj_glow = eng.project(glow)

    # List to hold all drawable objects for depth sorting
    drawable_objects = []

    # 1. Helper to package particles into drawable objects
    def package_particles(proj_points, source_points, color_func, type_id):
        valid_idx = ~np.isnan(proj_points[:, 0])
        
        if not np.any(valid_idx):
            return

        pts = proj_points[valid_idx]
        src = source_points[valid_idx]
        
        for pt, pos in zip(pts, src):
            sx, sy, z = pt
            color_core, size_core = color_func(pos, sx, sy)
            
            radius_glow = 0
            color_glow = (0, 0, 0, 0) # Fully transparent
            
            if type_id == 0: # Star
                radius_glow = int(size_core * STAR_GLOW_SIZE_MULTIPLIER)
                color_glow = color_core + (STAR_GLOW_ALPHA,) 
                
            elif type_id == 1: # Disk
                # No glow effect for disk particles to keep performance up and style consistent
                pass
                
            elif type_id == 2: # Glow Ring
                # Glow ring particles are already bright enough, treat them as core
                pass

            # Store as: (Z, type_id, sx, sy, radius_core, color_core, radius_glow, color_glow)
            drawable_objects.append((z, type_id, int(sx), int(sy), size_core, color_core, radius_glow, color_glow))

    # Color functions
    def star_color_func(pos, sx, sy):
        r = np.linalg.norm(pos)
        fade = max(0, 1 - (r - RS)/120)
        c = int(255 * (0.7 + 0.3*fade))
        return (c, c, 255), 2
    
    def disk_color_func(pos, sx, sy):
        r = np.linalg.norm(pos)
        intens = max(0, 1 - (r - RS*2)/80)
        col = (255, int(180*intens), 0)
        return col, 1

    def glow_color_func(pos, sx, sy):
        r = np.linalg.norm(pos)
        r_xy = math.hypot(pos[0], pos[2]) 
        bright = max(0, min(1, 1 - (r_xy - RS*1.2)/(RS*2)))
        col = (255, int(120 + 135*bright), int(60*bright))
        sz = 2 if bright > 0.7 else 1
        return col, sz

    # Package all particles
    package_particles(proj_stars, stars, star_color_func, 0)
    package_particles(proj_disk, disk, disk_color_func, 1)
    package_particles(proj_glow, glow, glow_color_func, 2)


    # 2. Black Hole (BH)
    bh = eng.project(np.zeros((1,3)))[0]
    if not np.isnan(bh[0]): 
        sx, sy, z = bh
        radius_core = max(RS * eng.focal / z * eng.scale, 12)
        radius_rim = int(radius_core + 4)
        
        # Glow Layer (Largest, dimmest circle)
        radius_bh_glow = int(radius_rim * 1.5)
        color_bh_glow = (255, 60, 0, 30) # Dim red/orange with low alpha
        drawable_objects.append((z, 3, int(sx), int(sy), 0, (0,0,0), radius_bh_glow, color_bh_glow))
        
        # Core Layers (Drawn after glow, closer Z)
        # Type 4: Black Hole Core and Rim. Handled as a special case in the drawing loop.
        drawable_objects.append((z, 4, int(sx), int(sy), int(radius_core), (0,0,0), radius_rim, (255,100,0)))

    # 3. Sort by Z-coordinate (Depth)
    drawable_objects.sort(key=lambda x: x[0], reverse=True)

    # 4. Final Drawing Loop (Correct Z-order and Glow layers)
    for z, type_id, sx, sy, radius_core, color_core, radius_glow, color_glow in drawable_objects:
        if type_id == 0: # Star
            # Draw glow layer first
            if radius_glow > 0:
                s = pygame.Surface((radius_glow * 2, radius_glow * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, color_glow, (radius_glow, radius_glow), radius_glow)
                eng.screen.blit(s, (sx - radius_glow, sy - radius_glow))
            # Draw core layer second
            pygame.draw.circle(eng.screen, color_core, (sx, sy), radius_core)
            
        elif type_id == 1 or type_id == 2: # Disk or Glow Ring (No secondary glow layer)
            pygame.draw.circle(eng.screen, color_core, (sx, sy), radius_core)
            
        elif type_id == 3: # Black Hole Glow Layer (Must be drawn first at this Z level)
            s = pygame.Surface((radius_glow * 2, radius_glow * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color_glow, (radius_glow, radius_glow), radius_glow)
            eng.screen.blit(s, (sx - radius_glow, sy - radius_glow))

        elif type_id == 4: # Black Hole Core and Rim (Drawn last at this Z level)
            radius_rim = radius_glow
            color_rim = color_glow
            pygame.draw.circle(eng.screen, color_core, (sx, sy), radius_rim)
            pygame.draw.circle(eng.screen, color_rim, (sx, sy), radius_rim, 4)
            pygame.draw.circle(eng.screen, color_core, (sx, sy), radius_core)
            
    # HUD (always drawn last)
    pygame.draw.circle(eng.screen, (255,255,255), eng.center.astype(int), 5, 1)
    txt = eng.font.render(f"Zoom {np.linalg.norm(eng.cam_pos):.0f} au  Glow {NUM_GLOW_PARTICLES}", True, (255,255,255))
    eng.screen.blit(txt, (12, 12))

    eng.flip()

pygame.quit()