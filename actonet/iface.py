
from .gc import gc_controls

def v(n):
    return "v{}".format(n)
def to_n(v):
    return v[1:]

def asp_of_condition(state):
    def from_cond(ns):
        n, s = ns
        pre = "not " if not s else ""
        return "{}{}".format(pre, v(n))
    return ", ".join(map(from_cond, sorted(state.items())))

class ActoNet(object):
    def __init__(self, bn):
        # TODO: handle constants
        self.bn = bn
        self.inputs = []
        self.outputs = []
        self.input_conditions = {}
        self.property = None

    def _assert_defined(self, nodes):
        for n in nodes:
            assert n in self.bn, "unknown variable '{}'".format(n)

    def set_outputs(self, outputs):
        self._assert_defined(outputs)
        self.outputs = outputs

    def set_input_condition(self, state):
        self._assert_defined(state)
        self.input_conditions = state
        self.inputs = set(self.input_conditions.keys())

    def set_property(self, state):
        self._assert_defined(state)
        self.property = state


    def asp_fixpoint(self):
        clauses = []

        def from_literal(l):
            if l[0] in self.inputs:
                pre = "not " if not l[1] else ""
                return "{}holds({})".format(pre, v(l[0]))
            pre = "not " if l[1] else ""
            return "{}not {}".format(pre, v(l[0]))
        def from_clause(c):
            return ", ".join(map(from_literal, c))

        for n, cs in sorted(self.bn.as_dnf().items()):
            if n in self.inputs:
                continue
            is_output = n in self.outputs
            if not is_output:
                clauses.append("{0} :- holds(set({0}, 1)).".format(v(n)))
            for c in cs:
                pre = "not holds(set({}, _)), ".format(v(n)) if not is_output else ""
                clauses.append("{} :- {}{}.".format(v(n), pre, from_clause(c)))

        return clauses

    def asp_guess(self):
        clauses = [
            "value(0;1).",
            "variable({}).".format("; ".join(map(v, sorted(self.bn.keys())))),
            "output({}).".format("; ".join(map(v, sorted(self.outputs)))),
            "controlled(X) :- variable(X), not output(X).", # XXX controllable variables
            "control(X,T) :- controlled(X), value(T).",
            "#const maxcontrol=2.",
            "{set(X,V) : control(X,V)} maxcontrol.",
            ":- set(X,0), set(X,1).",
            "holds(set(X,V)) :- set(X,V).",
            "#show holds/1.",
            "#show nholds/1.",
            "#project holds/1.",
        ]
        #
        # inputs
        #
        clauses.append("{{{}}}.".format("; ".join(map(v, self.inputs))))
        for n in self.inputs:
            clauses.append("holds({0}) :- {0}.".format(v(n)))
            clauses.append("nholds({0}) :- not holds({0}).".format(v(n)))
        # TODO: ??
        if self.input_conditions:
            clauses.append("inputselectionnecessary :- {}.".format(asp_of_condition(self.input_conditions)))
            clauses.append(":- not inputselectionnecessary.")
        return clauses

    def asp_check(self):
        clauses = []
        if self.property:
            clauses.append(":- {}.".format(asp_of_condition(self.property)))
        return clauses

    def controls(self, universal=True, existential=True, maxcontrol=2):
        assert universal or existential, "At least universal or existential should be true"
        if universal:
            has_fixpoint = self.asp_fixpoint()
            guess = self.asp_guess()
            if existential:
                guess += has_fixpoint
            check = self.asp_check() + has_fixpoint
            guess = "\n".join(guess)
            check = "\n".join(check)
            for control in gc_controls(guess, check, maxcontrol=maxcontrol):
                c = {}
                m = {}
                for f in control:
                    assert f.name in ["holds", "nholds"]
                    g = f.arguments[0]
                    if g.name == "set" and len(g.arguments) == 2:
                        assert f.name == "holds"
                        m[to_n(g.arguments[0].name)] = g.arguments[1].number
                    else:
                        c[to_n(g.name)] = 1 if f.name == "holds" else 0
                if len(self.input_conditions) == len(self.inputs):
                    yield m
                else:
                    yield (c, m)
        else:
            raise NotImplementedError



