#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 02.02.2024
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

def update(fs_tree, queue, abrupted_nodes, nucl, fs_x, fs_xp, loop, extend, current_cid, cid, cutoff):
  if len(fs_x) > cutoff:
    fs_tree[cid] = (cid, [nucl], fs_x, fs_xp, [current_cid], [], [len(fs_xp)], loop, extend)
    fs_tree[current_cid][5].append(cid)
    queue.append(cid)
    cid += 1
  else:
    for ii, fs in enumerate(fs_x):
      abrupted_nodes[fs] = (fs_xp[ii]-1, nucl)
  return cid


def update_left(fs_tree_left, queue, abrupted_nodes_left, nucl, fs_x, fs_xp, loop, extend, current_cid, cid, cutoff):
  if len(fs_x) > cutoff:
    fs_tree_left[cid] = (cid, [nucl], fs_x, fs_xp, [], [current_cid], [len(fs_x)], loop, extend)
    fs_tree_left[current_cid][4].append(cid)
    queue.append(cid)
    cid += 1
  else:
    for ii, fs in enumerate(fs_x):
      abrupted_nodes_left[fs] = (fs_xp[ii]+1, nucl)
  return cid

def build_fs_tree_from_sequence(array, starting_seq_, names_, positions_, cutoff):

  fs_tree = {}
  abrupted_nodes = {}
  queue = []
  cid = 0
  loop = None
  seq = starting_seq_
  names = names_[::]
  positions = positions_[::]
  parents = []
  children = []
  extend = True
  coverage = [len(positions)]
  fs = (cid, [seq], names, positions, parents, children, coverage, loop, extend)
  queue.append(cid)
  fs_tree[cid] = fs
  cid += 1
  cutoff = cutoff

  while queue:

    qcid = queue.pop()

    fs = fs_tree[qcid]

    assert qcid == fs[0]

    if not fs[-1]:
      continue

    fs_a, fs_c, fs_g, fs_t, fs_n, fs_start_n = [], [], [], [], [], []
    fs_ap, fs_cp, fs_gp, fs_tp, fs_np, fs_start_p = [], [], [], [], [], []

    for ii, pos in enumerate(fs[3]):
      current_cid = fs[0]
      seq = fs[1]
      name = fs[2][ii]
      loop = None
      extend = True

      if pos + 1 == len(array):
        fs_n.append(name)
        fs_np.append(pos)
        continue

      nucl = array[pos+1]
      if nucl == "A":
        fs_a.append(name)
        fs_ap.append(pos+1)
      elif nucl == "C":
        fs_c.append(name)
        fs_cp.append(pos+1)
      elif nucl == "G":
        fs_g.append(name)
        fs_gp.append(pos+1)
      elif nucl == "T":
        fs_t.append(name)
        fs_tp.append(pos+1)
      else:
        fs_n.append(name)
        fs_np.append(pos)

    cid = update(fs_tree, queue, abrupted_nodes, "A", fs_a, fs_ap, loop, extend, current_cid, cid, cutoff)
    cid = update(fs_tree, queue, abrupted_nodes, "C", fs_c, fs_cp, loop, extend, current_cid, cid, cutoff)
    cid = update(fs_tree, queue, abrupted_nodes, "G", fs_g, fs_gp, loop, extend, current_cid, cid, cutoff)
    cid = update(fs_tree, queue, abrupted_nodes, "T", fs_t, fs_tp, loop, extend, current_cid, cid, cutoff)

    for ii, fs in enumerate(fs_n):
      abrupted_nodes[fs] = (fs_np[ii], "N")

  return fs_tree, abrupted_nodes

