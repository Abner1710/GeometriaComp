class DoublyLinkedItem:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self, first_element_value):
        first = DoublyLinkedItem(first_element_value)
        first.next = first
        first.prev = first

        self.head = first
        self.active = first
        self.size = 1

    def move_right(self):
        self.active = self.active.next
    
    def move_left(self):
        self.active = self.active.prev

    def insert_end(self, value):
        new_item = DoublyLinkedItem(value)
        
        last = self.head.prev
        
        new_item.next = self.head
        new_item.prev = last
        self.head.prev = new_item
        last.next = new_item
        self.size += 1

    def remove(self):
        if self.size <= 1:
            raise ValueError("Invalid operation")
        if self.active == self.head:
            self.head = self.head.next
        self.active.next.prev = self.active.prev
        self.active.prev.next = self.active.next
        self.active = self.active.next
        self.size -= 1

    def remove_item(self, item):
        if self.size <= 1:
            raise ValueError("Invalid operation")
        if item == self.head:
            self.head = self.head.next
        item.next.prev = item.prev
        item.prev.next = item.next
        item = item.next
        self.size -= 1
    
    def __len__(self):
        return self.size
    
    def enumerate_values(self):
        values = []
        curr = self.head
        for _ in range(len(self)):
            values.append(curr.value)
            curr = curr.next
        return values

