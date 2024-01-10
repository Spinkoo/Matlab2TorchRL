import matlab.engine
import numpy as np
import time


#to add in the assertion params
#set_param(bdroot,'SimulationCommand','pause'), disp(sprintf('\nSimulation paused.'))
#Simulation path



#a second
STEP_SIZE = 1


#Matlab wrapper
class Engine:
    def __init__(self, model_path : str, sim_path : str, model_name = 'Trolley', matlab_stepper:str = 'step_time', simulation_type ='sbs') -> None:

        self.model_path = model_path
        self.model_name = model_name
        self.step_counter = 1
        self.matlab_stepper = matlab_stepper
        self.sim_path = sim_path
        self.sim_type = simulation_type
        self.step_fn = self.init_steps_dict()
    
    # Initialize the dictionary of step functions
    def init_steps_dict(self) -> dict:
        return {'sbs' : self.step_by_step, 'sparsesbs' : self.sparsesbs, 'normal' : self.f}
    
    # Step by step simulation
    def step_by_step(self):
        self.set_param(f'{self.model_name}/{self.matlab_stepper}', str(9999))
        self.start_pause_simulation()

    # Sparse Step by step simulation, the idea is to skip certain number of steps if they are superfluous 

    def sparsesbs(self):
        self.timestep_forward()
    
    # Run a .m file on matlab
    def run_engine_script(self, script_name : str):
        f = getattr(self.eng, script_name)
        f(nargout = 0)
    def f(self):
        pass
    

    def step_forward(self):
        self.step_fn[self.sim_type]()

    #Access a folder
    def cd_folder(self, path):
        self.eng.cd(f'{path}', nargout = 0)

    # Load the Python-Matlab engine
    def load_engine(self) -> None:

        self.eng = matlab.engine.start_matlab()
        self.cd_folder(self.sim_path)
        

        #Load initalization script, for example after accessing the simulation path that contains your Init_Calcul_Coef.m script you can run it this way
        #self.eng.Init_Calcul_Coef(nargout = 0)
        self.model = self.eng.load_system(self.model_path)

    def set_simulation_mode(self, s_mode : str = 'accelerator') -> None:
        self.eng.set_param(self.model, 'SimulationMode', s_mode, nargout = 0)
    
    # Set maximum steps for the simulation, sort of timeout
    def set_max_steps(self, max_iter : int, max_iter_block = 'max_sim_time') -> None:
        self.set_param(f'{max_iter_block}', str(max_iter), )

    """An assertion block needs to be created in order to properly pause the simulation on Matlab each N steps (check simulink model)"""
    def set_step_size(self, step_sz):

        assert self.sim_type == 'sparsesbs', 'Simulation type has to be set to step by step (sbs), an assertion block should set inplace inside the simulation'
        self.step_size = step_sz
        self.set_param(f'{self.matlab_stepper}', str(step_sz), )
    
    def forward_sim(self) -> None:
        self.step_counter +=1
        current_time = self.step_counter * self.step_size
        t = f'{current_time:.1f}'
         
        self.set_param(f'{self.matlab_stepper}', t)

    def start_simulation(self) -> None:
        self.eng.set_param(self.model_name, 'SimulationCommand', 'start', nargout = 0)

    #One step forward -this moves according to the simulation timestep-
    def start_pause_simulation(self) -> None:
        self.step_counter = 1
        #self.eng.set_param(self.model_name, 'SimulationCommand', 'pause', nargout = 0)
        self.eng.set_param(self.model_name, 'SimulationCommand', 'start', 'SimulationCommand', 'pause', nargout = 0)

    def timestep_forward(self) -> None:
        self.forward_sim()
        self.eng.set_param(self.model_name, 'SimulationCommand', 'continue', nargout = 0)

    def end_simulation(self) -> None:
        self.eng.quit()
    
    def stop_simulation(self) -> None:
        
        self.eng.set_param(self.model_name, 'SimulationCommand', 'stop', nargout = 0)

    def update_simulation(self) -> None:
        self.eng.set_param(self.model_name, 'SimulationCommand', 'update', nargout = 0)
    
    def pause_simulation(self) -> None:
        self.eng.set_param(self.model_name, 'SimulationCommand', 'pause', nargout = 0)

    def get_param(self, block_path, param_name):
        return self.eng.get_param(f'{self.model_name}{block_path}', param_name)

    #This requires a Display / Calculation block on the Simuliation side, basically any block that has input and output ports
    def get_runtime_attribute(self, attribute : str, block_path : str, inport = True, port = 1, param_name = 'RuntimeObject'):
        try:
            br = self.get_param(f'{block_path}/{attribute}', param_name)
            #time.sleep(.01)
            self.eng.workspace['br'] = br
            return self.eng.eval(f"br.{'InputPort' if inport else 'OutpotPort'}({port}).data") # Access displayed  data
        except Exception as e:
            print(e)
            self.stop_simulation()  
            return -1
    
    # Get simulation output

    def get_simout(self, ws = 'base'):
        return self.get_simulation_last_readings('simout', ws)
    
    # Get simulation status
    def get_simulation_status(self) -> str:
        return self.get_param("", 'SimulationStatus')
    
    # Get robot sensors readings
    def get_robots_readings(self, ws = 'base'):
        return np.array(self.get_simulation_last_readings('robot_readings', ws)[0], dtype=np.float16)
    
    def get_simulation_last_readings(self, att, ws = 'base'):
        br = self.eng.evalin(ws, att)
        self.eng.workspace['br'] = br
        return self.eng.eval(f"br.data")
    
    # Get workspace parameter
    def get_ws_value(self, attribute = 'Vitesse', ws = 'base'):
        return self.eng.evalin(ws, attribute)
    
    # Write to workspace
    def write_ws_value(self, attribute = 'Vitesse', ws = 'base', value = 0) -> None:
        self.eng.assignin(ws, attribute, value, nargout = 0)
    
    def set_param(self, block_path, value, type = 'Value') -> None:
        self.eng.set_param(f'{self.model_name}/{block_path}', type, str(value), nargout = 0)


if __name__ == '__main__':

    #DEBUG Section
    # Start MATLAB engine
    
    SIMULATION_PATH = 'envs/maze/'
    MODEL_PATH = f"{SIMULATION_PATH}Simulation_2_Wall_Follower_v1.slx"
    model_name = 'Simulation_2_Wall_Follower_v1'
    eng = Engine(model_path = MODEL_PATH, sim_path = SIMULATION_PATH, model_name = model_name, simulation_type='sparsesbs')
    eng.load_engine()
    eng.run_engine_script('setup')
    eng.set_simulation_mode(s_mode='Normal')

    if eng.sim_type == 'sparsesbs':
        eng.set_step_size(STEP_SIZE)

    
    eng.start_simulation()

    i = 0
    while True:
        sim_status = eng.get_param("", 'SimulationStatus')
        print(sim_status)
        if sim_status == 'stopped' :
            import numpy as  np
            print(np.array(eng.get_simout()))
            break
        if sim_status != 'paused' and eng.sim_type == 'sparsesbs':
            continue

        print(eng.get_robots_readings())

        
        

        
        """
        Now the simulation reached one step time iterations
        In between steps process calls down below
        """
        
        #print(eng.get_ws_value())
        #Carry forward in the simulation
        
        if i % 5 == 0:
            eng.stop_simulation()
            eng.update_simulation()
            
            #eng.start_simulation()
            eng.start_pause_simulation()
            print(eng.get_runtime_attribute("time1", ''))
        else:
            eng.step_forward()
            
        i+= 1


    # Close the MATLAB engine session
    eng.end_simulation()
