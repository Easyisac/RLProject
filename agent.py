def get_action_0(state, step): #Switch quando ci sono almeno 5 macchine in una coda
    right, up, left, down, light = state
    print('cars in lanes:\n'
          'right: {}, up: {}, left: {}, down: {}\n'
          'traffic light phase: {}\n'
          'time step: {}'.format(right, up, left, down, light, step))

    if (left > 4 or right > 4) and (light != 1 and light != 2):
        return 1
    elif (up > 4 or down > 4) and (light != 3 and light != 0):
        return 3
    else:
        return None

def get_action_1(state, step): #Switch quando c'è una corsia completamente libera
    right, up, left, down, light = state
    print('cars in lanes:\n'
          'right: {}, up: {}, left: {}, down: {}\n'
          'traffic light phase: {}\n'
          'time step: {}'.format(right, up, left, down, light, step))

    if left == 0 and right == 0 and light == 2:
        return 3
    elif up == 0 and down == 0 and light == 0:
        return 1
    else:
        return None

def get_action(state, step):
    right, up, left, down, light = state
    print('cars in lanes:\n'
          'right: {}, up: {}, left: {}, down: {}\n'
          'traffic light phase: {}\n'
          'time step: {}'.format(right, up, left, down, light, step))

    if left == 0 and right == 0 and light == 2:
        return 3
    elif up == 0 and down == 0 and light == 0:
        return 1
    else:
        return None

