import copy
from base import Query, Node, SegmentTree, MinHeap, DistributeTracker

class MonitorProcess:
    def __init__(self):
        self.query_list = []
        self.dt_dict = {}
        self.nodes = []
        self.hp_dict={}
    def query_controller(self, inputdata):
        for data in inputdata:
            query = Query(data[0], data[1], data[2], data[3])
            self.query_list.append(query)


    def dt_controller(self):
        for query in self.query_list:
            if query.get_status() == 0:
                dt = DistributeTracker(query)
                self.dt_dict[query] = dt

    def delete_query(self, query):
        del self.dt_dict[query]
        for node in self.nodes:
            if query in node.get_queries():
                node.delete_query(query)

    def heap_controller(self): # active nodes
        if self.nodes:

            self.hp_dict = {}
            for node in self.nodes:

                heap = MinHeap(node)
                heap.set_up(self.dt_dict)
                self.hp_dict[node] = heap


    def monitor_controller(self, element):
        #node_list = copy.deepcopy(self.nodes)
        node_list = self.nodes

        for node in node_list:
            print("!!!", node_list)
            print("=>", node)
            heap = self.hp_dict[node]
            if node.start <= element < node.end:
                node.update_count()
                print(node, node.get_count())
                i = 0
                while i in range(len(heap.heap)):
                    i += 1
                    (min, q) = heap.min()
                    if node.get_count() < min:
                        break
                    elif node.get_count() >= min:
                        heap.pop()
                        if self.dt_dict[q].report_mature_api(node) == 1:
                            self.delete_query(q)
                            if len(node.get_queries()) == 0:
                                self.nodes.remove(node)
                                self.heap_controller()

                        elif self.dt_dict[q].report_mature_api(node) == True:
                            heap.set_up(self.dt_dict)


    def set_up(self, data):
        self.query_controller(data)
        seg_tree = SegmentTree()
        seg_tree.add_queries(self.query_list)
        seg_tree.tree_setup()
        self.nodes = seg_tree.get_active_nodes()


        self.dt_controller()
        self.heap_controller()



















inputdata = [[1, 2, 'usd', 10], [2, 5, 'usd', 1], [3, 8, 'usd', 2]]
mp = MonitorProcess()
mp.set_up(inputdata)
print(mp.hp_dict)
print('\n','---------------------Start Monitor-------------------------')
mp.monitor_controller(4)
print(mp.hp_dict)

print('-------------------------------No.2-------------------------')
mp.monitor_controller(4)
print(mp.hp_dict)
mp.monitor_controller(4)
print(mp.hp_dict)


