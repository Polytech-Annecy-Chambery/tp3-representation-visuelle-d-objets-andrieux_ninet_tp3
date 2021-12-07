# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul
"""
import OpenGL.GL as gl

class Section:
    # Constructor
    def __init__(self, parameters = {}) :  
        # Parameters
        # position: position of the wall 
        # width: width of the wall - mandatory
        # height: height of the wall - mandatory
        # thickness: thickness of the wall
        # color: color of the wall        

        # Sets the parameters
        self.parameters = parameters
        
        # Sets the default parameters
        if 'position' not in self.parameters:
            self.parameters['position'] = [0, 0, 0]        
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')   
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')   
        if 'orientation' not in self.parameters:
            self.parameters['orientation'] = 0              
        if 'thickness' not in self.parameters:
            self.parameters['thickness'] = 0.2    
        if 'color' not in self.parameters:
            self.parameters['color'] = [0.5, 0.5, 0.5]       
        if 'edges' not in self.parameters:
            self.parameters['edges'] = True            
            
        # Objects list
        self.objects = []

        # Generates the wall from parameters
        self.generate()   
        
    # Getter
    def getParameter(self, parameterKey):
        return self.parameters[parameterKey]
    
    # Setter
    def setParameter(self, parameterKey, parameterValue):
        self.parameters[parameterKey] = parameterValue
        return self     

    # Defines the vertices and faces 
    def generate(self):
        self.vertices = [ 
                [0, 0, 0 ], 
                [0, 0, self.parameters['height']], 
                [self.parameters['width'], 0, self.parameters['height']],
                [self.parameters['width'], 0, 0],      
                [0, self.parameters['thickness'], 0], 
                [0, self.parameters['thickness'], self.parameters['height']], 
                [self.parameters['width'], self.parameters['thickness'], self.parameters['height']],
                [self.parameters['width'], self.parameters['thickness'], 0]
                ]
        self.faces = [
                [0, 3, 2, 1],
                [5, 6, 7, 4],                
                [1, 0, 4, 5],               
                [4, 0, 3, 7],
                [7, 3, 2, 6],
                [6, 2, 1, 5]
                ]   


    # Checks if the opening can be crated for the object x
    def canCreateOpening(self, x):
        # A compléter en remplaçant pass par votre code
        '''
        for i in range (0,len(x.vertices)):
            if x.vertices[i][0] >= self.vertices[0][0] and x.vertices[i][0] <= self.vertices[3][0]:
                if x.vertices[i][1] >= self.vertices[0][1] and x.vertices[i][1] <= self.vertices[4][1]:
                    if x.vertices[i][2] >= self.vertices[0][2] and x.vertices[i][2] <= self.vertices[1][2]:
                        print(i)
                    else:
                       return False
                else:
                   return False
            else:
                return False
        return True
    '''
    
        pos_s = self.parameters['position']
        height_s = self.parameters['height']
        width_s = self.parameters['width']
        thickness_s = self.parameters['thickness']
        
        pos_x = x.parameters['position']
        height_x = x.parameters['height']
        width_x = x.parameters['width']
        thickness_x = x.parameters['thickness']
        
        cond = pos_x[0] >= pos_s[0] and pos_x[0]<=pos_s[0]+width_s
        cond = cond and ( pos_x[1]>=pos_s[1] and pos_x[1]<=pos_s[1]+thickness_s)
        cond = cond and ( pos_x[2]>=pos_s[2] and pos_x[2]<=pos_s[2]+height_s)  
        cond = cond and ( pos_x[0]+width_x >= pos_s[0] and pos_x[0]+width_x <=pos_s[0]+width_s)
        cond = cond and ( pos_x[1]+thickness_x >=pos_s[1] and pos_x[1]+thickness_x <=pos_s[1]+thickness_s)  
        cond = cond and ( pos_x[2]+height_x >=pos_s[2] and pos_x[2]+height_x <=pos_s[2]+height_s)  
        return cond
            
    # Creates the new sections for the object x
    def createNewSections(self, x):
        # A compléter en remplaçant pass par votre code
        if self.canCreateOpening(x) == True:
            section1 = Section({'position':self.parameters['position'], 
                     'width':x.parameters['position'][0],
                     'height':self.parameters['height'],
                     'thickness': self.parameters['thickness']})
            
            section2 = Section({'position':[x.parameters['position'][0],x.parameters['position'][1],x.parameters['position'][2]+x.parameters['height']],
                     'width':x.parameters['width'],
                     'height':self.parameters['height']-x.parameters['position'][2]-x.parameters['height'],
                     'thickness': self.parameters['thickness']})
            
            section3 = Section({'position':[x.parameters['position'][0],self.parameters['position'][1],self.parameters['position'][2]],
                     'width':x.parameters['width'],
                     'height':x.parameters['position'][2],
                     'thickness': x.parameters['thickness']})
            
            section4 = Section({'position':[x.parameters['position'][0]+x.parameters['width'],x.parameters['position'][1],self.parameters['position'][2]],
                     'width':self.parameters['width']-x.parameters['position'][0]-x.parameters['width'],
                     'height':self.parameters['height'],
                     'thickness': x.parameters['thickness']})
            
            return [section1,section2,section3,section4]
        
    # Draws the edges
    def drawEdges(self):
        # A compléter en remplaçant pass par votre code
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE) 
        gl.glBegin(gl.GL_QUADS)
        gl.glColor3fv([self.parameters['color'][0]/2, 
                       self.parameters['color'][1]/2, 
                       self.parameters['color'][2]/2])
        for face in self.faces:
            for vertex in face:
                gl.glVertex3fv(self.vertices[vertex])  
        gl.glEnd()  
        
                    
    # Draws the faces
    def draw(self):
        
        
        # A compléter en remplaçant pass par votre code
        
        gl.glPushMatrix()
        gl.glTranslatef(self.parameters['position'][0],
                        self.parameters['position'][1],
                        self.parameters['position'][2])
        
        if self.parameters['edges'] == True:
            self.drawEdges()
            
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL) 
        gl.glBegin(gl.GL_QUADS)
        gl.glColor3fv(self.parameters['color'])
        for face in self.faces:
            for vertex in face:
                gl.glVertex3fv(self.vertices[vertex])  
        gl.glEnd()  
        gl.glPopMatrix() 
        
        
  
