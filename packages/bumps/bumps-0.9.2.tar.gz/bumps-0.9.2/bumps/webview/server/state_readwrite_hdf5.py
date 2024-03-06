from collections import deque
import json
from queue import Queue
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING
from threading import Event
import asyncio
import h5py
import numpy as np

from bumps.dream.state import MCMCDraw
from .state_hdf5_backed import SERIALIZERS, serialize_problem, deserialize_problem

if TYPE_CHECKING:
    import bumps, bumps.fitproblem, bumps.dream.state
    from .webserver import TopicNameType
    from .fit_thread import FitThread
    from h5py import Group, Dataset


SESSION_FILE_NAME = "session.h5"
MAX_PROBLEM_SIZE = 100*1024*1024 # 10 MB problem max size
UNCERTAINTY_DTYPE = 'f'
MAX_LABEL_LENGTH = 1024
LABEL_DTYPE = f"|S{MAX_LABEL_LENGTH}"
COMPRESSION = 5
UNCERTAINTY_COMPRESSION = None

def write_string_data(group: 'Group', name: str, data: str, maxsize=102400):
    if data is not None:
        dset = group.create_dataset(name, data=[data], compression=COMPRESSION, dtype=f"|S{maxsize}")
    else:
        dset = group.create_dataset(name, dtype="S1") # empty
    return dset

def read_string_data(group: 'Group', name: str):
    raw_data = group[name]
    if isinstance(raw_data, h5py.Empty):
        return None
    else:
        return raw_data[0]

def write_fitproblem(group: 'Group', name: str, fitProblem: 'bumps.fitproblem.FitProblem', serializer: SERIALIZERS):
    serialized = serialize_problem(fitProblem, serializer) if fitProblem is not None else None
    dset = write_string_data(group, name, serialized, maxsize=MAX_PROBLEM_SIZE)
    return dset

def read_fitproblem(group: 'Group', name: str, serializer: SERIALIZERS):
    serialized = read_string_data(group, name)
    fitProblem = deserialize_problem(serialized, serializer) if serialized is not None else None
    return fitProblem

def write_string(group: 'Group', name: str, value: Optional[str]):
    serialized = value.encode() if value is not None else None
    dset = write_string_data(group, name, serialized)
    return dset

def read_string(group: 'Group', name: str):
    serialized = read_string_data(group, name)
    return serialized.decode() if serialized is not None else None

def write_json(group: 'Group', name: str, data):
    serialized = json.dumps(data) if data is not None else None
    dset = write_string_data(group, name, serialized)
    return dset

def read_json(group: 'Group', name: str):
    serialized = read_string_data(group, name)
    return json.loads(serialized) if serialized is not None else None

def write_ndarray(group: 'Group', name: str, data: Optional[np.ndarray], dtype=UNCERTAINTY_DTYPE):
    if data is not None:
        dset = group.create_dataset(name, data=data, dtype=dtype, compression=UNCERTAINTY_COMPRESSION)
    else:
        dset = group.create_dataset(name, dtype='f') # empty
    return dset

def read_ndarray(group: 'Group', name: str):
    raw_data = group[name]
    return None if isinstance(raw_data, h5py.Empty) else raw_data[()]

class StringAttribute:
    @classmethod
    def serialize(value, obj=None):
        return json.dumps(value)

    @classmethod
    def deserialize(value, obj=None):
        return json.loads(value) if value else None

class ProblemState:
    fitProblem: Optional['bumps.fitproblem.FitProblem'] = None
    pathlist: Optional[List[str]] = None
    serializer: Optional[SERIALIZERS] = None
    filename: Optional[str] = None

    def write(self, parent: 'Group'):
        group = parent.require_group('problem')
        write_fitproblem(group, 'fitProblem', self.fitProblem, self.serializer)
        write_string(group, 'serializer', self.serializer)
        write_json(group, 'pathlist', self.pathlist)
        write_string(group, 'filename', self.filename)

    def read(self, parent: 'Group'):
        group = parent.require_group('problem')
        self.serializer = read_string(group, 'serializer')
        self.fitProblem = read_fitproblem(group, 'fitProblem', self.serializer)
        self.pathlist = read_json(group, 'pathlist')
        self.filename = read_string(group, 'filename')
        print('fitProblem: ', self.fitProblem, self.serializer)
               

