import gc

import pytest

from src.core.tree import TreeNode


@pytest.fixture
def root_node():
    """提供一个基础的根节点，用于各个测试。"""
    return TreeNode("root", data={"id": 0})


class TestTreeNode:
    """TreeNode 类的测试套件。"""

    def test_node_initialization_and_properties(self, root_node):
        """测试：节点初始化时，各个属性是否正确。"""
        assert root_node.name == "root"
        assert root_node.data == {"id": 0}
        assert root_node.parent is None
        assert root_node._children == {}

    def test_parent_is_weakref(self):
        """测试：父节点引用是否为弱引用，以防止循环引用和内存泄漏。"""
        parent = TreeNode("parent")
        child = TreeNode("child", parent=parent)

        assert child.parent is parent

        # 删除父节点对象并强制执行垃圾回收
        del parent
        gc.collect()

        # 此时，弱引用应该已经失效
        assert child.parent is None, "父节点删除后，子节点的 parent 属性应为 None"

    def test_add_child_with_name_creates_child(self, root_node):
        """测试：当提供了 name 时，add_child 应创建子节点。"""
        # 使用新签名：name 在前，data 在后
        child_a = root_node.add_child(name="a", data="data_a")

        assert "a" in root_node._children, "子节点 'a' 应该在 _children 字典中"
        assert root_node.a is child_a, "应该可以通过 root.a 访问子节点"
        assert child_a.parent is root_node, "子节点的 parent 应该指向 root"
        assert child_a.name == "a"
        assert child_a.data == "data_a"

    def test_add_child_with_none_name_updates_self(self, root_node):
        """测试：当 name 为 None 时，add_child 应直接更新当前节点的数据。"""
        original_children_count = len(root_node._children)

        # 调用 add_child 时 name 参数使用默认值 None
        modified_node = root_node.add_child(data="updated_root_data")

        assert modified_node is root_node, "当 name 为 None 时，方法应返回 self"
        assert root_node.data == "updated_root_data", "当前节点的数据应该被更新"
        assert len(root_node._children) == original_children_count, "不应该添加任何新的子节点"

    def test_add_child_multi_level_path_creation(self, root_node):
        """测试：使用点分隔路径添加多层子节点，验证中间节点是否被创建。"""
        leaf_node = root_node.add_child(name="b.c.d", data="deep_data")

        assert root_node.has_child("b.c.d")
        assert root_node.b.c.d is leaf_node
        assert leaf_node.data == "deep_data"
        assert leaf_node.parent.name == "c"

    def test_get_child_and_has_child(self, root_node):
        """测试：get_child 和 has_child 方法能否正确查找节点。"""
        root_node.add_child(name="x.y.z")

        assert root_node.has_child("x.y.z") is True
        assert root_node.has_child("x.a") is False

        node_y = root_node.get_child("x.y")
        assert isinstance(node_y, TreeNode)
        assert node_y.name == "y"
        assert root_node.get_child("nonexistent.path") is None

    def test_get_children(self, root_node):
        """测试：get_children 能正确返回当前节点或指定路径下的所有子节点。"""
        # 添加一些嵌套结构
        root_node.add_child(name="a.b.c", data=1)
        root_node.add_child(name="a.b.d", data=2)
        root_node.add_child(name="x.y", data=3)

        # 1. 获取当前节点的所有直接子节点（应有 a 和 x）
        children = root_node.get_children()
        assert isinstance(children, dict)
        assert set(children.keys()) == {"a", "x"}

        # 2. 获取 a.b 的子节点（应有 c 和 d）
        ab_children = root_node.get_children("a.b")
        assert isinstance(ab_children, dict)
        assert set(ab_children.keys()) == {"c", "d"}

        # 3. 获取不存在路径的子节点（应为 None）
        non_exist = root_node.get_children("not.exist")
        assert non_exist is None

        # 4. 获取叶子节点（a.b.c）的子节点（应为空字典）
        leaf_children = root_node.get_children("a.b.c")
        assert leaf_children == {}

    def test_remove_child_single_and_multi_level(self, root_node):
        """测试：删除单层和多层嵌套的子节点。"""
        root_node.add_child(name="a.b.c")
        node_d = root_node.add_child(name="d")

        # 删除嵌套子节点
        assert root_node.remove_child("a.b.c") is True
        assert not root_node.has_child("a.b.c")

        # 删除直接子节点并检查其 parent 引用
        assert root_node.remove_child("d") is True
        assert not root_node.has_child("d")
        assert node_d.parent is None

    def test_attribute_access_error(self, root_node):
        """测试：访问一个不存在的属性（也不是子节点名）时，应抛出 AttributeError。"""
        with pytest.raises(AttributeError):
            _ = root_node.non_existent_child

    def test_repr_output(self, root_node):
        """测试：节点的 __repr__ 方法是否产生预期的字符串。"""
        child = root_node.add_child(name="child1", data=123)

        expected_root_repr = "<TreeNode: root, data: {'id': 0}, parent: None>"
        expected_child_repr = "<TreeNode: child1, data: 123, parent: root>"

        assert repr(root_node) == expected_root_repr
        assert repr(child) == expected_child_repr

    def test_add_child_to_existing_path_updates_data(self, root_node):
        """测试：对一个已存在的路径调用 add_child 时，应只更新其数据。"""
        node1 = root_node.add_child(name="a.b", data="initial")
        assert node1.data == "initial"

        # 再次对相同路径调用，传入新数据
        node2 = root_node.add_child(name="a.b", data="updated")

        assert node1 is node2, "应该是同一个节点对象"
        assert root_node.a.b.data == "updated", "数据应该被更新"
