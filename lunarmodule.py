from __future__ import division
from vpython import *


# Construindo o cenário
scene.width = 600
scene.height = 400
scene.range = 75
scene.center = vector(0, 10, 0)
scene.autoscale = False 
scene.userzoom = False
scene.userspin = False 
scene.ambient=color.gray(0.5)
offset = 0
print("Press left and right arrow keys to rotate.\nHold up arrow to apply thrust")

N_stars = 200
star = [] 
for i in range(N_stars):
  # Numeros aleatorios
  # Criando um campo de estrelas
  # varios valores foram testados para tentar parecer mais bonito
  star.append(sphere(radius = 0.25 + 0.75 * random()))
  star[i].color = vector(0.85, 0.85, 0.85) + 0.15 * vector(random(), 0, random())
  star[i].pos.z = -250 + 100 * random()
  star[i].pos.x = 6 * scene.range * (random() - 0.5)
  star[i].pos.y = 20 + 6 * scene.range * (random() - 0.5)

# Criando as zonas de pouso e as montanhas "cortadas" embaixo
pad = []   # cilindro
L = []   # tamanho(s) da(s) montanha(s) (tamanho do cone cortado)
R1 = []  # pequenos raios dos cones cortados 
R2 = []  # grandes raio dos cones cortados
s = []   # formas para formarem o cone cortado
c = []   # cones 

N_pads = 15

for i in range(N_pads):
  pad.append(cylinder(radius = 3 + 4 * random()))
  pad[i].axis = vector(0,1,0)
  pad[i].pos.z = 0
  pad[i].pos.y = -50 + 50 * random()
  pad[i].pos.x = -scene.range + i * ((1 + 2 * random())*scene.range/N_pads)  
  # Fazendo a montanha
  L.append(50 - (pad[i].pos.y))
  R1.append(15 + 100*random())
  R2.append(pad[i].radius)
  s.append([ [-R1[i]/2,0], [R1[i]/2,0], [-R1[i]/2+R2[i],L[i]], [-R1[i]/2,L[i]], [-R1[i]/2,0] ])
  c.append(extrusion(path=paths.circle(radius=R1[i]/2), shape=s[i]))
  c[i].pos = vector(pad[i].pos.x, pad[i].pos.y - L[i]/2 + pad[i].axis.y, 0)
  c[i].texture = textures.rough
  c[i].bumpmap = bumpmaps.stucco

# Construindo o módulo lunar

capsule = cylinder(axis = vector(0,3,0), radius = 2.0)
# Parametros do VPython
capsule.pos = vector(-50 + 10*random(), 40 + 10*random(), 0)
capsule.texture = textures.metal
# Meus proprios parametros
capsule.mass = 2000   # kg 
capsule.thrust = 0 
capsule.maxthrust = 5000
capsule.thrustincrement = 500
capsule.angle = 0.0 
capsule.rotangle = 0.2
capsule.vel = vector(6 + 2 * random(), 0, 0) 
capsule.fuel = 100 

leg1 = cylinder(axis = vector(-2,-4,0), radius = 0.25)
leg2 = cylinder(axis = vector(2,-4,0), radius = 0.25 )
leg1.pos = capsule.pos + 0.25 * capsule.axis
leg2.pos = capsule.pos + 0.25 * capsule.axis
legs = compound([leg1, leg2])
legs.texture = textures.metal

flame = cone(axis = vector(0,-25,0), radius = 1.5, color = color.red)
flame.texture = textures.wood_old

def process(event):
  if running == False: return 
  if (event.which == 37):   # esquerda
    capsule.rotate(axis = vector(0,0,1), angle = capsule.rotangle)
    legs.rotate(axis = vector(0,0,1), angle = capsule.rotangle)
    capsule.angle = capsule.angle + capsule.rotangle
  if (event.which == 39):   # direita
    capsule.rotate(axis = vector(0,0,1), angle = -capsule.rotangle)
    legs.rotate(axis = vector(0,0,1), angle = -capsule.rotangle)
    capsule.angle = capsule.angle - capsule.rotangle
  if (event.which == 38):   # cima
    # Tamanho da chama é 1 m por 1000 "impulsos"(thrust)
    capsule.thrust = capsule.thrust + capsule.thrustincrement
    if (capsule.fuel < 0):
      capsule.thrust = 0.0
      capsule.fuel = 0.0
    if (capsule.thrust > capsule.maxthrust):
      capsule.thrust = capsule.maxthrust

def letgo(event):
  if (event.which == 38):
    capsule.thrust = 0


# Processando as ações do teclado
scene.bind('click keydown', process)
scene.bind('click keyup', letgo)

# Area de dados para o canto direito superior
data = label(box = False, text = '', visible = True, height = 11, pixel_pos = True, align = 'left')
data.pos = vector(scene.width - 150,scene.height - 20,0)

# Area de debug para o canto esquero superior
debug = label(box = False, text = '', visible = False, height = 11, pixel_pos = True, align = 'left')
debug.pos = vector(50 ,scene.height - 50,0)

# Area de anuncios
announce = label(box = False, text = '', visible = False, height = 30, pixel_pos = True, align ='center', opacity = 0.0 )
announce.pos = vector(scene.width/2, 125 + scene.height/2, 0)

