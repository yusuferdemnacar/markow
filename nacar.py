walls="x xx  xx x"
sensors=["on","on","off","on"]
# your code starts

movement = {"even":{"right": 0.8, "stay": 0.2}, "odd":{"right": 0.6, "stay": 0.4}}
sensor = {"wall": {"on": 0.7, "off": 0.3}, "no wall": {"on": 0.2, "off": 0.8}}
probabilities = [1/len(walls)] * len(walls)

def sense(current_position, moves, input_probabilities, sensor):
    middle_probabilities = input_probabilities.copy()
    if walls[current_position] == "x":
        middle_probabilities[current_position] = input_probabilities[current_position] * sensor["wall"][sensors[moves]]
    else:
        middle_probabilities[current_position] = input_probabilities[current_position] * sensor["no wall"][sensors[moves]]
    return middle_probabilities

def action(current_position, t, middle_probabilities, movement):
    output_probabilities = middle_probabilities.copy()
    if current_position == len(walls) - 1:
        output_probabilities[current_position] = middle_probabilities[current_position]
    else:
        if (current_position+1) % 2 == 0:
            output_probabilities[current_position + 1] = middle_probabilities[current_position] * movement["even"]["right"]
            output_probabilities[current_position] = middle_probabilities[current_position] * movement["even"]["stay"]
        else:
            output_probabilities[current_position + 1] = middle_probabilities[current_position]*movement["odd"]["right"]
            output_probabilities[current_position] = middle_probabilities[current_position] * movement["odd"]["stay"]
    return output_probabilities

filtering_probabilities = [0 for i in range(len(walls))]

for starting_position in range(len(walls)):
    position_probabilities = [0 for _ in range(len(walls))]
    position_probabilities[starting_position] = 1
    for t in range(len(sensors)):
        sum_probabilities = [0 for _ in range(len(walls))]
        for ii in range(starting_position, min(starting_position + t + 1, len(walls))):
            input_probabilities = [0 for _ in range(len(walls))]
            input_probabilities[ii] = position_probabilities[ii]
            middle_probabilities = sense(ii, t, input_probabilities, sensor)
            output_probabilities = action(ii, t, middle_probabilities, movement)
            sum_probabilities = [sum(x) for x in zip(sum_probabilities, output_probabilities)]
        position_probabilities = sum_probabilities
    filtering_probabilities = [sum(x) for x in zip(filtering_probabilities, position_probabilities)]

filtering_probabilities = [x / sum(filtering_probabilities) for x in filtering_probabilities]

robot_pos_prob = max(filtering_probabilities)
robot_pos = filtering_probabilities.index(robot_pos_prob) + 1

# your code ends
print('The most likely current position of the robot is',robot_pos,'with probability',robot_pos_prob)
