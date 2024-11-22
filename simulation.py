import yaml, pygame, random, glob, math, numpy, pandas
from Lifter import Lifter
from objloader import *

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

textures = []
lifters = []
delta = 0


def GeneracionDeNodos():
	print("")


def loadSettingsYAML(File):
	class Settings:
		pass

	with open(File) as f:
		docs = yaml.load_all(f, Loader=yaml.FullLoader)
		for doc in docs:
			for k, v in doc.items():
				setattr(Settings, k, v)
	return Settings


Settings = loadSettingsYAML("Settings.yaml")


def Texturas(filepath):
	# Arreglo para el manejo de texturas
	global textures
	textures.append(glGenTextures(1))
	id = len(textures) - 1
	glBindTexture(GL_TEXTURE_2D, textures[id])
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	image = pygame.image.load(filepath).convert()
	w, h = image.get_rect().size
	image_data = pygame.image.tostring(image, "RGBA")
	glTexImage2D(
		GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data
	)
	glGenerateMipmap(GL_TEXTURE_2D)


def Init(Options):
	global textures, lifters, objetos
	screen = pygame.display.set_mode(
		(Settings.screen_width, Settings.screen_height), DOUBLEBUF | OPENGL
	)
	pygame.display.set_caption("Simulacion PontePizza")

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(
		Settings.FOVY,
		Settings.screen_width / Settings.screen_height,
		Settings.ZNEAR,
		Settings.ZFAR,
	)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(
		Settings.EYE_X,
		Settings.EYE_Y,
		Settings.EYE_Z,
		Settings.CENTER_X,
		Settings.CENTER_Y,
		Settings.CENTER_Z,
		Settings.UP_X,
		Settings.UP_Y,
		Settings.UP_Z,
	)
	glClearColor(0, 0, 0, 0)
	glEnable(GL_DEPTH_TEST)
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

	for File in glob.glob(Settings.Materials + "*.*"):
		Texturas(File)

	# Posiciones inicales de los montacargas
	Positions = numpy.zeros((Options.lifters, 3))

	NodosCarga = 10 * [[70, 0, 70]]

	CurrentNode = 0

	for i, p in enumerate(Positions):
		# i es el identificator del agente
		lifters.append(Lifter(Settings.DimBoard, 0.7, textures, i, p, CurrentNode))
	
	#Importantes para obj
	glEnable(GL_DEPTH_TEST)
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		
	#glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
	glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_COLOR_MATERIAL)
	glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded      
	objetos = []  
	objetos.append(OBJ("WarehouseShelving.obj", swapyz=True))
	objetos[0].generate()

def displayobj0():
	glPushMatrix()  
	#correcciones para dibujar el objeto en plano XZ
	#esto depende de cada objeto
	glRotatef(-90.0, 1.0, 0.0, 0.0)
	glTranslatef(-185, -60, 2)
	glScale(20,32,20)
	objetos[0].render()  
	glPopMatrix()

def displayobj1():
	glPushMatrix()  
	#correcciones para dibujar el objeto en plano XZ
	#esto depende de cada objeto
	glRotatef(-90.0, 1.0, 0.0, 0.0)
	glRotatef(-90.0, 0.0, 0.0, 1.0)
	glTranslatef(-180, 70, 2)
	glScale(20,32,20)
	objetos[0].render()  
	glPopMatrix()

def displayobj2():
	glPushMatrix()  
	#correcciones para dibujar el objeto en plano XZ
	#esto depende de cada objeto
	glRotatef(-90.0, 1.0, 0.0, 0.0)
	glTranslatef(170, -20, 2)
	glScale(20,32,20)
	objetos[0].render()  
	glPopMatrix()

def displayobj3():
	glPushMatrix()  
	#correcciones para dibujar el objeto en plano XZ
	#esto depende de cada objeto
	glRotatef(-90.0, 1.0, 0.0, 0.0)
	glRotatef(-90.0, 0.0, 0.0, 1.0)
	glTranslatef(-180, -70, 2)
	glScale(20,32,20)
	objetos[0].render()  
	glPopMatrix()

