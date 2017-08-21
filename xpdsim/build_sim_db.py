"""this module exists for simulation environment"""

def build_sim_db():
    from databroker import temp_config, Broker
    return Broker.from_config(temp_config())
