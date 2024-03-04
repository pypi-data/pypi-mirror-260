from dataclasses import dataclass
from typing import Callable, Dict, List

from perfetto.trace_processor import TraceProcessor

from .slice import Slice


@dataclass
class SliceSet:
    """
    A set of `Slice`.
    """

    slices: List[Slice]
    id_index: Dict[int, Slice] = None
    name_index: Dict[str, List[Slice]] = None
    root: Slice = None

    @classmethod
    def from_query(cls, tp: TraceProcessor, query: str) -> "SliceSet":
        slices: List[Slice] = []

        for row in tp.query(query):
            slice = Slice(
                id=row.id,
                ts=row.ts,
                dur=row.dur,
                name=row.name,
                parent_id=row.parent_id,
            )
            slices.append(slice)

        slice_set = SliceSet(slices=slices)
        return slice_set

    def optimize(self):
        self.index_id()
        self.index_name()
        self.construct_tree()
        self.root.compute_self_dur()
        return self

    def index_id(self):
        self.id_index = {}
        for slice in self.slices:
            self.id_index[slice.id] = slice
        return self

    def index_name(self):
        self.name_index = {}
        for slice in self.slices:
            if slice.name in self.name_index:
                self.name_index[slice.name].append(slice)
            else:
                self.name_index[slice.name] = [slice]
        return self

    def construct_tree(self):
        self.root = Slice(id=-1, ts=-1, dur=-1, name="root")
        for slice in self.slices:
            if slice.parent_id is not None and slice.parent_id in self.id_index:
                slice.parent = self.id_index[slice.parent_id]
                slice.parent.children.append(slice)
            else:
                slice.parent = self.root
                self.root.children.append(slice)
        return self

    def filter_tree(self, filter: Callable[[Slice], bool]):

        def _filter_tree(slice: Slice):
            for child in slice.children[:]:
                _filter_tree(child)

            slice.children = sorted(slice.children, key=lambda s: s.ts)

            if slice.parent is not None and not filter(slice):
                for child in slice.children:
                    child.parent = slice.parent

                self.slices.remove(slice)
                slice.parent.children.remove(slice)
                slice.parent.children += slice.children

        _filter_tree(self.root)

        return self

    def print(self):
        def _print(slice: Slice, depth: int):
            print(f"{' ' * depth}{slice.name} (ts={slice.ts}, dur={slice.dur})")
            for child in slice.children:
                _print(child, depth + 1)

        _print(self.root, 0)
