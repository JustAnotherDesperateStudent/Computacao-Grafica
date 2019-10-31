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
capsule.thrust = 0 
capsule.maxthrust = 5000
capsule.thrustincrement = 500
capsule.angle = 0.0 
capsule.rotangle = 0.2

leg1 = cylinder(axis = vector(-2,-4,0), radius = 0.25)
leg2 = cylinder(axis = vector(2,-4,0), radius = 0.25 )
leg1.pos = capsule.pos + 0.25 * capsule.axis
leg2.pos = capsule.pos + 0.25 * capsule.axis
legs = compound([leg1, leg2])
legs.texture = textures.metal

flame = cone(axis = vector(0,-25,0), radius = 1.5, color = color.red)
flame.texture = textures.wood_old

dt = 0.001
running = True 
# Loop da animação
while(running):

  rate(1/dt)
  
  # Atualizar o estado do modulo 
  flame.pos = capsule.pos + 0.25 * capsule.axis
  legs.pos = capsule.pos + 0.25 * capsule.axis
    
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
        announce.text = "O modulo foi destruido!"
    
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
        announce.text = "O modulo foi destruido!"
