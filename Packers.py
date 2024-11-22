from Node import Node, Rect


class Packer():

    def __init__(self, min_w:int, min_h:int) -> None:
        self.root = Node((0,0), (min_w, min_h))
        self.bounds = (min_w, min_h)
        self.rects = []
    

    def increment_size(self, amount:int = 1) -> None:
        """ Increment the size of the bounds by +amount in both directions"""
        self.bounds = (self.bounds[0] + amount, self.bounds[1] + amount)
        self.root = Node((0,0), (self.bounds[0] + amount, self.bounds[1] + amount))


    def n_in_bounds(self) -> int:
        """ Get the number of rects that are inbound"""
        return sum([r.inbounds for r in self.rects])


    def n_outside_bounds(self) -> int:
        """ Get the number of rects that are out of bounds"""
        return len(self.rects) - self.n_in_bounds()


    def filled_pct(self) -> float:
        """ Get the percentage of the total area that is filled"""
        filled_area = sum([r.w*r.h for r in self.rects if r.inbounds])
        total_area = self.bounds[0]*self.bounds[1]
        return filled_area / float(total_area)


    def fit(self, rects: list[Rect]) -> list[Rect]:
        for rect in rects:
            # Find a suitable node for the rectangle
            node = self.find_node(self.root, rect.w, rect.h)

            # If a node is found, split it and assign the rectangle's fit
            if node:
                rect.fit = self.split_node(node, rect.w, rect.h)

            # Set the inbounds variable based on the rectangle's position
            if rect.fit:
                rect.inbounds = (
                    0 <= rect.fit.x and
                    0 <= rect.fit.y and
                    rect.fit.x + rect.w <= self.bounds[0] and
                    rect.fit.y + rect.h <= self.bounds[1]
                )
            else:
                rect.inbounds = False

        # Second pass: compact floating rectangles
        for rect in rects:
            if not rect.inbounds:
                node = self.find_node(self.root, rect.w, rect.h)
                if node:
                    rect.fit = self.split_node(node, rect.w, rect.h)
                    rect.inbounds = True

        return rects


    def _fit(self, rects:list[Rect]) -> list[Rect]:
        ...


    def find_node(self, node: Node, w: int, h: int) -> Node:
        # If the current node is used, prioritize 'down' before 'right'
        if node.used:
            return self.find_node(node.down, w, h) or self.find_node(node.right, w, h)
        # Check if the rectangle fits in this node
        elif w <= node.w and h <= node.h:
            return node
        else:
            return None


    def split_node(self, node: Node, w: int, h: int) -> Node:
        # Mark the node as used
        node.used = True
        
        # Ensure the node has enough space for splitting
        if node.h < h or node.w < w:
            raise ValueError("Invalid split: Node size is too small for the rectangle.")
        
        # Create the down node (below the placed rectangle)
        node.down = Node(
            origin=(node.x, node.y + h),
            size=(node.w, node.h - h)
        )
        
        # Create the right node (to the right of the placed rectangle)
        node.right = Node(
            origin=(node.x + w, node.y),
            size=(node.w - w, h)
        )
        
        return node



class SimplePacker(Packer):

    def _fit(self, rects:list[Rect]) -> list[Rect]:
        for rect in rects:
            node = self.find_node(self.root, rect.w, rect.h)
            if node:
                rect.fit = self.split_node(node, rect.w, rect.h)
        
            # Set inbound variable for each rect
            if rect.fit:
                rect.inbounds = False if self.root.x+self.bounds[0] < rect.fit.x or self.root.y+self.bounds[1] < rect.fit.y else True
            else:
                rect.inbounds = False

        return rects



class AdvancedPacker(Packer):

    def _fit(self, rects:list[Rect]) -> list[Rect]:
        for rect in rects:
            node = self.find_node(self.root, rect.w, rect.h)
            if node:
                rect.fit = self.split_node(node, rect.w, rect.h)
            else:
                rect.fit = self.grow_node(rect.w, rect.h)
            
            # Set inbound variable for each rect
            rect.inbounds = False if self.root.x+self.bounds[0] <= rect.fit.x or self.root.y+self.bounds[1] <= rect.fit.y else True

        return rects


    def grow_node(self, w:int, h:int):
        can_grow_down = w <= self.root.w
        can_grow_right = w <= self.root.h

        should_grow_right = can_grow_right and (self.root.w + w <= self.root.h)
        should_grow_down = can_grow_down and (self.root.h + h <= self.root.w)
        
        if should_grow_right:
            return self.grow_right(w,h)
        elif should_grow_down:
            return self.grow_down(w,h)
        elif can_grow_right:
            return self.grow_right(w,h)
        elif can_grow_down:
            return self.grow_down(w,h)
        else:
            return None


    def grow_down(self, w:int, h:int):
        new_root = Node((0,0), (self.root.w, self.root.h + h))
        new_root.used = True
        new_root.down = Node((0, self.root.h), (self.root.w, h))
        new_root.right = self.root

        self.root = new_root
        return self.next(w,h)


    def grow_right(self, w:int, h:int):
        new_root = Node((0,0), (self.root.w + w, self.root.h))
        new_root.used = True
        new_root.down = self.root
        new_root.right = Node((self.root.w, 0), (w, self.root.h))

        self.root = new_root
        return self.next(w,h)


    def next(self, w, h):
        node = self.find_node(self.root, w, h)
        if node:
            return self.split_node(node, w, h)
        else:
            return None