def build_fs_left_tree_from_sequence(array, starting_seq_, names_, positions_, cutoff):

  fs_tree = {}
  abrupted_nodes = {}
  queue = []
  cid = 0
  loop = None
  seq = starting_seq_
  names = names_[::]
  positions = positions_[::]
  parents = []
  children = []
  extend = True
  coverage = [len(positions)]
  fs = (cid, [seq], names, positions, parents, children, coverage, loop, extend)
  queue.append(cid)
  fs_tree[cid] = fs
  cid += 1
  cutoff = cutoff

  while queue:

    qcid = queue.pop()

    fs = fs_tree[qcid]

    assert qcid == fs[0]

    if not fs[-1]:
      continue

    fs_a, fs_c, fs_g, fs_t, fs_n, fs_start_n = [], [], [], [], [], []
    fs_ap, fs_cp, fs_gp, fs_tp, fs_np, fs_start_p = [], [], [], [], [], []

    for ii, pos in enumerate(fs[3]):
      current_cid = fs[0]
      seq = fs[1]
      name = fs[2][ii]
      loop = None
      extend = True

      if pos - 1 == 0:
        fs_n.append(name)
        fs_np.append(pos)
        continue

      nucl = array[pos-1]
      if nucl == "A":
        fs_a.append(name)
        fs_ap.append(pos-1)
      elif nucl == "C":
        fs_c.append(name)
        fs_cp.append(pos-1)
      elif nucl == "G":
        fs_g.append(name)
        fs_gp.append(pos-1)
      elif nucl == "T":
        fs_t.append(name)
        fs_tp.append(pos-1)
      else:
        fs_n.append(name)
        fs_np.append(pos)

    cid = update_left(fs_tree, queue, abrupted_nodes, "A", fs_a, fs_ap, loop, extend, current_cid, cid, cutoff)
    cid = update_left(fs_tree, queue, abrupted_nodes, "C", fs_c, fs_cp, loop, extend, current_cid, cid, cutoff)
    cid = update_left(fs_tree, queue, abrupted_nodes, "G", fs_g, fs_gp, loop, extend, current_cid, cid, cutoff)
    cid = update_left(fs_tree, queue, abrupted_nodes, "T", fs_t, fs_tp, loop, extend, current_cid, cid, cutoff)

    for ii, fs in enumerate(fs_n):
      abrupted_nodes[fs] = (fs_np[ii], "N")

  return fs_tree, abrupted_nodes

def build_fs_tree_from_kmers(kmer2tf, starting_seq_, names_, positions_, cutoff, k=23):

  fs_tree = {}
  abrupted_nodes = {}
  queue = []
  cid = 0
  loop = None
  seq = starting_seq_
  names = names_[::]
  positions = positions_[::]
  parents = []
  children = []
  extend = True
  coverage = [len(positions)]
  fs = (cid, [seq], names, positions, parents, children, coverage, loop, extend)
  queue.append(cid)
  fs_tree[cid] = fs
  cid += 1
  cutoff = cutoff

  start_nodes = {}
  for pos in positions:
    start_nodes[pos] = 0

  while queue:

    qcid = queue.pop()

    fs = fs_tree[qcid]

    assert qcid == fs[0]

    if not fs[-1]:
      continue

    fs_a, fs_c, fs_g, fs_t, fs_n, fs_start_n = [], [], [], [], [], []
    fs_ap, fs_cp, fs_gp, fs_tp, fs_np, fs_start_p = [], [], [], [], [], []

    for ii, pos in enumerate(fs[3]):
      current_cid = fs[0]
      seq = fs[1]
      name = fs[2][ii]
      loop = None
      extend = True

      if pos + 1 in start_nodes:
        fs_start_n.append(name)
        fs_start_p.append(pos+1)
        continue


      nucl = kmer2tf.reads[pos+k]
      if nucl == 65:
        fs_a.append(name)
        fs_ap.append(pos+1)
      elif nucl == 67:
        fs_c.append(name)
        fs_cp.append(pos+1)
      elif nucl == 71:
        fs_g.append(name)
        fs_gp.append(pos+1)
      elif nucl == 84:
        fs_t.append(name)
        fs_tp.append(pos+1)
      else:
        fs_n.append(name)
        fs_np.append(pos+1)

    if len(fs_start_n) > cutoff:
      fs_tree[0][4].append(current_cid)
      fs_tree[current_cid][5].append(0)
    if fs_start_n:
      for ii, fs in enumerate(fs_start_n):
        abrupted_nodes[fs] = (fs_start_p[ii], "L")

    cid = update(fs_tree, queue, abrupted_nodes, "A", fs_a, fs_ap, loop, extend, current_cid, cid, cutoff)
    cid = update(fs_tree, queue, abrupted_nodes, "C", fs_c, fs_cp, loop, extend, current_cid, cid, cutoff)
    cid = update(fs_tree, queue, abrupted_nodes, "G", fs_g, fs_gp, loop, extend, current_cid, cid, cutoff)
    cid = update(fs_tree, queue, abrupted_nodes, "T", fs_t, fs_tp, loop, extend, current_cid, cid, cutoff)

    for ii, fs in enumerate(fs_n):
      abrupted_nodes[fs] = (fs_np[ii], "N")

  return fs_tree, abrupted_nodes

