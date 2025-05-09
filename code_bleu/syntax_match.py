# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import tree_sitter_c_sharp
import tree_sitter_go
import tree_sitter_java
import tree_sitter_javascript
import tree_sitter_python
from tree_sitter import Language, Parser

from .parser import (
    DFG_csharp,
    DFG_go,
    DFG_java,
    DFG_javascript,
    DFG_php,
    DFG_python,
    DFG_ruby,
    index_to_code_token,
    remove_comments_and_docstrings,
    tree_to_token_index,
    tree_to_variable_index,
)

dfg_function = {
    "python": DFG_python,
    "java": DFG_java,
    "ruby": DFG_ruby,
    "go": DFG_go,
    "php": DFG_php,
    "javascript": DFG_javascript,
    "c_sharp": DFG_csharp,
}

tree_sitter_lib = {
    "python": tree_sitter_python,
    "java": tree_sitter_java,
    "go": tree_sitter_go,
    "javascript": tree_sitter_javascript,
    "c_sharp": tree_sitter_c_sharp,
}


def calc_syntax_match(references, candidate, lang):
    return corpus_syntax_match([references], [candidate], lang)


def corpus_syntax_match(references, candidates, lang):

    parser = Parser(Language(tree_sitter_lib[lang].language()))

    match_count = 0
    total_count = 0

    for i in range(len(candidates)):
        references_sample = references[i]
        candidate = candidates[i]
        for reference in references_sample:
            try:
                candidate = remove_comments_and_docstrings(candidate, lang)
            except:
                pass
            try:
                reference = remove_comments_and_docstrings(reference, lang)
            except:
                pass

            candidate_tree = parser.parse(bytes(candidate, "utf8")).root_node

            reference_tree = parser.parse(bytes(reference, "utf8")).root_node

            def get_all_sub_trees(root_node):
                node_stack = []
                sub_tree_sexp_list = []
                depth = 1
                node_stack.append([root_node, depth])
                while len(node_stack) != 0:
                    cur_node, cur_depth = node_stack.pop()
                    sub_tree_sexp_list.append([str(cur_node), cur_depth])
                    for child_node in cur_node.children:
                        if len(child_node.children) != 0:
                            depth = cur_depth + 1
                            node_stack.append([child_node, depth])
                return sub_tree_sexp_list

            cand_sexps = [x[0] for x in get_all_sub_trees(candidate_tree)]
            ref_sexps = get_all_sub_trees(reference_tree)

            # print(cand_sexps)
            # print(ref_sexps)

            for sub_tree, depth in ref_sexps:
                if sub_tree in cand_sexps:
                    match_count += 1
            total_count += len(ref_sexps)

    score = match_count / total_count
    return score
