class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

    def __repr__(self):
        return str(self.data)


class DoublyLinkedList_Short:
    def __init__(self):
        self.head = None
        self.tail = None

    def __repr__(self):
        values = []
        current = self.head
        while current is not None:
            values.append(current.data)
            current = current.next
        return f"DLL({values})"

    def __len__(self):
        return self.size()

    def size(self):
        count = 0
        current_node = self.head
        while current_node:
            count += 1
            current_node = current_node.next
        return count

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def append_if_lacks(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                if current.data == data:
                    return
                current = current.next
            if current.data == data:
                return
            current.next = new_node
            new_node.prev = current

    def count(self, data):
        count = 0
        current = self.head
        while current is not None:
            if current.data == data:
                count += 1
            current = current.next
        return count

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

    def merge(self, other):
        if self.head is None:
            self.head = other.head
        elif other.head is not None:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = other.head
            other.head.prev = current

    def is_empty(self):
        return self.head is None

    def get(self, index):
        if index < 0 or index >= self.size():
            raise IndexError("Index out of range")
        current_node = self.head
        for i in range(index):
            current_node = current_node.next
        return current_node.data

    def get_and_remove(self, index):
        if self.head is None:
            raise IndexError("list index out of range")
        elif index == 0:
            data = self.head.data
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None
            return data
        else:
            current = self.head
            for i in range(index):
                if current.next is None:
                    raise IndexError("list index out of range")
                current = current.next
            data = current.data
            current.prev.next = current.next
            if current.next is not None:
                current.next.prev = current.prev
            return data

    def __iter__(self):
        current_node = self.head
        while current_node:
            yield current_node.data
            current_node = current_node.next
