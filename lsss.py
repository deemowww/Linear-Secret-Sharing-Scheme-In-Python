import numpy as np


# lexer for access policy
class lexer:
    def __init__(self, string: str):
        self.text = string
        self.index = 0

    def read_token(self):
        while self.index < len(self.text):
            c = self.text[self.index]
            if c == ' ':
                self.index += 1
                continue

            if c == '(':
                self.index += 1
                return '('

            if c == ')':
                self.index += 1
                return ')'

            if (c.isalpha() or c.isdigit()) or c == '_':
                f = self.index
                while True:
                    self.index += 1

                    if self.index == len(self.text):
                        return self.text[f: self.index]

                    c = self.text[self.index]

                    if not ((c.isalpha() or c.isdigit()) or c == '_'):
                        return self.text[f: self.index]

            if self.index == len(self.text):
                return ""

            raise ValueError("bad policy(%s) at %d" % (self.text, self.index))

        return ""


# tree nodes for access policy
class lsss_tree_node:
    def __init__(self, left, right, is_leaf, is_and_node, attr: str):
        self.left = left
        self.right = right
        self.is_leaf = is_leaf
        self.is_and_node = is_and_node
        self.attr = attr
        self.index = -1

    def init_index(self, base: int):
        if self.is_leaf:
            self.index = base
            return base + 1

        base_next = self.left.init_index(base)
        base_next = self.right.init_index(base_next)

        return base_next

    def match(self, attr_set):
        if self.is_leaf:
            return self.attr in attr_set, [self.index]

        if self.is_and_node:
            matched, arr = self.left.match(attr_set)
            if not matched:
                return False, None
            matched, arr2 = self.right.match(attr_set)
            if not matched:
                return False, None
            arr.extend(arr2)
            return True, arr
        else:
            matched, arr = self.left.match(attr_set)
            if matched:
                return True, arr
            matched, arr2 = self.right.match(attr_set)
            if matched:
                return True, arr2
            return False, None


def leaf_node(att):
    return lsss_tree_node(None, None, True, False, att)


def and_node(left, right):
    return lsss_tree_node(left, right, False, True, "")


def or_node(left, right):
    return lsss_tree_node(left, right, False, False, "")


def or_item(pa, pb):
    size_pa = pa.shape
    size_pb = pb.shape

    row_a = size_pa[0]
    row_b = size_pb[0]

    tmp1 = np.r_[pa[:, :1], pb[:, :1]]
    tmp2 = np.lib.pad(pa[:, 1:], ((0, row_b), (0, 0)), 'constant', constant_values=(0))
    tmp3 = np.lib.pad(pb[:, 1:], ((row_a, 0), (0, 0)), 'constant', constant_values=(0))

    return np.c_[tmp1, tmp2, tmp3]


def and_item(pa, pb):
    oi = or_item(pa, pb)

    tmp1 = np.lib.pad(pa[:, :1], ((0, pb.shape[0]), (0, 0)), 'constant', constant_values=(0))

    return np.c_[tmp1, oi]


def or_with_tag(pa, pb):
    tmp0 = np.r_[pa[:, :1], pb[:, :1]]
    tmp1 = or_item(pa[:, 1:], pb[:, 1:])
    return np.c_[tmp0, tmp1]


def and_with_tag(pa, pb):
    tmp0 = np.r_[pa[:, :1], pb[:, :1]]
    tmp1 = and_item(pa[:, 1:], pb[:, 1:])
    return np.c_[tmp0, tmp1]


def parse_policy(policy):
    lex = lexer(policy)
    return parse(lex, 0)


def parse(lex, level):
    begin = parse_token(lex, level)
    next_token = begin
    while True:
        next_token, tag = parse_logic(lex, next_token, level)
        if tag == ")":
            if level == 0:
                raise ValueError("bad ) at parse")
            return next_token
        if tag == "EOF":
            return next_token

        if len(next_token[0]) == 0:
            break

    return begin


def parse_logic(lex, left, level):
    token = lex.read_token()

    if token == ")":
        return left, ")"

    if len(token) == 0:
        return left, "EOF"

    if token == "and":
        left_mat, left_node = left
        right_mat, right_node = parse_token(lex, level)

        mat = and_with_tag(left_mat, right_mat)
        node = and_node(left_node, right_node)

        return (mat, node), "token"

    if token == "or":
        left_mat, left_node = left
        right_mat, right_node = parse_token(lex, level)

        mat = or_with_tag(left_mat, right_mat)
        node = or_node(left_node, right_node)

        return (mat, node), "token"

    raise ValueError("bad token at parse_logic:" + token)


def parse_token(lex, level):
    token = lex.read_token()

    if token is None:
        raise ValueError

    if len(token) == 0 or token == ")":
        raise ValueError("bad token at parse_token:" + token)

    if token == "(":
        return parse(lex, level + 1)

    if token == "and" or token == "or":
        raise ValueError("bad token at parse_token:" + token)

    return np.array([[token, 1]]), leaf_node(token)


def cal_w_by_tree(mat, w_index):
    ret = np.zeros((1, len(mat[0]) - 1))
    for index in w_index:
        ret = np.r_[ret, mat[index: index + 1, 1:]]

    hit = ret[1:, :].T

    filtered = hit[~(hit == '0').all(1)]

    a = np.array(filtered, dtype=np.float)
    b = np.zeros((filtered.shape[1], 1), dtype=np.float)
    b[0][0] = 1

    x = np.linalg.solve(a, b)

    return x


def test(policy, attr_set):
    print("policy: ", end="")
    print(policy)

    print("attr_set: ", end="")
    print(attr_set)

    mat, tree = parse_policy(policy)

    print("matrix: ")
    print(mat)

    tree.init_index(0)

    matched, w_index = tree.match(attr_set)

    if matched:
        print("attr_path: ", end="")
        print(w_index)
    else:
        print("not matched")
        print()
        return

    w = cal_w_by_tree(mat, w_index)

    print("w_result: ")
    print(w)
    print()


if __name__ == '__main__':
    s3 = "(a1 and a2) or (a1 and a3 and a4) or (a4 and a5) or (a1 and a5)"

    s4 = "a1 or a2 or a3 or a4 or a5"

    s5 = "a1 and a2 and a3 and a4 and a5 and a6"

    s6 = "((a1 and a2) or (a1 and a3 and a4) or (a4 and a5) or (a1 and a5)) and a6"

    all_policy = [s3, s4, s5, s6]

    us = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']

    us2 = ['a1', 'a3', 'a4', 'a6']

    all_attr_set = [us, us2]

    for policy in all_policy:
        for attr_set in all_attr_set:
            test(policy, attr_set)
