# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 16:54:45 2020

Simple MC simulation of virus infections

@author: B.Menser
"""
import random 
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

color = ('','k','r','b')

healthStatus={'uninfected':1,'infected':2,'immune':3}
    
class statClass:
    
    def __init__(self,numInfected):
        self.numInfected=[numInfected]
        self.numImmune=[0]
        self.newInfected=[0]
        self.reproductionRate=[0]
        

    def update(self,word):
        
        # update statistics with last time step
        self.numInfected.append(np.count_nonzero(world.data==healthStatus['infected']))
        self.numImmune.append(np.count_nonzero(word.data==healthStatus['immune']))

        if world.t>0:
            newImmune = self.numImmune[-1]-self.numImmune[-2]
            deltaInfected = self.numInfected[-1]-self.numInfected[-2]
            self.newInfected.append(max(0,deltaInfected+newImmune))
        else:
           self.newInfected.append(0) 
      
    def update2(self,population):
        self.numInfected.append(sum(map(lambda person : person.status==healthStatus['infected'], population)))
        self.numImmune.append(sum(map(lambda person : person.status==healthStatus['immune'], population)))
        numInfectedPersons=[person.numInfectedPersons for person in population if person.status==healthStatus['immune'] and person.daysAfterInfection<3]
        if len(numInfectedPersons)>0:
            self.reproductionRate.append(mean(numInfectedPersons))
        else:
            self.reproductionRate.append(0)
       
        if world.t>0:
            newImmune = self.numImmune[-1]-self.numImmune[-2]
            deltaInfected = self.numInfected[-1]-self.numInfected[-2]
            self.newInfected.append(max(0,deltaInfected+newImmune))
        else:
           self.newInfected.append(0) 
           
    def print(self):
        print('\nnumInfected={}'.format(self.numInfected))
        print('numImmune  ={}'.format(self.numImmune))
        print('newInfected={}\n'.format(self.newInfected))

class worldClass:
   
    markerSize=2
    delay=0.01
    K=10         # for moving average
    
    
    
    def __init__(self, size,T,N):
        self.size=size
        self.data = np.zeros(size,dtype=np.uint8)
        
        self.fig=plt.figure('world',constrained_layout=True)
        
        # gs = self.fig.add_gridspec(3, 2)
        gs = self.fig.add_gridspec(2, 2)
        self.ax1 = self.fig.add_subplot(gs[:,0])
        # self.ax1.axis('square')
        self.ax1.set(xlim=(0,size[0]),ylim=(0,size[1]))
        # self.ax1.axis('equal','box')
        self.ax1.axis('equal')
        self.ax1.axis('equal')
        self.ax2=self.fig.add_subplot(gs[0,1])
        self.ax2.set_xlabel('time t')
        self.ax2.set_ylabel('persons')
        
        self.ax3=self.fig.add_subplot(gs[1,1])
        self.ax3.set_xlabel('time t')
        self.ax3.set_ylabel('delta persons')
        
        # self.ax4=self.fig.add_subplot(gs[2,1])
        # self.ax4.set_xlabel('time t')
        # self.ax4.set_ylabel('rate')
        
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        
         

        self.t=0   
        self.markerSize=5
            
        self.T=T
        self.N=N
        
        
    def checkValidPos(self,pos):
        (dimx,dimy) = self.size
        if pos[0]<0 or pos[1]<0 or pos[0]>dimx-1 or pos[1]>dimy-1:
            return False
        else:
            return True
        
    def checkFreePos(self,pos):
        if self.checkValidPos(pos) and  self.data[pos[0],pos[1]]==0:
            return True
        else:
            return False
        
    def set(self,pos,value):
        self.data[pos[0],pos[1]]=value
        
        
    def get(self,pos):
        return self.data[pos[0],pos[1]]
        
        
    def plot(self,stat):
        
        self.t+=1
        
        (x,y) = self.data.nonzero()
        self.ax1.cla()
        col=[color[i] for i in self.data[x,y]]
        self.ax1.scatter(x,y,s=worldClass.markerSize,c=col)   
        self.ax1.set(xlim=(0,self.size[0]),ylim=(0,self.size[1]))
       
        self.ax2.cla()
        h21, = self.ax2.plot(np.array(stat.numInfected)+np.array(stat.numImmune),color[1],label='total')
        h22, = self.ax2.plot(stat.numInfected,color[healthStatus['infected']],label='infected')
        h23, = self.ax2.plot(stat.numImmune,color[healthStatus['immune']],label='immune')
        # self.ax2.set_ylim((0,self.N))
        # self.ax2.set_xlim((0,self.T))
        
      
        self.ax2.set_yticklabels([y/self.N for y in self.ax2.get_yticks()])
        self.ax2.set_xlim((0,self.t+20))
        self.ax2.legend(handles=[h21,h22,h23],prop={'size': 6})
        self.ax2.axes.grid()

        self.ax3.cla()
        self.ax3.bar(np.arange(0,self.t),stat.newInfected,width=0.8,color=color[2],label='new infections')
        if self.t>self.K:
            newInfectionsAvg = np.convolve(np.array(stat.newInfected), np.ones((self.K,))/self.K, mode='valid')
            self.ax3.plot(np.arange(self.K-1,self.t),newInfectionsAvg,color=color[2],label='new infections (avg)')
        self.ax3.legend(prop={'size': 6})
         # self.ax3.set_xlim((0,self.T))
        self.ax3.set_xlim((0,self.t+20))
        self.ax3.axes.grid()
       
        # self.ax4.cla()
        # self.ax4.bar(np.arange(0,self.t),stat.reproductionRate,width=0.8,color=color[2],label='reproduction')
        # self.ax4.axhline(1.0,0,1)
        # self.ax4.legend(prop={'size': 6})
        #  # self.ax4.set_xlim((0,self.T))
        # self.ax4.set_xlim((0,self.t+20))
        # self.ax4.axes.grid()
        
        self.fig.suptitle('step {}: infected={} ({}%), immune={} ({}%), total={} ({}%)'.format(self.t,stat.numInfected[-1],100*stat.numInfected[-1]/self.N,stat.numImmune[-1],100*stat.numImmune[-1]/self.N,(stat.numImmune[-1]+stat.numInfected[-1]),100*(stat.numImmune[-1]+stat.numInfected[-1])/self.N), fontsize=12)
        plt.show()
        plt.draw()
        plt.pause(worldClass.delay)

        
  
     
class personClass:
 
    world=worldClass((100,100),10,1)
    
    infectionDist=10
    numInfectionSteps=30
      
    # Initializer / Instance Attributes
    def __init__(self, pos, status, ID,steps=3,stepsDelta=1):
        self.pos=pos
        self.status=status
        personClass.world.set(pos,status)
        self.daysInfected=0
        self.daysAfterInfection=0
        self.numInfectedPersons=0
        self.id=ID
        self.steps=steps
        self.stepsDelta=stepsDelta
        dx=random.randint(-self.steps,self.steps)
        dy=random.choice([-1,1])*(self.steps-abs(dx))
        self.speed = [dx,dy]
        
    def set(self,status=None,posNew=None):
        if status is not None:
            self.status=status
        if posNew is not None:
            personClass.world.set(self.pos,0)
            self.pos=posNew
        personClass.world.set(self.pos,self.status)
        
    def move(self,world):
        posNew = self.pos + self.speed
       
        delta = random.randint(-1,1)*self.stepsDelta
        dx = np.clip(self.speed[0]+delta, -self.steps, self.steps)
        deltaEffAbs=abs(dx)-abs(self.speed[0])  # >0 -> x-speed increases
        if self.speed[1]>0:
            dy=self.speed[1]-deltaEffAbs
        elif self.speed[1]<0:
            dy=self.speed[1]+deltaEffAbs
        else:
            dy=random.choice([-1,1])*abs(deltaEffAbs)
      
        # if self.id == 0:
        #     print('{} -> {}  deltaEffAbs={}'.format(self.speed[0],dx,deltaEffAbs))
        #     print('{} -> {}'.format(self.speed[1],dy))
            
        self.speed = [dx,dy]
        
        if personClass.world.checkFreePos(posNew):
            self.set(posNew = posNew)  
        else:
            self.speed[0]=-self.speed[0]
            self.speed[1]=-self.speed[1]
       
        # progress infection if present
        if self.status == healthStatus['infected']:
            if self.daysInfected == personClass.numInfectionSteps:
                self.set(status=healthStatus['immune'])    
            else:
                self.daysInfected+=1
        if self.status == healthStatus['immune']:
             self.daysAfterInfection+=1
             
    def infect(self,personList):
        distList=np.array([person.pos-self.pos for person in personList])
        inContact=np.all(abs(distList)<=personClass.infectionDist,axis=1)
        indexList = np.where(inContact)[0]
       
        for index in indexList:
            if self.id != personList[index].id:
                if personList[index].status == healthStatus['uninfected']:
                    personList[index].set(status=healthStatus['infected'])
                    self.numInfectedPersons+=1
        
    def print(self):
        print('\nID     : {}'.format(self.id))
        print('pos    : {}'.format(self.pos))
        print('speed  : {}'.format(self.speed))
        print('status : {}\n'.format(self.status))
        
        
        
    def config(world,infectionsDist=None,numInfectionSteps=None):
        personClass.world=world
        if numInfectionSteps is not None:
            personClass.numInfectionSteps=numInfectionSteps
        if infectionsDist is not None:
            personClass.infectionDist=infectionDist
            
        
if __name__ == "__main__":
    
    
    dim=(1200,1000)
    
    # motion
    steps=7
    stepsDelta=2
    
    # size of populaiton
    N=1000
    Ninfected = 3
    
    infectionDist=15        # spatial distance for infection
    numInfectionSteps=20    # duration of infections
    
    T=500
    
    #-----------------------
    
    plt.close('all')
    
    world = worldClass(dim,T,N)
    personClass.config(world,infectionDist,numInfectionSteps)
    
    stat = statClass(Ninfected)
    
    # init population
    population=list()
    n=0;
    while n<N:
        # randomw position
        pos_n = np.array([random.randint(0,dim[0]-1),random.randint(0,dim[1]-1)])
       
        if personClass.world.get(pos_n)==0:
            person = personClass(pos_n,healthStatus['uninfected'],n,steps,stepsDelta)
            population.append(person)
            n+=1
            
    # start with single infected person
    for n in range(Ninfected):
        population[n].set(status=healthStatus['infected'])

    
    for t in range(T):
       
        print('---- step {} ----'.format(t))

        world.plot(stat)
        for person in population:
            if person.id==0:
                person.print()        
                     
            person.move(world)
            
            if person.status is healthStatus['infected']:
                person.infect(population)
            
        # stat.update2(population)
        stat.update(world)
        # stat.print()

        # input("Press Enter to continue...")
        if stat.numInfected[-1]==0:
            break
        

    world.plot(stat)
       
        
       