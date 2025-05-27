from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class CategoryNode:
    name: str
    children: Dict[str, "CategoryNode"] = field(default_factory=dict)

    def add_child(self, child_name: str) -> "CategoryNode":
        if child_name not in self.children:
            self.children[child_name] = CategoryNode(child_name)
        return self.children[child_name]

    def get_child(self, child_name: str) -> Optional["CategoryNode"]:
        return self.children.get(child_name)

    def get_children(self) -> List[str]:
        return list(self.children.keys())

    def has_child(self, child_name: str) -> bool:
        return child_name in self.children

    def get_all_paths(self, current_path: str = "") -> List[str]:
        paths = []
        new_path = f"{current_path}>{self.name}" if current_path else self.name

        if not self.children:
            paths.append(new_path)
        else:
            for child in self.children.values():
                paths.extend(child.get_all_paths(new_path))

        return paths


class CategoryTree:
    def __init__(self):
        self.root = CategoryNode("root")

    def add_category_path(self, category_path: str) -> None:
        """Add a category path to the tree."""
        categories = category_path.split(" > ")
        current_node = self.root

        for category in categories:
            current_node = current_node.add_child(category)

    def get_category_node(self, category_path: str) -> Optional[CategoryNode]:
        """Get a category node by its path."""
        categories = category_path.split(" > ")
        current_node = self.root

        for category in categories:
            current_node = current_node.get_child(category)
            if not current_node:
                return None

        return current_node

    def get_children(self, category_path: str) -> List[str]:
        """Get all children of a category."""
        node = self.get_category_node(category_path)
        if node:
            return node.get_children()
        return []

    def display_tree(self, node: Optional[CategoryNode] = None, prefix: str = "", is_last: bool = True) -> None:
        """
        Display the tree structure with proper tree-like visualization.

        Args:
            node: The current node to display (defaults to root)
            prefix: The prefix string for the current line
            is_last: Whether this is the last child of its parent
        """
        if node is None:
            node = self.root

        # Print the current node
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{node.name}")

        # Calculate the new prefix for children
        new_prefix = prefix + ("    " if is_last else "│   ")

        # Get all children and sort them for consistent display
        children = list(node.children.values())
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            self.display_tree(child, new_prefix, is_last_child)

    def get_all_categories(self) -> List[str]:
        """Get all category paths in the tree."""
        return self.root.get_all_paths()


# Example usage:
if __name__ == "__main__":
    # Example categories
    categories = [
        "Beverages > Fruit & Vegetable Juices > Wellness Shots",
        "Beverages > Fruit & Vegetable Juices > Other Juices",
        "Apparel & Accessories > Clothing > Underwear & Socks > Shapewear",
        "Pantry > Packaged Fruit & Applesauce > Other Packaged Fruit",
        "Sporting Goods > Athletics > Water Sports",
        "Beverages > Drink Mixes > Energy & Hydration Mixes",
        "Household Supplies > Household Cleaning Supplies > Household Cleaning Products > Dish Soap",
        "Beverages > Drink Mixes > Protein Powder",
        "Beverages > Carbonated Soft Drinks > Cola > Zero Sugar Cola",
        "Pantry > Packaged Seafood > Other Packaged Seafood",
    ]

    # Create and populate the tree
    tree = CategoryTree()
    for category in categories:
        tree.add_category_path(category)

    # Display the tree structure
    print("Tree Structure:")
    tree.display_tree()

    # Example of getting children
    print("\nChildren of 'root':")
    print(tree.get_children("root"))

    print("\nChildren of 'Beverages':")
    print(tree.get_children("Beverages"))

    # Get children of intermediate nodes
    print("\nChildren of intermediate nodes:")
    print("Children of 'Beverages > Fruit & Vegetable Juices':")
    print(tree.get_children("Beverages > Fruit & Vegetable Juices"))

    print("\nChildren of 'Pantry':")
    print(tree.get_children("Pantry"))

    print("\nChildren of 'Household Supplies > Household Cleaning Supplies':")
    print(tree.get_children("Household Supplies > Household Cleaning Supplies"))

    # Example of getting all categories
    print("\nAll categories:")
    for category in tree.get_all_categories():
        print(category)
