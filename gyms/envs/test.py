from Matlab2Py.online_matlab import OnlineEngine
import numpy as np
import keyboard


# 1 second
STEP_SIZE = 1

if __name__ == '__main__':

    #DEBUG Section
    # Start MATLAB engine
    
    SIMULATION_PATH = 'gyms/envs/maze/'
    MODEL_PATH = f"{SIMULATION_PATH}Simulation_2_Wall_Follower_v1.slx"
    model_name = 'Simulation_2_Wall_Follower_v1'
    eng = OnlineEngine(model_path = MODEL_PATH, sim_path = SIMULATION_PATH, model_name = model_name, simulation_type='sparsesbs')
    eng.load_engine()
    eng.run_engine_script('setup')
    eng.set_simulation_mode(s_mode='Normal')

    if eng.sim_type == 'sparsesbs':
        eng.set_step_size(STEP_SIZE)

    
    eng.start_simulation()

    i = 0
    while True:
        sim_status = eng.get_param("", 'SimulationStatus')
        

        if sim_status != 'paused' and eng.sim_type == 'sparsesbs':
            continue

        print(np.array(eng.get_simulation_last_readings('robot_readings', 'base')[0], dtype=np.float16))

        
        

        
        """
        Now the simulation reached one step time iterations
        In between steps process calls down below
        """
        
        #print(eng.get_ws_value())
        #Carry forward in the simulation
        if keyboard.is_pressed('q'):
            eng.end_simulation()
            print('Existing simulation')
            exit()

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
