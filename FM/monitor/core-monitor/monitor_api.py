import math
import heapq
from operator import itemgetter
from websocket import create_connection
import simplejson as json


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_contains(self, interval):
        """
        Return True if it contains a given interval
        e.g. interval1=[3, 9) and interval2=[4, 5.5)
        interval1 contains interval2, so interval1.is_contains(interval2) => TRUE
        """
        if interval:
            return self.start <= interval.start and interval.end <= self.end

    def is_intersect(self, interval):
        """Return True if self is intersect interval"""
        # s=(2, 6) i=(3, 8)  or s->(3, 8) i->(2, 6)
        if interval:           return self.start < interval.end or self.end > interval.start

    def get_endpoints(self):
        return self.start, self.end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def __repr__(self):
        return "[{}, {})".format(self.start, self.end)

    def __str__(self):
        return repr(self)


class Query(Interval):
    def __init__(self, start, end, id, target):
        super().__init__(start, end)
        self.id = id  # Stock name
        self._target = target  # target amount to monitor
        self._nodes = []
        self.status = 0  # 1 mature, 0 unmature

    def add_node(self, node):
        self._nodes.append(node)

    def update_status(self):
        self.status = 1

    def get_id(self):
        return self.id

    def get_status(self):
        return self.status

    def get_target(self):
        return self._target

    def get_nodes(self):
        return self._nodes

    def __hash__(self):
        return hash(self.start + self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return self.start != other.start or self.end != other.end

    def __repr__(self):
        return "Query([{}, {}), {}, {}, {})".format(self.start, self.end, self.status, self._target, self._nodes)


class Node(Interval):
    def __init__(self, start, end):
        super().__init__(start, end)
        self.left = None  # left child
        self.right = None  # right child
        self.queries = []  # a list to put Queries assigned to this Node
        self.counter = 0

    def set_child(self, left, right):
        """
        Set child node
        """
        self.left = left
        self.right = right

    def add_query(self, query):
        """
        Insert a query to a node
        """
        self.queries.append(query)

    def delete_query(self, query):
        self.queries.remove(query)

    def update_count(self):
        self.counter += 1

    def get_queries(self):
        """
        Return a list of Queries inserted in this node
        """
        return self.queries

    def get_count(self):
        """
        Return it count
        """
        return self.counter

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def is_leaf(self):
        return self.left is None and self.right is None

    def __hash__(self):
        return hash(self.start + self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return self.start != other.start or self.end != other.end

    def __repr__(self):
        return "Node([{}, {}), Counter: {})".format(self.start, self.end, self.counter)
        # return 'Node: {}'.format(self.counter)


class SegmentTree(Node):

    def __init__(self):
        self.root = None
        self._endpoints = []  # a list to hold all start and end of queries
        self._leaf_nodes = []  # a list to hold leaf nodes of the tree
        self._queries = []
        self.height = 0  # tree height
        self.all_nodes = {0: self._leaf_nodes}
        self._active_nodes = []  # a list stored nodes need to monitor

    def add_query(self, query):
        """Add one query"""
        self._queries.append(query)

    def add_queries(self, queries):
        """Add a list of Queries"""
        self._queries.extend(queries)

    def add_endpoints(self):
        for query in self._queries:
            self._endpoints.extend(query.get_endpoints())
        self._endpoints.sort()

    def update_leaf_nodes(self):
        i = 0
        while i < len(self._endpoints) - 1:
            node = Node(self._endpoints[i], self._endpoints[i + 1])
            self._leaf_nodes.append(node)
            i += 1

    def is_active_node(self, node):
        """
        Check if a node is need to monitor, namely active
        :param node: Node
        :return: boolean
        """
        return node.get_queries()

    def get_active_nodes(self):
        return self._active_nodes

    def build(self, nodes_list):
        """
        Build BST with leaf nodes bottom-up.
        """
        nodes_new = []
        self.height += 1
        num = len(nodes_list)  # the number of nodes in nodes_list
        if num == 1:
            self.root = nodes_list[0]
            return  # check later
        elif num > 1:
            if num % 2 == 0:
                nodes_new = self.parent_nodes(nodes_list, num)
            elif num % 2 == 1:
                nodes_new = self.parent_nodes(nodes_list, num - 1)
                nodes_new.append(nodes_list[-1])
            self.all_nodes[self.height] = nodes_new
            self.build(nodes_new)

    @staticmethod
    def parent_nodes(nodes, num):
        parent_nodes = []
        i = 0
        while i < num:
            left = nodes[i]  # left child
            right = nodes[i + 1]  # right child
            parent = Node(left.get_start(), right.get_end())
            parent.set_child(left, right)
            parent_nodes.append(parent)
            i += 2
        return parent_nodes

    def insert_query(self, node, query):
        """
        Assign query to tree node, default inserting starts from ROOT node
        """
        if query.is_contains(node):  # if query contains node
            node.add_query(query)  # add query to the node
            query.add_node(node)  # add node to the query
            self._active_nodes.append(node)
            return
        else:
            if query.is_intersect(node.left):
                self.insert_query(node.left, query)

            if query.is_intersect(node.right):
                self.insert_query(node.right, query)

    def tree_setup(self):
        """
        Build the tree bottom-up, insert Query, update Query.nodes and Node.queries
        Ready for Monitor
        !!! After Tree Setup, cannot add any new Query or delete existing Query
        """
        self.add_endpoints()

        self.update_leaf_nodes()

        self.build(self._leaf_nodes)

        for query in self._queries:
            self.insert_query(self.root, query)

    def __repr__(self):
        return "SegmentTree(root->{}, height->{}, {})".format(self.root, self.height, self.all_nodes)


class MinHeap:

    def __init__(self, node):
        self.node = node
        self.heap = []

    def set_up(self, dt_dict):
        t_lsit = []
        queries = self.node.get_queries()

        for query in queries:
            if query.get_status() == 0:
                future_count = dt_dict[query].get_future_count(self.node)
                t_lsit.append((future_count, query))
        self.heap = sorted(t_lsit)

    def pop(self):
        if self.heap:
            return self.heap.pop(0)  # pop the min item of heap and return min

    def min(self):  # only return min item
        if self.heap:
            return self.heap[0]


class DistributeTracker:

    def __init__(self, query):
        self._query = query  # coordinator
        self._target = query.get_target()
        self._signal = 0
        self._counters = {}  # a dict to store last count

    @property  # participants
    def _nodes(self):
        return self._query.get_nodes()

    @property
    def _amount(self):  # target amount
        return self._query.get_target()

    @property
    def _num_of_participants(self):
        return len(self._nodes)

    @property
    def _slack(self):  # when the first round finishes, self._target will change, and  self._slack change also
        slack = math.ceil(self._amount / (2 * self._num_of_participants))

        return slack

    def set_counters(self):
        for node in self._nodes:
            self._counters[node] = node.get_count()

    def _update_counters(self, node):
        self._counters[node] = node.get_count()

    def _update_target(self):  # calculate the new target amount
        sum_counters = sum(self._counters.values())
        self._target = self._target - sum_counters

    def _send_signal(self, node):

        count_last = self._counters[node]
        count = node.get_count()
        if count - count_last == self._slack:
            self._signal += 1
        self._update_counters(node)

    def _tracking_signal(self):
        if self._signal == self._num_of_participants:
            self._signal = 0  # set signal tracking to 0
            self._update_target()  # collect all sites count and update target
            return True

    def get_future_count(self, node):  # this will be used in min-heap

        count_future = node.get_count() + self._slack
        return count_future

    def report_mature_api(self, node):  # this is the api where need external data
        self.set_counters()

        if self._target <= 6 * self._num_of_participants:
            total_count = sum(self._counters.values())
            if total_count == self._query.get_target():
                self._query.update_status()
                print('COOL!', 'The Query [', self._query, '] is MATURE')
                return 1

                # TODO alert User and delete the query or set this query as history
        else:
            self._send_signal(node)  # check if need to send signal to coordinate
            self._tracking_signal()  # check if need to collect mgs


class MonitorProcess:
    def __init__(self):
        self.query_list = []
        self.dt_dict = {}
        self.nodes = []
        self.hp_dict = {}

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

    def heap_controller(self):  # active nodes
        if self.nodes:

            self.hp_dict = {}
            for node in self.nodes:
                heap = MinHeap(node)
                heap.set_up(self.dt_dict)
                self.hp_dict[node] = heap

    def monitor_controller(self, element):
        # node_list = copy.deepcopy(self.nodes)
        node_list = self.nodes
        print("####==>", node_list, '\n')

        for node in node_list:
            # print("!!!", node_list)
            # print("=>", node)
            heap = self.hp_dict[node]
            if node.start <= element < node.end:
                node.update_count()
                # print(node, node.get_count())
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


# inputdata = [[6870, 6875, 'btceur', 100], [6868, 6873, 'btceur', 2], [6871, 6881, 'btceur', 2]]
inputdata = [[8017, 8023, 'btceur', 17], [8000, 8015, 'btceur', 120], [8013, 8022, 'btceur', 140]]
mp = MonitorProcess()
mp.set_up(inputdata)

ws = create_connection("wss://api.tiingo.com/crypto")

subscribe = {
    'eventName': 'subscribe',
    'authorization': '993e1b0a543e60b88848094cb90521871a02711e',
    'eventData': {
        'tickers': ['btcusd']
    }
}

ws.send(json.dumps(subscribe))

while (True):
    json_data = json.loads(ws.recv())
    if json_data['messageType'] == 'A':
        fx_data = json_data['data']
        price = fx_data[-1]
        print('Price==>', price)
        mp.monitor_controller(price)