def planoText():
	# Enable textures
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, textures[5])  # Use the first texture

	glColor(1.0, 1.0, 1.0)

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3d(-Settings.DimBoard, 0, -Settings.DimBoard)

	glTexCoord2f(0.0, 1.0)
	glVertex3d(-Settings.DimBoard, 0, Settings.DimBoard)
	glTexCoord2f(1.0, 1.0)
	glVertex3d(Settings.DimBoard, 0, Settings.DimBoard)

	glTexCoord2f(1.0, 0.0)
	glVertex3d(Settings.DimBoard, 0, -Settings.DimBoard)
	glEnd()

	# Disable textures
	glDisable(GL_TEXTURE_2D)


def display():
	global lifters, delta
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	displayobj0()
	displayobj1()
	displayobj2()
	displayobj3()

	# Se dibuja cubos
	for obj in lifters:
		obj.draw()
		obj.update(delta)

	# Se dibuja el incinerador
	glColor3f(1.0, 0.5, 0.0)  # Color: Naranja
	square_size = 20.0  # Tamaño

	half_size = square_size / 2.0
	glBegin(GL_QUADS)
	glVertex3d(-half_size, 0.5, -half_size)
	glVertex3d(-half_size, 0.5, half_size)
	glVertex3d(half_size, 0.5, half_size)
	glVertex3d(half_size, 0.5, -half_size)
	glEnd()

	# Se dibuja el plano gris
	planoText()
	drawColumn()
	drawColumn2()
	drawColumn3()
	drawColumn4()
	drawColumn5()
	drawRefri()

	glColor3f(0.3, 0.3, 0.3)
	glBegin(GL_QUADS)
	glVertex3d(-Settings.DimBoard, 0, -Settings.DimBoard)
	glVertex3d(-Settings.DimBoard, 0, Settings.DimBoard)
	glVertex3d(Settings.DimBoard, 0, Settings.DimBoard)
	glVertex3d(Settings.DimBoard, 0, -Settings.DimBoard)
	glEnd()

	# Draw the walls bounding the plane
	wall_height = 50.0  # Adjust the wall height as needed

	glColor3f(0.8, 0.8, 0.8)  # Light gray color for walls

	glEnable(GL_TEXTURE_2D)

	# Draw the left wall with texture
	glBindTexture(
		GL_TEXTURE_2D, textures[3]
	)  # Replace 4 with your texture index for walls
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3d(-Settings.DimBoard, 0, -Settings.DimBoard)
	glTexCoord2f(1.0, 0.0)
	glVertex3d(-Settings.DimBoard, 0, Settings.DimBoard)
	glTexCoord2f(1.0, 1.0)
	glVertex3d(-Settings.DimBoard, wall_height, Settings.DimBoard)
	glTexCoord2f(0.0, 1.0)
	glVertex3d(-Settings.DimBoard, wall_height, -Settings.DimBoard)
	glEnd()

	# Draw the right wall with texture
	glBindTexture(GL_TEXTURE_2D, textures[3])  # Use the same or a different texture
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3d(Settings.DimBoard, 0, -Settings.DimBoard)
	glTexCoord2f(1.0, 0.0)
	glVertex3d(Settings.DimBoard, 0, Settings.DimBoard)
	glTexCoord2f(1.0, 1.0)
	glVertex3d(Settings.DimBoard, wall_height, Settings.DimBoard)
	glTexCoord2f(0.0, 1.0)
	glVertex3d(Settings.DimBoard, wall_height, -Settings.DimBoard)
	glEnd()

	# Draw the front wall with texture
	glBindTexture(GL_TEXTURE_2D, textures[3])
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3d(-Settings.DimBoard, 0, Settings.DimBoard)
	glTexCoord2f(1.0, 0.0)
	glVertex3d(Settings.DimBoard, 0, Settings.DimBoard)
	glTexCoord2f(1.0, 1.0)
	glVertex3d(Settings.DimBoard, wall_height, Settings.DimBoard)
	glTexCoord2f(0.0, 1.0)
	glVertex3d(-Settings.DimBoard, wall_height, Settings.DimBoard)
	glEnd()

	# Draw the back wall with texture
	glBindTexture(GL_TEXTURE_2D, textures[3])
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3d(-Settings.DimBoard, 0, -Settings.DimBoard)
	glTexCoord2f(1.0, 0.0)
	glVertex3d(Settings.DimBoard, 0, -Settings.DimBoard)
	glTexCoord2f(1.0, 1.0)
	glVertex3d(Settings.DimBoard, wall_height, -Settings.DimBoard)
	glTexCoord2f(0.0, 1.0)
	glVertex3d(-Settings.DimBoard, wall_height, -Settings.DimBoard)
	glEnd()

	# Disable textures after drawing walls
	glDisable(GL_TEXTURE_2D)


