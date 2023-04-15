class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def delete_start(self):
        if self.head is None:
            return None
        else:
            data = self.head.data
            if self.head == self.tail:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None
            return data


    def delete_end(self):
        if self.head is None:
            return None
        else:
            data = self.tail.data
            if self.head == self.tail:
                self.head = None
                self.tail = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None
            return data

    def delete_value(self, value):
        current_node = self.head
        while current_node is not None and current_node.data != value:
            current_node = current_node.next
        if current_node is None:
            return False
        if current_node.prev is None:
            self.head = current_node.next
        else:
            current_node.prev.next = current_node.next
        if current_node.next is None:
            self.tail = current_node.prev
        else:
            current_node.next.prev = current_node.prev
        return True
    def size(self):
        count = 0
        current_node = self.head
        while current_node:
            count += 1
            current_node = current_node.next
        return count

    def get(self, index):
        if index < 0 or index >= self.size():
            raise IndexError("Index out of range")
        current_node = self.head
        for i in range(index):
            current_node = current_node.next
        return current_node.data

    def __iter__(self):
        current_node = self.head
        while current_node:
            yield current_node.data
            current_node = current_node.next

def convert_to_dllist(lst):
    dllist = DoublyLinkedList()
    for item in lst:
        dllist.append(item)
    return dllist