# Fisica
g = 0.8   # N/kg
dt = 0.001
running = True 

# Loop da animação
while(running):

  rate(1/dt)
  
  # Forcas do modulo
  force = vector(0, -capsule.mass * g, 0) 
  force = force + capsule.axis.norm() * capsule.thrust 
  
  # Removendo combustivel
  capsule.fuel = capsule.fuel - capsule.thrust * dt / 1000
  if (capsule.fuel < 20):
    announce.color = color.red
    announce.visible = True 
    announce.text = "Low on fuel!"
  
  # Atualizar o estado do modulo 
  capsule.vel = capsule.vel + (force / capsule.mass) * dt
  capsule.pos = capsule.pos + capsule.vel * dt
  flame.pos = capsule.pos + 0.25 * capsule.axis
  legs.pos = capsule.pos + 0.25 * capsule.axis
  
  # Tentativa de adicionar efeito ao fogo
  flame.axis = - capsule.axis.norm() * (25 * capsule.thrust / capsule.maxthrust) 
  #flame.axis = flame.axis + 0.3 * random() * flame.axis + 0.02 * flame.axis.mag * vectortor.random()
  flame.opacity = 0.5 + 0.25*random()
  flame.color = vector(0.5 + 0.5 * random(), 0.35*random(), 0.35*random())
    
  # Checando por montanhas e contato com areas de pouso
  zoom = False   # Zoom in se perto de uma montanha ou zona de pouso 
  for i in range(len(pad)):

    # Checar para ver se esta perto a uma montanha - tratar todas como uma linha inclinada
    
    # Paredes à esquerda
    m = L[i] / (R1[i] - R2[i])   # Declive da parede 
    b = pad[i].pos.y - m * (pad[i].pos.x - pad[i].radius)   # Deslocamento da parede
    if ((capsule.pos.y < (m * capsule.pos.x + b)) # Se estiver embaixo da parede
      and (capsule.pos.x < pad[i].pos.x - pad[i].radius) # Se estiver a esquerda da zona de pouso
      and (capsule.pos.y - (pad[i].pos.y + pad[i].axis.y) < 0.0)):  # Se estiver embaixo da zona de pouso
        running = False 
        flame.axis = vector(0,0,0)
        announce.color = color.red
        announce.visible = True 
        announce.text = "Crash landing!"
    
    # Paredes à direita
    m = - m
    b = pad[i].pos.y - m * (pad[i].pos.x + pad[i].radius)   # Deslocamento da parede
    if ((capsule.pos.y < (m * capsule.pos.x + b)) # Se estiver embaixo da parede
      and (capsule.pos.x > pad[i].pos.x - pad[i].radius)  # Se estiver a esquerda da zona de pouso
      and (capsule.pos.y - (pad[i].pos.y + pad[i].axis.y) < 0.0)):   # Se estiver embaixo da zona de pouso
        running = False 
        flame.axis = vector(0,0,0)
        announce.color = color.red
        announce.visible = True 
        announce.text = "Crash landing!"
 
    # Checar se está perto de uma zona de pouso
    horsep = abs(capsule.pos.x - pad[i].pos.x)  # Separação horizontal entre o módulo e a zona
    versep = capsule.pos.y - 1 - (pad[i].pos.y + pad[i].axis.y)   # Separação vertical entre o módulo e a zona
    # Devemos aumentar o zoom?
    if (horsep < 3 * pad[i].radius and versep < 4 * pad[i].radius and versep > 0):
      zoom = True
      scene.center = pad[i].pos + vector(0, pad[i].radius, 0)
      offset = pad[i].pos.y + pad[i].axis.y
      scene.range = 3 * pad[i].radius 
    
    # Estamos tentando pousar?
    if ((horsep < 0.85 * pad[i].radius) and (abs(versep) < 0.1 * capsule.axis.mag)): 
      running = False 
      flame.axis = vector(0,0,0)
      if (abs(capsule.vel.x) < 1.0 and abs(capsule.vel.y) < 1.5 and capsule.angle < capsule.rotangle):
        announce.text = "Safe landing!"
        announce.color = color.cyan
        announce.visible = True 
      else:
        announce.color = color.red
        announce.visible = True 
        announce.text = "Crash landing!"
        if (capsule.angle > capsule.rotangle):
          announce.text += "\nRotation angle too high!"
        if (abs(capsule.vel.x) >= 1.0): 
          announce.text += "\nHorizontal speed too high!"
        if (abs(capsule.vel.y) >= 1.5): 
          announce.text += "\nVertical speed too high!"
  
  # Resetar o zoom se não tivermos dado zoom in em nenhuma zona de pouso
  if (zoom == False):
    scene.range = 75
    scene.center = vector(0, 10, 0)
    offset = -50
    
  # Atualizando a área de dados
  data.text = 'Altitude: ' + str((round(10*(capsule.pos.y - 1 - offset))/10)) + " m"
  data.text += '\nHorizontal velocity: ' + str(round(10*capsule.vel.x)/10) + " m/s"
  data.text += '\nVertical velocity: ' + str(round(10*capsule.vel.y)/10) + " m/s"
  data.text += '\nOrientation: ' + str(round(-10*capsule.angle * 5.625 % 360)) + " deg"
  data.text += "\nFuel: " + str(round(10*capsule.fuel)/10) + " units"