def drawColumn():
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, textures[1])  # Use appropriate texture index

	width = 30.0
	depth = 30.0
	height = 70.0

	glPushMatrix()
	glTranslatef(0.0, 0.0, 0.0)  # Center of the plane

	# Front face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Back face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Left face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Right face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glEnd()

	# Top face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Bottom face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glEnd()

	glPopMatrix()
	glDisable(GL_TEXTURE_2D)


def drawColumn2():

	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, textures[1])  # Use appropriate texture index

	width = 30.0
	depth = 30.0
	height = 70.0

	glPushMatrix()
	glTranslatef(0.0, 0.0, -200 + depth / 2)  # Center of the plane

	# Front face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Back face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Left face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Right face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glEnd()

	# Top face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Bottom face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glEnd()

	glPopMatrix()
	glDisable(GL_TEXTURE_2D)


def drawColumn3():
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, textures[1])  # Use appropriate texture index

	width = 70.0
	depth = 15.0
	height = 50.0

	glPushMatrix()
	glTranslatef(-200 + width / 2, 0.0, -25)  # Center of the plane

	# Front face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Back face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Left face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Right face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glEnd()

	# Top face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Bottom face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glEnd()

	glPopMatrix()
	glDisable(GL_TEXTURE_2D)


def drawColumn4():
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, textures[1])  # Use appropriate texture index

	width = 15.0
	depth = 70.0
	height = 50.0

	glPushMatrix()
	glTranslatef(-200 + depth , 0, -52)  # Center of the plane

	# Front face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Back face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Left face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Right face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glEnd()

	# Top face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Bottom face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glEnd()

	glPopMatrix()
	glDisable(GL_TEXTURE_2D)

#borde larga
def drawColumn5():
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, textures[1])  # Use appropriate texture index

	width = 10.0
	depth = 140.0
	height = 50.0

	glPushMatrix()
	glTranslatef(200-width , 0, 20)  # Center of the plane

	# Front face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Back face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Left face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Right face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glEnd()

	# Top face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Bottom face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glEnd()

	glPopMatrix()
	glDisable(GL_TEXTURE_2D)

def drawRefri():
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, textures[-1])  # Use appropriate texture index

	width = 70.0
	depth = 70.0
	height = 50.0

	glPushMatrix()
	glTranslatef(-200+depth/2 , 0, 200-width/2)  # Center of the plane

	# Front face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Back face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Left face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glEnd()

	# Right face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(width / 2, height, -depth / 2)
	glEnd()

	# Top face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, height, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, height, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, height, depth / 2)
	glEnd()

	# Bottom face
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(width / 2, 0.0, -depth / 2)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(width / 2, 0.0, depth / 2)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-width / 2, 0.0, depth / 2)
	glEnd()

	glPopMatrix()
	glDisable(GL_TEXTURE_2D)



def lookAt(theta):
	glLoadIdentity()
	rad = theta * math.pi / 180
	newX = Settings.EYE_X * math.cos(rad) + Settings.EYE_Z * math.sin(rad)
	newZ = -Settings.EYE_X * math.sin(rad) + Settings.EYE_Z * math.cos(rad)
	gluLookAt(
		newX,
		Settings.EYE_Y,
		newZ,
		Settings.CENTER_X,
		Settings.CENTER_Y,
		Settings.CENTER_Z,
		Settings.UP_X,
		Settings.UP_Y,
		Settings.UP_Z,
	)


def Simulacion(Options):
	# Variables para el control del observador
	global delta
	theta = Options.theta
	radius = Options.radious
	delta = Options.Delta
	Init(Options)
	while True:
		keys = pygame.key.get_pressed()  # Checking pressed keys
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
					pygame.quit()
					return
		if keys[pygame.K_RIGHT]:
			if theta > 359.0:
				theta = 0
			else:
				theta += 1.0
		lookAt(theta)
		if keys[pygame.K_LEFT]:
			if theta < 1.0:
				theta = 360.0
			else:
				theta -= 1.0
		lookAt(theta)
		display()
		display()
		pygame.display.flip()
		pygame.time.wait(10)

	#
