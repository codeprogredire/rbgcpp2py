import rbg_game
import random
import time

bitarraystack = rbg_game.resettable_bitarray_stack()

# This modifies the input state. Calculates the keeper closure on the given state.
def keeper_closure(state):
  move_exists = True
  while state.get_current_player() == 0 and move_exists:
    move_exists = state.apply_any_move(bitarraystack)

# Visits all the game tree of a given game to the given depth
# Returns a pair of numbers of leaves visited and number of nodes visited
def perft(state, depth):
  if not state:
    return [0,0]
  if depth == 0:
    return [1,1] 
  moves = state.get_all_moves(bitarraystack)
  result = [0,0]
  result[1] += 1
  for move in moves:
    next_state = state.copy()
    next_state.apply_move(move)
    keeper_closure(next_state)
    rec_result = perft(next_state, depth-1)
    result[0] += rec_result[0]
    result[1] += rec_result[1]
  return result

# Play the game till the end from the current state. 
# This modifies the given state.
def playout(state):
  keeper_closure(state)
  moves = state.get_all_moves(bitarraystack)
  nodes = 1
  while moves:
    move = random.choice(moves)
    state.apply_move(move)
    keeper_closure(state)
    moves = state.get_all_moves(bitarraystack)
    nodes += 1
  return [state.get_player_score(i) for i in range(1,rbg_game.number_of_players())], nodes

__RBG_BENCHMARK_PLAYOUTS__=1000
__RBG_BENCHMARK_DEPTH__=3
def benchmark():
  points = [0 for i in range(1,rbg_game.number_of_players())]
  nodes = 0
  begin = time.time()
  begin_state = rbg_game.game_state()
  for i in range(__RBG_BENCHMARK_PLAYOUTS__):
    results, nodes_visited = playout(begin_state.copy())
    for player, score in enumerate(results):
      points[player] += score
      nodes += nodes_visited
    if i % 100 == 0:
      print('Played out',i,'out of',__RBG_BENCHMARK_PLAYOUTS__)
  end = time.time()
  print('Done',__RBG_BENCHMARK_PLAYOUTS__,'games in',end-begin,'s')
  print('Visited',nodes,'nodes (',nodes/(end - begin),' nodes/sec)')
  print('Average scores:')
  for player, score in enumerate(points):
    print(player+1,':',score/__RBG_BENCHMARK_PLAYOUTS__)
  begin = time.time()
  result = perft(rbg_game.game_state(), __RBG_BENCHMARK_DEPTH__)
  end = time.time()
  print('Calculated perft to depth',__RBG_BENCHMARK_DEPTH__,'in',end-begin,'s')
  print('Visited',result[1],'nodes (',nodes/(end - begin),' nodes/sec)')
  print('There are',result[0],'leaves and',result[1],'nodes')
