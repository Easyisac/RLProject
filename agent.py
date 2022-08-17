def get_action_0(state, step, delta):  # timer
    timer = 50
    right, up, left, down, light = state
    print('cars in lanes:\n'
          'right: {}, up: {}, left: {}, down: {}\n'
          'traffic light phase: {}\n'
          'time step: {}'.format(right, up, left, down, light, step))

    if delta >= timer and light == 2:
        return 3
    elif delta >= timer and light == 0:
        return 1
    else:
        return None


def get_action_1(state, step, delta):  # Switch quando ci sono almeno 5 macchine in una coda
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


def get_action_2(state, step, delta):  # Switch quando c'è una corsia completamente libera
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


def get_action_3(state, step, delta):  # Switch con corsia libera + timer
    timer = 50
    right, up, left, down, light = state
    print('cars in lanes:\n'
          'right: {}, up: {}, left: {}, down: {}\n'
          'traffic light phase: {}\n'
          'time step: {}'.format(right, up, left, down, light, step))

    if (left == 0 and right == 0 and light == 2) or (delta >= timer and light == 2):
        return 3
    elif (up == 0 and down == 0 and light == 0) or (delta >= timer and light == 0):
        return 1
    else:
        return None

def get_action(state, step, delta):
    return get_action_3(state, step, delta)