class UncertaintyStateStorage:
    AR: Optional['np.ndarray'] = None
    gen_draws: Optional['np.ndarray'] = None
    labels: Optional['np.ndarray'] = None
    thin_draws: Optional['np.ndarray'] = None
    gen_logp: Optional['np.ndarray'] = None
    thin_logp: Optional['np.ndarray'] = None
    thin_point: Optional['np.ndarray'] = None
    update_CR_weight: Optional['np.ndarray'] = None
    update_draws: Optional['np.ndarray'] = None

    def write(self, parent: 'Group'):
        group = parent.require_group('uncertainty_state')
        for attrname in ['AR', 'gen_draws', 'thin_draws', 'gen_logp', 'thin_logp', 'thin_point', 'update_CR_weight', 'update_draws']:
            write_ndarray(group, attrname, getattr(self, attrname), dtype=UNCERTAINTY_DTYPE)
        write_ndarray(group, 'labels', self.labels, dtype=LABEL_DTYPE)

    def read(self, parent: 'Group'):
        group = parent['uncertainty_state']
        for attrname in ['AR', 'gen_draws', 'labels', 'thin_draws', 'gen_logp', 'thin_logp', 'thin_point', 'update_CR_weight', 'update_draws']:
            setattr(self, attrname, read_ndarray(group, attrname))

class FittingState:
    population: Optional[List] = None
    uncertainty_state: Optional['bumps.dream.state.MCMCDraw'] = None

    def write(self, parent: 'Group'):
        group = parent.require_group('fitting')
        write_ndarray(group, 'population', self.population)
        uncertainty_state_storage = UncertaintyStateStorage()
        uncertainty_state = self.uncertainty_state
        if uncertainty_state is not None:
            write_uncertainty_state(uncertainty_state, uncertainty_state_storage)
            uncertainty_state_storage.write(group)

    def read(self, parent: 'Group'):
        group = parent['fitting']
        print("fitting group:", group)
        population = read_ndarray(group, 'population')
        print("population read in")
        self.population = population
        if 'uncertainty_state' in group:
            uncertainty_state_storage = UncertaintyStateStorage()
            uncertainty_state_storage.read(group)
            self.uncertainty_state = read_uncertainty_state(uncertainty_state_storage)
        print("uncertainty done")


