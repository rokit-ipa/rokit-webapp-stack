
###STILL WORK IN PROGRESS

class velocity_tracker:
    """Calculate the velocity between two timestamped coordinates"""

    def __init__(self, start, starttime, end, endtime):
        self.timestamped_start = (start, starttime)
        self.timestamped_end = (end, endtime)

    def velocity_calculation(self):
        traveled_distance = self.timestamped_end[1]- self.timestamped_start[0]
        traveled_time = self.timestamped_end[1]- self.timestamped_start[0]

        ##m_per_second = traveled_distance/traveled_time
        ##return m_per_second
        