def simplify_repeat_wave_graph(fs_tree):
  ### simplifications
  #### 1) simple path1
  changed = True
  while changed:
    changed = False
    for fs in fs_tree:
      if fs_tree[fs] is None:
        continue
      cid1, seq1, names1, positions1, parents1, children1, cov, loop1, extend1 = fs_tree[fs]
      if not extend1:
        continue

      if len(children1) == 1:
        child = children1[0]
        cid2, seq2, names2, positions2, parents2, children2, cov2, loop2, extend2 = fs_tree[child]
        if len(parents2) == 1 and parents2[0] == cid1:
          # print(len(names1), len(names2))
          # print(parents1, cid1, children1, "|", parents2, cid2, children2)

          fs_tree[fs] = list(fs_tree[fs])

          fs_tree[fs][1] += seq2
          fs_tree[fs][2] = names2
          fs_tree[fs][3] = positions2
          fs_tree[fs][5] = children2
          fs_tree[fs][6] += cov2
          fs_tree[fs][7] = loop2
          fs_tree[fs][8] = extend2

          for child2 in children2:
            fs_tree[child2] = list(fs_tree[child2])
            fs_tree[child2][4].append(cid1)
            fs_tree[child2][4] = [x for x in fs_tree[child2][4] if x != cid2]

          fs_tree[child] = None

          changed = True

    print(len([x for x in fs_tree if fs_tree[x] != None]))

  new_tree = {}
  for fs in fs_tree:
    if fs_tree[fs] is not None:
      new_tree[fs] = fs_tree[fs]

  return new_tree

def call_right_sequences(fs_tree):
  leaves = []
  total = 0
  for ii, fs in enumerate(fs_tree):
    if not fs_tree[fs][5]:
      leaves.append(fs)
      total += len(fs_tree[fs][3])
  start2pos = {}
  for ii, node in enumerate(fs_tree[0][2]):
    start2pos[node] = fs_tree[0][3][ii]

  sequences = []
  for leaf in leaves:
    for ii, node in enumerate(fs_tree[leaf][2]):
      L = abs(start2pos[node]-fs_tree[leaf][3][ii])+k
      sequences.append((leaf, node, L, start2pos[node], fs_tree[leaf][3][ii]+k))
  return sequences


def call_left_sequences(fs_tree):
  leaves = []
  total = 0
  for ii, fs in enumerate(fs_tree):
    if not fs_tree[fs][4]:
      leaves.append(fs)
      total += len(fs_tree[fs][3])
  start2pos = {}
  for ii, node in enumerate(fs_tree[0][2]):
    start2pos[node] = fs_tree[0][3][ii]

  sequences = []
  for leaf in leaves:
    for ii, node in enumerate(fs_tree[leaf][2]):
      L = abs(start2pos[node]-fs_tree[leaf][3][ii])+k
      sequences.append((leaf, node, L, fs_tree[leaf][3][ii], start2pos[node]+k))
  return sequences

def join_left_right(left_sequences, right_sequences):
  sequences = []
  i, j = 0, 0
  while i < len(left_sequences) and j < len(right_sequences):
    nodeA = left_sequences[i][1]
    nodeB = right_sequences[j][1]
    if nodeA < nodeB:
      i += 1
    elif nodeA > nodeB:
      j += 1
    else:
      s = list(left_sequences[i])
      s[4] = right_sequences[j][4]
      s[2] = abs(s[3] - s[4])
      sequences.append(s)
      i += 1
      j += 1
  return sequences