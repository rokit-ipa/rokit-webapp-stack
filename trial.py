data = [('floor_type', 'wood'), ('floor_type', 'wood'), ('floor_type', 'wood'), ('floor_type', 'wood'), ('floor_type', 'wood'), ('floor_type', 'wood'), ('floor_type', 'wood'), ('floor_type', 'wood'), ('floor_type', 'wood'), ('humidity', 80.0), ('humidity', 80.0), ('humidity', 80.0), ('humidity', 80.0), ('humidity', 80.0), ('humidity', 80.0), ('humidity', 80.0), ('humidity', 80.0), ('humidity', 80.0), ('inclination', 0.0), ('inclination', 0.0), ('inclination', 0.0), ('inclination', 0.0), ('inclination', 0.0), ('inclination', 0.0), ('inclination', 0.0), ('inclination', 0.0), ('inclination', 0.0), ('notes', 'none'), ('notes', 'none'), ('notes', 'none'), ('notes', 'none'), ('notes', 'none'), ('notes', 'none'), ('notes', 'none'), ('notes', 'none'), ('notes', 'none'), ('temperature', 25.0), ('temperature', 25.0), ('temperature', 25.0), ('temperature', 25.0), ('temperature', 25.0), ('temperature', 25.0), ('temperature', 25.0), ('temperature', 25.0), ('temperature', 25.0), ('tracking_object', None), ('tracking_object', None), ('tracking_object', None), ('tracking_object', None), ('tracking_object', None), ('tracking_object', None), ('tracking_object', None), ('tracking_object', None), ('tracking_object', None), ('trial_number', 1.0), ('trial_number', 2.0), ('trial_number', 3.0), ('trial_number', 4.0), ('trial_number', 5.0), ('trial_number', 6.0), ('trial_number', 7.0)]

attribute_order = ['trial_number', 'tracking_object', 'temperature', 'humidity', 'floor_type', 'inclination']

def process_data(data_list):
    processed_data = {}
    
    for key, value in data_list:
        if key in processed_data:
            processed_data[key].append(value)
        else:
            processed_data[key] = [value]
    
    for attribute in attribute_order:
        values = processed_data.get(attribute, [None] * len(data_list))
        print(', '.join(str(val) for val in values))

process_data(data)