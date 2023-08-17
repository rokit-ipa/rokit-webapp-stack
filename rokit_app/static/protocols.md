# ISO 18646 Protocol for testing the Mobile Robots

### **Test for rated speed**:

![]('../image.png')

#### Conditions:
  - The robot should be equipped with a rated load.
  - The robot should reach max speed before the start line.
  - The robot should not deviate by more than 0.1m.

#### How to test:

  - Place the robot equipped with rated load at the initial position.
  - Robot travels in a straight line till reaches the rated speed.
  - Initiate stop automatically or manually. (Stop category 1 or 2 acc.   to IEC 60204-1) (Stop initiation should be recorded by a camera).
  - Stopping distance and stopping time are measured after initiating stop until the robot completely stops.

#### Test Result:

 - Stopping distance, stopping time, specific test conditions, rated speed, the accuracy of the measurement device, stop category, and friction are to be mentioned in the report.


### **Test for maximum speed on the slope:**

#### Conditions:

  - Tests shall be performed on slopes with angles of 3°, 6°, and 10° as appropriate.
  - The angles shall be set within ±0,5°

#### How to test:

  - Place the robot equipped with rated load at an initial position on the slope of 3°, 6°, or 10.
  - The robot moves in a straight line while it is accelerating, moving with maximum speed and decelerating.
  - The speed of the robot is determined with the measurement system in the maximum speed area
  - The robot shall stop on the slope after it reaches the goal position


  
| **Travel patterns** | **Path of the robot relative to the slope** | **Driving direction of the robot** |
|---------------------|---------------------------------------------|------------------------------------|
|          1          |                    upward                   |               forward              |
|          2          |                    upward                   |              backward              |
|          3          |                   downward                  |               forward              |
|          4          |                   downward                  |              backward              |
|          5          |           lateral (perpendicular)           |               forward              |

### Test results:

| **Travel direction**             | **upward/forward** | **upward/backward** | **downward/forward** | **downward/backward** | **lateral/forward** |
|----------------------------------|--------------------|---------------------|----------------------|-----------------------|---------------------|
|  Maximum speed at 3° slope angle |                    |                     |                      |                       |                     |
|  Maximum speed at 6° slope angle |                    |                     |                      |                       |                     |
| Maximum speed at 10° slope angle |                    |                     |                      |                       |                     |

- The trial will fail if the robot does not reach the finish line of the test area or if it deviates from the designated travel direction by more than 20 % of the length of the speed measurement test area.

- The maximum speed on the slope angle for each test configuration shall be selected as the minimum speed value from three consecutive successful trials.

  
