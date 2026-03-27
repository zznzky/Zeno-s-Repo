import time as timer
import heapq
import random
from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost


def detect_collision(path1, path2):
    ##############################
    # Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
    #           There are two types of collisions: vertex collision and edge collision.
    #           A vertex collision occurs if both robots occupy the same location at the same timestep
    #           An edge collision occurs if the robots swap their location at the same timestep.
    #           You should use "get_location(path, t)" to get the location of a robot at time t.

    max_t=max(len(path1),len(path2))
    for t in range(max_t):
        loc1=get_location(path1,t)
        loc2=get_location(path2,t)

        if loc1==loc2:
            return{'loc':[loc1],'timestep':t}
        
        if t>0:
            pre_loc1=get_location(path1,t-1)
            pre_loc2=get_location(path2,t-1)
            if loc1==pre_loc2 and loc2==pre_loc1:
                return{'loc':[pre_loc1,loc1],'timestep':t}
    return None




def detect_collisions(paths):
    ##############################
    # Task 3.1: Return a list of first collisions between all robot pairs.
    #           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
    #           causing the collision, and the timestep at which the collision occurred.
    #           You should use your detect_collision function to find a collision between two robots.

    collisions=[]
    num_agents=len(paths)
    
    for i in range(num_agents):
        for j in range (i+1,num_agents):
            collision=detect_collision(paths[i],paths[j])
            if collision is not None:
                collision['a1']=i
                collision['a2']=j
                collisions.append(collision)
    return collisions


def standard_splitting(collision):
    ##############################
    # Task 3.2: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the second agent to be at the
    #                            specified location at the specified timestep.
    #           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the second agent to traverse the
    #                          specified edge at the specified timestep

    constraints=[]
    agent1=collision['a1']
    agent2=collision['a2']
    loc=collision['loc']
    timestep=collision['timestep']
    if len(loc)==1:
        constraints.append({'agent':agent1,'loc':loc,'timestep':timestep})
        constraints.append({'agent':agent2,'loc':loc,'timestep':timestep})

    elif len(loc)==2:
        constraints.append({'agent':agent1,'loc':[loc[0],loc[1]],'timestep':timestep})
        constraints.append({'agent':agent2,'loc':[loc[1],loc[0]],'timestep':timestep})
    return constraints



def disjoint_splitting(collision):
    ##############################
    # Task 4.1: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint enforces one agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the same agent to be at the
    #                            same location at the timestep.
    #           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the same agent to traverse the
    #                          specified edge at the specified timestep
    #           Choose the agent randomly

    constraints=[]
    agent1=collision['a1']
    agent2=collision['a2']
    loc=collision['loc']
    timestep=collision['timestep']
    chosen_agent=agent1 if random.randint(0,1)==0 else agent2
    if len(loc)==1:
        constraints.append({'agent':chosen_agent,'loc':loc,'timestep':timestep,'positive':True})
        constraints.append({'agent':chosen_agent,'loc':loc,'timestep':timestep,'positive':False})
    elif len(loc)==2:
        if chosen_agent==agent1:
            edge=[loc[0],loc[1]]
        else:
            edge=[loc[1],loc[0]]
        constraints.append({'agent':chosen_agent,'loc':edge,'timestep':timestep,'positive':True})
        constraints.append({'agent':chosen_agent,'loc':edge,'timestep':timestep,'positive':False})
    return constraints

def paths_violate_constraint(constraint,paths):
    assert constraint.get('positive',False)
    violating_agents=[]
    for i in range(len(paths)):
        if i ==constraint['agent']:
            continue
        t=constraint['timestep']
        loc=constraint['loc']
        if len(loc)==1:
            if get_location(paths[i],t)==loc[0]:
                violating_agents.append(i)
        elif len(loc)==2:
            if get_location(paths[i],t)==loc[1] or get_location(paths[i],t-1)==loc[0]\
               or (get_location(paths[i],t-1)==loc[1] and get_location(paths[i],t)==loc[0]):
                violating_agents.append(i)
    return violating_agents

class CBSSolver(object):
    """The high-level search of CBS."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def push_node(self, node):
        heapq.heappush(self.open_list, (node['cost'], len(node['collisions']), self.num_of_generated, node))
        print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, _, id, node = heapq.heappop(self.open_list)
        print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, disjoint=True):
        """ Finds paths for all agents from their start locations to their goal locations

        disjoint    - use disjoint splitting or not
        """

        self.start_time = timer.time()

        # Generate the root node
        # constraints   - list of constraints
        # paths         - list of paths, one for each agent
        #               [[(x11, y11), (x12, y12), ...], [(x21, y21), (x22, y22), ...], ...]
        # collisions     - list of collisions in paths
        root = {'cost': 0,
                'constraints': [],
                'paths': [],
                'collisions': []}
        for i in range(self.num_of_agents):  # Find initial path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, root['constraints'])
            if path is None:
                raise BaseException('No solutions')
            root['paths'].append(path)

        root['cost'] = get_sum_of_cost(root['paths'])
        root['collisions'] = detect_collisions(root['paths'])
        self.push_node(root)

        # Task 3.1: Testing
        print(root['collisions'])

        # Task 3.2: Testing
        for collision in root['collisions']:
            if disjoint:
                print(disjoint_splitting(collision))
            else:
                print(standard_splitting(collision))

        ##############################
        # Task 3.3: High-Level Search
        #           Repeat the following as long as the open list is not empty:
        #             1. Get the next node from the open list (you can use self.pop_node()
        #             2. If this node has no collision, return solution
        #             3. Otherwise, choose the first collision and convert to a list of constraints (using your
        #                standard_splitting function). Add a new child node to your open list for each constraint
        #           Ensure to create a copy of any objects that your child nodes might inherit
        while len(self.open_list)>0:
            p=self.pop_node()
            if len(p['collisions'])==0:
                self.print_results(p)
                return p['paths']
            collision=p['collisions'][0]
            if disjoint:
                constraints=disjoint_splitting(collision)
            else:
                constraints=standard_splitting(collision)
            for constraint in constraints:
                q={'cost':0,'constraints':list(p['constraints']),'paths':list(p['paths']),'collisions':[]}
                q['constraints'].append(constraint)
                agent=constraint['agent']
                path=a_star(self.my_map,self.starts[agent],self.goals[agent],self.heuristics[agent],agent,q['constraints'])
                if path is not None:
                    q['paths'][agent]=path
                    is_valid=True

                    if constraint.get('positive',False):
                        violating_agents=paths_violate_constraint(constraint,q['paths'])
                        for v_agent in violating_agents:
                            agent_path=a_star(self.my_map,self.starts[v_agent],self.goals[v_agent],self.heuristics[v_agent],v_agent,q['constraints'])
                            if agent_path is None:
                                is_valid=False
                                break
                            q['paths'][v_agent]=agent_path
                    if is_valid:
                        q['collisions']=detect_collisions(q['paths'])
                        q['cost']=get_sum_of_cost(q['paths'])
                        self.push_node(q)
        raise BaseException('No solutions')


    def print_results(self, node):
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(node['paths'])))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
