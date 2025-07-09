import weakref


class TreeNode:
    """
    一个功能完备的树节点类：
    - 通过属性路径访问子节点 (node.child)
    - 在节点上存储任意数据 (.data)
    - 子节点可以反向访问父节点 (.parent)，使用弱引用防止循环引用
    - 支持多级路径操作
    """

    def __init__(self, name: str, data: any = None, parent: "TreeNode" = None):
        """初始化一个节点。"""
        self.name = name
        self.data = data
        self._children = {}
        self._parent = weakref.ref(parent) if parent else None

    @property
    def parent(self):
        """以属性的方式返回父节点对象。"""
        return self._parent() if self._parent else None

    def add_child(self, name: str = None, data: any = None):
        """
        向当前节点或其子节点添加/更新数据。
        - 如果提供了 name (路径)，则会沿路径创建节点，并将数据设置在路径末端。
        - 如果 name 为 None，则直接更新当前节点的数据。

        Args:
            name (str, optional): 点分隔的路径字符串。默认为 None。
            data (any, optional): 要存储的数据。默认为 None。
        """
        # 如果 name 为 None，直接更新当前节点的数据
        if name is None:
            self.data = data
            return self

        path_segments = name.split(".")
        current_node = self
        for segment in path_segments:
            # 跳过空的路径段，以处理像 "a..b" 或 "" 这样的情况
            if not segment:
                continue
            if segment not in current_node._children:
                # 如果子节点不存在，创建它并设置好父节点
                new_node = TreeNode(name=segment, parent=current_node)
                current_node._children[segment] = new_node
                current_node = new_node
            else:
                # 如果存在，则移动到该子节点
                current_node = current_node._children[segment]

        # 将数据设置在路径的最终节点上
        if data is not None:
            current_node.data = data
        return current_node

    def has_child(self, path: str) -> bool:
        """判断是否有指定路径的孩子节点。"""
        return self.get_child(path) is not None

    def get_child(self, path: str):
        """根据路径获取一个孩子节点。"""
        if not path:
            return None
        path_segments = path.split(".")
        current_node = self
        for segment in path_segments:
            # 跳过空的路径段，以处理像 "a..b" 这样的情况
            if not segment:
                continue
            if isinstance(current_node, TreeNode) and segment in current_node._children:
                current_node = current_node._children[segment]
            else:
                return None  # 路径中任何一段无效，则立即返回 None

        # 如果路径有效，则 current_node 就是目标节点
        return current_node

    def get_children(self, path: str = None):
        """
        获取指定路径下节点的所有子节点。
        - 如果 path 为 None，返回当前节点的所有子节点。
        - 如果路径无效，则返回 None。

        Args:
            path (str, optional): 点分隔的路径字符串。默认为 None。

        Returns:
            dict[str, TreeNode] or None: 子节点字典或 None。
        """
        target_node = self if path is None else self.get_child(path)
        if isinstance(target_node, TreeNode):
            return target_node._children
        return None

    def remove_child(self, path: str) -> bool:
        """根据路径删除一个孩子节点。"""
        if not path:
            return False

        path_segments = path.split(".")
        child_name = path_segments[-1]
        parent_path_segments = path_segments[:-1]

        # 1. 直接遍历路径找到父节点
        parent_node = self
        for segment in parent_path_segments:
            if segment in parent_node._children:
                parent_node = parent_node._children[segment]
            else:
                # 如果父路径不存在，则无法删除
                return False

        # 2. 从找到的父节点中删除子节点
        if parent_node and child_name in parent_node._children:
            child_object = parent_node._children[child_name]
            child_object._parent = None  # 清除弱引用
            del parent_node._children[child_name]
            return True

        return False

    def __getattribute__(self, name: str):
        """允许将子节点作为属性进行访问。"""
        children = object.__getattribute__(self, "_children")
        if name in children:
            return children[name]
        return object.__getattribute__(self, name)

    def __repr__(self):
        """返回节点的开发者友好表示形式。"""
        parent_name = self.parent.name if self.parent else None
        return f"<TreeNode: {self.name}, data: {self.data}, parent: {parent_name}>"