class State:
    # These attributes are ephemeral, not to be serialized/stored:
    hostname: str
    port: int
    parallel: int
    abort_queue: Queue
    fit_thread: Optional['FitThread'] = None
    fit_abort: Optional[Event] = None
    fit_abort_event: Event
    fit_complete_event: Event
    calling_loop: Optional[asyncio.AbstractEventLoop] = None
    fit_enabled: Event
    session_file_name: Optional[str]

    # State to be stored:
    problem: ProblemState
    fitting: FittingState
    topics: Dict['TopicNameType', 'deque[Dict]']

    def __init__(self, problem: Optional[ProblemState] = None, fitting: Optional[FittingState] = None):
        self.problem = problem if problem is not None else ProblemState()
        self.fitting = FittingState()
        self.fit_abort_event = Event()
        self.fit_complete_event = Event()
        self.topics = {
            "log": deque([]),
            "update_parameters": deque([], maxlen=1),
            "update_model": deque([], maxlen=1),
            "model_loaded": deque([], maxlen=1),
            "fit_active": deque([], maxlen=1),
            "convergence_update": deque([], maxlen=1),
            "uncertainty_update": deque([], maxlen=1),
            "fitter_settings": deque([], maxlen=1),
            "fitter_active": deque([], maxlen=1),
        }

    def setup_backing(self, session_file_name: Optional[str] = SESSION_FILE_NAME, read_only: bool = False ):
        self.session_file_name = session_file_name
        if session_file_name is not None:
            if Path(session_file_name).exists():
                self.read_session_file(session_file_name)
            else:
                self.save()

    def save(self):
        if self.session_file_name is not None:
            self.write_session_file(self.session_file_name)

    def copy_session_file(self, session_copy_name: str):
        self.write_session_file(session_copy_name)

    def write_session_file(self, session_filename: str):
        import time
        start_time = time.time()
        import os
        import shutil
        import tempfile
        from pathlib import Path
        tmp_fd, tmp_name = tempfile.mkstemp(dir=Path('.'))
        with os.fdopen(tmp_fd, 'w+b') as output_file:
            with h5py.File(output_file, 'w') as root_group:
                self.problem.write(root_group)
                self.fitting.write(root_group)
                self.write_topics(root_group)
        shutil.move(tmp_name, session_filename)
        end_time = time.time()
        print("time to write: ", end_time - start_time)

    def read_session_file(self, session_filename: str):
        try:
            with h5py.File(session_filename, 'r') as root_group:
                self.problem.read(root_group)
                print("problem loaded")
                self.fitting.read(root_group)
                print("uncertainty loaded")
                self.read_topics(root_group)
                print("topics done")
        except Exception as e:
            print(f"could not load session file {session_filename} because of {e}")

    def write_topics(self, parent: 'Group'):
        group = parent.require_group('topics')
        for topic, messages in self.topics.items():
            write_json(group, topic, list(messages))

    def read_topics(self, parent: 'Group'):
        group = parent.require_group('topics')
        for topic in group:
            topic_data = read_json(group, topic)
            if topic_data is not None:
                self.topics[topic].extend(topic_data)

    def cleanup(self):
        self._session_file.close()

    def __del__(self):
        self.cleanup()

    async def async_cleanup(self):
        self.cleanup()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cleanup()
    async def cleanup(self):
        pass

def write_uncertainty_state(state: 'MCMCDraw', storage: UncertaintyStateStorage):
        # Build 2-D data structures
        storage.gen_draws, storage.gen_logp = state.logp(full=True)
        _, storage.AR = state.acceptance_rate()

        storage.thin_draws, storage.thin_point, storage.thin_logp = state.chains()
        storage.update_draws, storage.update_CR_weight = state.CR_weight()
        storage.labels = np.array(state.labels, dtype=LABEL_DTYPE)

def read_uncertainty_state(loaded: UncertaintyStateStorage, skip=0, report=0, derived_vars=0):

    # Guess dimensions
    Ngen = loaded.gen_draws.shape[0]
    thinning = 1
    Nthin, Npop, Nvar = loaded.thin_point.shape
    Nupdate, Ncr = loaded.update_CR_weight.shape
    Nthin -= skip

    # Create empty draw and fill it with loaded data
    state = MCMCDraw(0, 0, 0, 0, 0, 0, thinning)
    #print("gen, var, pop", Ngen, Nvar, Npop)
    state.draws = Ngen * Npop
    state.labels = [label.decode() for label in loaded.labels]
    state.generation = Ngen
    state._gen_index = 0
    state._gen_draws = loaded.gen_draws
    state._gen_acceptance_rate = loaded.AR
    state._gen_logp = loaded.gen_logp
    state.thinning = thinning
    state._thin_count = Ngen//thinning
    state._thin_index = 0
    state._thin_draws = loaded.thin_draws
    state._thin_logp = loaded.thin_logp
    state._thin_point = loaded.thin_point
    state._gen_current = state._thin_point[-1].copy()
    state._update_count = Nupdate
    state._update_index = 0
    state._update_draws = loaded.update_draws
    state._update_CR_weight = loaded.update_CR_weight
    state._outliers = []
