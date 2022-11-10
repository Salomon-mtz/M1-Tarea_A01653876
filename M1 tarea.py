import mesa
import random

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

class Agentemalo(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cantidad = True
        self.wealth = 1
        
    def step(self):
        contador = 0;
        contador += 1

class AgenteBueno(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore = True, include_center = False
        )
        new_pos = self.random.choice(possible_steps)
        self.model.grid.move_agent(self,new_pos)
        
        
    def step(self):
        self.move()
        
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for i in cell:
            if type(i) == Agentemalo and i.cantidad == True:
                self.model.grid.remove_agent(i)
                self.wealth += 1
                
class Modelo(mesa.Model):
    def __init__(self, N, T):
        self.num = N
        self.num2 = T
        self.grid = mesa.space.MultiGrid(10,10,False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        for i in range(self.num):
            agenteBueno = AgenteBueno(i, self)
            self.schedule.add(agenteBueno)
            self.grid.place_agent(agenteBueno,(1,1))
        
        for i in range(self.num2):
            basura = Agentemalo(self.num+i, self)
            self.schedule.add(basura)
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            self.grid.place_agent(basura,(x,y))
    
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        )
        
            
            
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        
        
def agent_port(agent):
    
    portrayal={
        "Shape":"circle",
        "Filled":"true",
        "Layer": "Aspiradora",
        "Color":"red",
        "r":0.5,
    }
    
    if type(agent) == Agentemalo:
        
        portrayal["Color"] = "blue"
    else:
        portrayal["Color"] = "green"
        
    if type(agent) == Agentemalo and agent.cantidad != True:
        portrayal["Color"] = "red"


    return portrayal

grid = mesa.visualization.CanvasGrid(agent_port, 10,10,500,500)
chart = mesa.visualization.ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
server = mesa.visualization.ModularServer(
    Modelo, [grid, chart], "Aspiradora",{"N":5, "T": 10}
)

server.port = 8522

server.launch()