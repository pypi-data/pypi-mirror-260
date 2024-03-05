import unittest

import numpy as np
import pandas as pd

from powerplantsim import Plant
from powerplantsim.plant import RecourseAction
from powerplantsim.utils.typing import Plan
from test.test_utils import PLANT, PLAN, IMPLEMENTATION, SETPOINT

INVALID_PLANT_EXCEPTION = lambda k, e, c, n: f"{k} commodity {c} has no valid {e} edge in node {n}"
SECOND_RUN_EXCEPTION = lambda: "Simulation for this plant was already run, create a new instance to run another one"
INPUT_VECTOR_EXCEPTION = lambda k, l: f"Vector for key '{k}' has length {l}, expected 3"
UNKNOWN_DATATYPE_EXCEPTION = lambda k: f"Key {k} is not present in the plant"
MISSING_DATATYPE_EXCEPTION = lambda t, g, l: f"No {t} vector has been passed for {g} {l}"


class DummyAction(RecourseAction):
    def execute(self) -> Plan:
        return {key: vector[self._plant.step] for key, vector in IMPLEMENTATION.items()}


class TestPlantRun(unittest.TestCase):
    def test_output(self):
        """Test the output of a simulation."""
        p = PLANT.copy()
        output = p.run(plan=PLAN, action=DummyAction(), progress=False)
        self.assertDictEqual(output.flows.to_dict(), {
            ('sup', 'mac_1'): {0: 1., 1: 2., 2: 3.},
            ('sup', 'mac_2'): {0: 0., 1: 0., 2: 0.},
            ('mac_1', 'cus'): {0: 1., 1: 2., 2: 3.},
            ('mac_1', 'sto'): {0: 0., 1: 0., 2: 0.},
            ('mac_2', 'pur'): {0: 0., 1: 0., 2: 0.},
            ('sto', 'cus'): {0: 0., 1: 0., 2: 0.},
            ('sto', 'pur'): {0: 0., 1: 0., 2: 0.}
        }, msg=f"Wrong output flows returned")
        self.assertDictEqual(
            output.storage.to_dict(),
            {'sto': {0: 0., 1: 0., 2: 0.}},
            msg="Wrong output storage returned"
        )
        self.assertDictEqual(
            output.demands.to_dict(),
            {'cus': {0: 1., 1: 2., 2: 3.}},
            msg="Wrong output demands returned"
        )
        self.assertDictEqual(
            output.buying_prices.to_dict(),
            {'pur': {0: 1., 1: 2., 2: 3.}},
            msg="Wrong output buying prices returned"
        )
        self.assertDictEqual(
            output.sell_prices.to_dict(),
            {'sup': {0: 1., 1: 2., 2: 3.}},
            msg="Wrong output selling prices returned"
        )
        # test mac_1 and mac_2 separately due to nan values returning False when compared
        self.assertSetEqual(set(output.states.columns), {'mac_1', 'mac_2'}, msg=f"Wrong output states returned")
        self.assertDictEqual(
            output.states.to_dict()['mac_1'],
            {0: 1., 1: 2., 2: 3.},
            msg=f"Wrong output states returned"
        )
        self.assertDictEqual(
            output.states.isna().to_dict()['mac_2'],
            {0: True, 1: True, 2: True},
            msg=f"Wrong output states returned"
        )

    def test_invalid_plant(self):
        p = Plant(horizon=1)
        p.add_extremity(kind='supplier', name='sup', commodity='in', predictions=1.)
        with self.assertRaises(AssertionError, msg="Running an invalid plant should raise an exception") as e:
            p.run(plan={}, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            INVALID_PLANT_EXCEPTION('Output', 'outgoing', 'in', 'sup'),
            msg='Wrong exception message returned for running an invalid plant'
        )
        p.add_machine(name='mac', parents='sup', **SETPOINT)
        with self.assertRaises(AssertionError, msg="Running an invalid plant should raise an exception") as e:
            p.run(plan={'mac': np.nan, ('sup', 'mac'): 0.0}, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            INVALID_PLANT_EXCEPTION('Output', 'outgoing', 'out', 'mac'),
            msg='Wrong exception message returned for running an invalid plant'
        )
        p.add_extremity(kind='customer', name='cus', commodity='out', parents='mac', predictions=1.)
        plan = {'mac': np.nan, ('sup', 'mac'): 0.0, ('mac', 'cus'): 0.0}
        p.run(plan=plan, action=lambda _: plan, progress=False)

    def test_already_run(self):
        p = PLANT.copy()
        p.run(plan=PLAN, action=DummyAction(), progress=False)
        with self.assertRaises(AssertionError, msg="Running a second simulation should raise an error") as e:
            p.run(plan=PLAN, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            SECOND_RUN_EXCEPTION(),
            msg='Wrong exception message returned for running a second simulation on the same plant'
        )

    def test_input_plan(self):
        """Test that the input plan is consistency processed."""
        # test correct dataframe input
        p = PLANT.copy()
        df = pd.DataFrame(PLAN, index=p.horizon)
        p.run(plan=df, action=DummyAction(), progress=False)
        # test wrong input vector
        p = PLANT.copy()
        with self.assertRaises(AssertionError, msg="Wrong input vectors should raise an error") as e:
            p.run(plan={'mac_1': [1., 2.]}, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            INPUT_VECTOR_EXCEPTION('mac_1', 2),
            msg='Wrong exception message returned for wrong input vectors on plant'
        )
        with self.assertRaises(AssertionError, msg="Wrong input vectors should raise an error") as e:
            p.run(plan={'mac_1': [1., 2., 3.], ('sup', 'mac_1'): [1.]}, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            INPUT_VECTOR_EXCEPTION(('sup', 'mac_1'), 1),
            msg='Wrong exception message returned for wrong input vectors on plant'
        )
        # test unknown datatype
        with self.assertRaises(AssertionError, msg="Unknown datatype should raise an error") as e:
            p.run(plan={'mac': [1., 2., 3.]}, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            UNKNOWN_DATATYPE_EXCEPTION("'mac'"),
            msg='Wrong exception message returned for unknown datatype vectors on plant'
        )
        with self.assertRaises(AssertionError, msg="Unknown datatype should raise an error") as e:
            p.run(plan={('sup', 'mac'): [1., 2., 3.]}, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            UNKNOWN_DATATYPE_EXCEPTION(('sup', 'mac')),
            msg='Wrong exception message returned for unknown datatype vectors on plant'
        )
        # test missing datatype
        plan = PLAN.copy()
        plan.pop('mac_2')
        with self.assertRaises(AssertionError, msg="Missing datatype should raise an error") as e:
            p.run(plan=plan, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            MISSING_DATATYPE_EXCEPTION('states', 'machines', ['mac_2']),
            msg='Wrong exception message returned for missing datatype vectors on plant'
        )
        plan = PLAN.copy()
        plan.pop(('sup', 'mac_2'))
        with self.assertRaises(AssertionError, msg="Missing datatype should raise an error") as e:
            p.run(plan=plan, action=DummyAction(), progress=False)
        self.assertEqual(
            str(e.exception),
            MISSING_DATATYPE_EXCEPTION('flows', 'edges', [('sup', 'mac_2')]),
            msg='Wrong exception message returned for missing datatype vectors on plant'
        )

    def test_action_output(self):
        """Test that the recourse action output is consistency processed."""
        p = PLANT.copy()
        # test unknown datatype
        with self.assertRaises(AssertionError, msg="Unknown datatype in recourse action should raise an error") as e:
            p.run(plan=PLAN, action=lambda _: {'mac': 1.}, progress=False)
        self.assertEqual(
            str(e.exception),
            UNKNOWN_DATATYPE_EXCEPTION("'mac'"),
            msg='Wrong exception message returned for unknown datatype vectors in recourse action on plant'
        )
        p = PLANT.copy()
        with self.assertRaises(AssertionError, msg="Unknown datatype in recourse action should raise an error") as e:
            p.run(plan=PLAN, action=lambda _: {('sup', 'mac'): 1.}, progress=False)
        self.assertEqual(
            str(e.exception),
            UNKNOWN_DATATYPE_EXCEPTION(('sup', 'mac')),
            msg='Wrong exception message returned for unknown datatype in recourse action vectors on plant'
        )
        # test missing datatype
        p = PLANT.copy()
        a = DummyAction().build(p)
        with self.assertRaises(AssertionError, msg="Missing datatype in recourse action should raise an error") as e:
            p.run(plan=PLAN, action=lambda _: {k: v for k, v in a.execute().items() if k != 'mac_2'}, progress=False)
        self.assertEqual(
            str(e.exception),
            MISSING_DATATYPE_EXCEPTION('states', 'machines', ['mac_2']),
            msg='Wrong exception message returned for missing datatype in recourse action vectors on plant'
        )
        p = PLANT.copy()
        a = DummyAction().build(p)
        with self.assertRaises(AssertionError, msg="Missing datatype in recourse action should raise an error") as e:
            p.run(
                plan=PLAN,
                action=lambda _: {k: v for k, v in a.execute().items() if k != ('sup', 'mac_2')},
                progress=False
            )
        self.assertEqual(
            str(e.exception),
            MISSING_DATATYPE_EXCEPTION('flows', 'edges', [('sup', 'mac_2')]),
            msg='Wrong exception message returned for missing datatype in recourse action vectors on plant'
        )
